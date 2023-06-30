import serial
import keyboard
from time import sleep

#Important : The code will run until Ctrl+C is pressed!

port = "/dev/ttyACM0" 

# Send trial trigger code
def send_trigger(port):
	Ser = serial.Serial(port)
	Ser.close()
	Ser.open()
	Trigger = b'\x01' 
	Ser.write(Trigger)
	Ser.close() 

keyboard.on_press_key("s",lambda _: send_trigger(port))

while True:
    sleep(6000)
