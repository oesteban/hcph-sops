# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2023 The Axon Lab <theaxonlab@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""A signal server listening to scanner trigger events (`s` key press) and psychopy events."""
import sys
from pathlib import Path
from serial import Serial
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import janus
import keyboard
import usb.core
import usb.util


LISTEN = 2023
SERIAL_PORT = "/dev/ttyACM0"
LOG_FILE = Path("/var") / "log" / "forward-trigger-service.log"
LOG_FILE.parent.mkdir(exist_ok=True, parents=True)
USB_MMBTS_DEVICE_ID = (0x07C0, 0x0101)
"""Device ID of the Neurospec's MMBT-S trigger adaptor."""
USB_TESTING_DEVICE_ID = (0x0BC2, 0x2322)
"""Device ID for testing purposes."""

handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="D",
    interval=1,
)

handler.setFormatter(
    logging.Formatter(
        "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ),
)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(handler)


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    async_q: janus.AsyncQueue[int],
) -> None:
    """
    Handle client connections.

    Read incoming data from the client and put it into the async queue.

    Parameters
    ----------
    reader : :obj:`asyncio.StreamReader`
        The client's stream reader.
    writer : :obj:`asyncio.StreamReader`
        The client's stream writer.
    async_q : :obj:`janus.AsyncQueue`
        The async queue for storing incoming signals.

    """
    while True:
        try:
            data = await reader.readexactly(1)
        except asyncio.exceptions.IncompleteReadError:
            await asyncio.sleep(0.1)  # Add a small delay to avoid busy waiting
            continue
        finally:
            writer.close()

        if data > b"\xff" or data < b"\x01":
            LOGGER.warning(f"Received invalid signal <{data}>")
            continue

        # Disallow receiving 00000001 on the socket, replace with 10000001
        if data == b"\x01":
            data = b"\x81"
            LOGGER.warning(
                "Trigger signal received through socket -- replaced with <\\x81>"
            )

        LOGGER.info(f"Data received: <{data}>")
        await async_q.put(data)


async def start_server(host: str, port: int, async_q: janus.AsyncQueue[int]) -> None:
    """
    Start the server.

    Create a server that listens for client connections and handles them.

    Parameters
    ----------
    host : :obj:`str`
        The server's host address.
    port : :obj:`int`
        The server's port number.
    async_q : :obj:`janus.AsyncQueue`
        The async queue for storing incoming signals.

    """
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, async_q), host, port
    )
    addr = server.sockets[0].getsockname()
    LOGGER.info(f"Server listening on {addr}")
    async with server:
        await server.serve_forever()


async def forward_signals(serial_port: str, async_q: janus.AsyncQueue[int]) -> None:
    """
    Forward incoming signals to the serial port.

    Read signals from the async queue and write them to the serial port.

    Parameters
    ----------
    serial_port : :obj:`str`
        The serial port to forward the signals to.
    async_q : :obj:`janus.AsyncQueue`
        The async queue storing the signals.

    """
    with Serial(serial_port) as conn:
        while True:
            signal = await async_q.get()
            conn.write(signal)
            async_q.task_done()
            LOGGER.info(f"Forwarded <{signal}>")


def _trigger(sync_q: janus.SyncQueue[int]) -> None:
    """
    Trigger the signal sync queue.

    Put a signal into the sync queue.

    Parameters:
        sync_q (janus.SyncQueue[int]): The sync queue for triggering the signal.

    """
    sync_q.put(b"\x01")
    sync_q.join()
    LOGGER.info("Scanner trigger received")


def ensure_usb_device_connected(usb_vendor_id, usb_product_id):
    """
    Check if a USB device with the specified vendor and product IDs is connected.

    Parameters
    ----------
    usb_vendor_id : :obj:`str`
        Vendor ID of a USB device.
    usb_product_id : :obj:`str`
        Product ID of a USB device.

    Returns
    -------
    connected : :obj:`bool`
        ``True`` when the device is connected. If the device is not connected, this
        function raises a :obj:`RuntimeError`.

    Raises
    ------
    :obj:`RuntimeError`
        If the USB device is not connected.

    """

    usb_vendor_id = (
        int(usb_vendor_id, 16) if isinstance(usb_vendor_id, str) else usb_vendor_id
    )
    usb_product_id = (
        int(usb_product_id, 16) if isinstance(usb_product_id, str) else usb_product_id
    )
    device = usb.core.find(idVendor=usb_vendor_id, idProduct=usb_product_id)
    if device is None:
        raise RuntimeError("MMTB-S (pink cable) is not connected")
    return True


async def main() -> None:
    """
    Main function.

    Run the signal server and forward the signals to the serial port.

    """
    if "--disable-mmbt-check" not in sys.argv:
        # Check if the USB device is connected
        ensure_usb_device_connected(*USB_MMBTS_DEVICE_ID)

    # Initiate a Queue that has synchronous and asynchronous endpoints.
    signal_queue: janus.Queue[int] = janus.Queue()

    # Attach an event listener to all `s` key presses.
    keyboard.on_press_key("s", lambda key: _trigger(signal_queue.sync_q))

    # Send a binary zero at the beginning
    signal_queue.sync_q.put(b"\x00")

    # Spin up socket listener and (asynchronously) queue up signals arriving from the socket
    await asyncio.gather(
        start_server("localhost", LISTEN, signal_queue.async_q),
        forward_signals(SERIAL_PORT, signal_queue.async_q),
    )


if __name__ == "__main__":
    asyncio.run(main())
