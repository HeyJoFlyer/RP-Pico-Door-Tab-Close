import time
import board
import usb_hid
import digitalio
import adafruit_hcsr04
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
distance = 124
distanceold = 124

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

reset = digitalio.DigitalInOut(board.GP2)
reset.direction = digitalio.Direction.INPUT
reset.pull = digitalio.Pull.DOWN
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
print("start")

resetstate = 0
led.value = False

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP9, echo_pin=board.GP10, timeout = 1)

while True:
    while resetstate == 1:
        time.sleep(0.4)
        try:
            distance = sonar.distance
            print("distance, distanceold", distance, distanceold)
            while distance < 10:
                time.sleep(0.5)
                distance = sonar.distance
                print("measurement ERROR", distance)
            distancemed = (distance + distanceold) / 2
            if distancemed < 115:
                keyboard.send(Keycode.WINDOWS, Keycode.ONE)
                time.sleep(0.1)
                keyboard.send(Keycode.SPACE)
                time.sleep(0.05)
                keyboard.send(Keycode.CONTROL, Keycode.TAB)
                print("closed")
                resetstate = 0
                led.value = False
            distanceold = distance
        except RuntimeError:
            print("ERROR")
            distance = 55
            print(distance)
    while resetstate == 0:
        time.sleep(0.1)
        if reset.value:
            print("START RESET")
            for i in range(8):
                led.value = True
                time.sleep(0.5)
                led.value = False
                time.sleep(0.5)
            led.value = True
            resetstate = 1
            distance = 124
            distanceold = 124
            print("RESET")
