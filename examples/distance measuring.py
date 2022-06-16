# RP-Pico-Door-Tab-Close
# https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input
# creates a python script for the Raspberry Pi Pico
# drag the distance measruing.py file onto the Raspberry Pi Pico and rename it to code.py
# measures the distance to the door and prints it over usb
# read the github page for further information and libraries
import time, board, adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP9, echo_pin=board.GP10, timeout = 1)

while True:
    time.sleep(1)
    try:
        print("Distance to the door is", sonar.distance)
    except RuntimeError:
        print("ERROR (this is normal and happens sometimes)")
