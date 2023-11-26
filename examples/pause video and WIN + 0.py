# RP-Pico-Door-Tab-Close
# https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input
# creates a python script for the Raspberry Pi Pico
# drag the distance measruing.py file onto the Raspberry Pi Pico and rename it to code.py
# an example that switches to the first pinned window (browser) and paues the video and switches tabs
# read the github page for further information and libraries
distancedoor = 50 # specify distance to door
import time
import board # GP allocation
import usb_hid # keyboard emulation (Human Interface Device)
import digitalio # digitalIO
import adafruit_hcsr04 #sonar sensor
from adafruit_hid.keyboard import Keyboard # import keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS # import keyboard layout
from adafruit_hid.keycode import Keycode # import keycodes
distance = distancedoor + 5
distanceold = distancedoor + 5

keyboard = Keyboard(usb_hid.devices) # initialize keyboard
keyboard_layout = KeyboardLayoutUS(keyboard) # initialize keyboard layout

reset = digitalio.DigitalInOut(board.GP2) # reset button
reset.direction = digitalio.Direction.INPUT
reset.pull = digitalio.Pull.DOWN
led = digitalio.DigitalInOut(board.GP25) # integrated LED for indication if system is "armed"
led.direction = digitalio.Direction.OUTPUT

resetstate = 0 # variable used to determine wether system is "armed"
led.value = False # turn off LED

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP9, echo_pin=board.GP10, timeout = 1) #sonar sensor on pins GP9 and GP10

while True:
    while resetstate == 1:
        time.sleep(0.4)
        try:
            distance = sonar.distance
            while distance < 10:
                time.sleep(0.5)
                distance = sonar.distance
            distancemed = (distance + distanceold) / 2 #calulate the average of distance and distanceold (previous measurement)
            if distancemed < distancedoor:
                keyboard.send(Keycode.WINDOWS, Keycode.ONE) #switches to first pinned window (should be browser)
                time.sleep(0.1)
                keyboard.send(Keycode.SPACE) #pauses the video
                resetstate = 0
                led.value = False # turns off LED
            distanceold = distance # safe the distance to distanceold to calulate the average
        except RuntimeError: #runtimeErrors can occur while use the sonar sensor
            distance = distancedoor + 5
    while resetstate == 0:
        time.sleep(0.1)
        if reset.value:
            for i in range(8): #Blink LED 8 times before "armed"
                led.value = True
                time.sleep(0.5)
                led.value = False
                time.sleep(0.5)
            led.value = True
            resetstate = 1 # "arms" the system
            distance = distancedoor + 5 # sets a safe value for distance
            distanceold = distancedoor + 5
