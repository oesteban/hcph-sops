import asyncio
import serial
import threading
import keyboard

async def handle_client(reader, signal_queue):
    while True:
        data = await reader.read(1)

        if not data:
            await asyncio.sleep(0.1)  # Add a small delay to avoid busy waiting
            continue

        signal = data  # No need for conversion if the signal is already in binary
        #print(f"Received signal: {signal}")
        await signal_queue.put(signal)

async def start_server(host, port, signal_queue):
    server = await asyncio.start_server(lambda r, w: handle_client(r, signal_queue), host, port)
    addr = server.sockets[0].getsockname()
    print(f"Server listening on {addr}")
    async with server:
        await server.serve_forever()

async def forward_signals(serial_port, signal_queue):
    with serial.Serial(serial_port) as ser:
        while True:
            signal = await signal_queue.get()
            ser.write(signal)

async def keyboard_input(signal_queue):
    while True:
        if keyboard.is_pressed("s"):
            await asyncio.sleep(0.1)
            #print(f"s pressed")
            await signal_queue.put(b"\x01")
        else:
            await asyncio.sleep(0.1)
              # Enqueue b"\x01" into the signal_queue

async def main():
    serial_port = '/dev/ttyACM0'
    signal_queue = asyncio.Queue()

    await asyncio.gather(
        start_server("localhost", 8888, signal_queue),
        forward_signals(serial_port, signal_queue),
        keyboard_input(signal_queue)
    )

if __name__ == "__main__":
    asyncio.run(main())




