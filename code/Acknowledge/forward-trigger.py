import sys
import serial
import keyboard
import asyncio

port = "/dev/ttyACM0"

def send_trigger():
    with serial.Serial(port) as ser:
        trigger = b'\x01'
        ser.write(trigger)

async def handle_key_press():
    keyboard.add_hotkey("s", send_trigger)
    await asyncio.Event().wait()

async def main():
    await asyncio.gather(
        handle_key_press(),
        asyncio.sleep(0.008)
    )

if __name__ == '__main__':
    print("Main loop")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.stop()
    finally:
        loop.close()




