# RP-Pico-Door-Keyboard-Input
With this python project you can set up a Raspberry Pi Pico to send a keyboard input to your PC. Uses HID, works on any PC without installation

Can be used to close tabs or windows on your PC, when a door is opened. Uses a Raspberry Pi Pico and an HC-SR04 ultrasonic sensor. It communicates with the PC using Circuitpython and the HID Library, so it works on any computer without configuration.

The python code examples and the distance measuring code for the Raspberry Pi Pico are under [examples](https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input/tree/main/examples).

The program under [door-Keyboard](https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input/tree/main/door-Keyboard) is used to create your own keyboard shortcuts and to spefify the distance to the door.

You can find precompiled binaries for Windows and Linux [here](https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input/releases/).

## How to get started
First you need a few Downloads for the Pi Pico:

- [circuitpython.uf2](https://circuitpython.org/board/raspberry_pi_pico/)

- download and extract [circuitpython libraries](https://circuitpython.org/libraries)

- [mu editor](https://codewith.mu/en/download) for serial communication (only for distance mesearing or troubleshooting)

You need to connect a Pi Pico to your computer while holding the BOOTSEL Button. Then drag the .uf2 file onto the Pi Pico(usb drive named CIRCUITPY), the Pi will restart. Drag the adafruit_hid folder from the circuitpython libraries and the adafruit_hcsr04.mpy into the lib folder on the CIRCUITPY drive. Open the code creator and follow the instructions there. You can find the keycodes [here](https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/keycode.py) (just add Keycode.\*\*\*) Seperate each key with a comma. Copy the code.py file created by the program onto the main directory of the Pi Pico. Unplug the Pi Pico and place it where you want to, connect it to a computer with a micro usb cable.

You need to "arm" the system by connecting pin GP2 to ground (use a button).

## How to get the distance

- You can either measure the distance with a tape measure

- Or you can measure it by installing the mu editor, installing the libraries on the Pi Pico and connecting it to the computer. Download [this code](), copy it to the Pi and rename it to code.py

## Trobleshooting

- Great resoruce for help is the [CircuitPython repo](https://github.com/adafruit/circuitpython)
- If you have any questions or bugreports, feel free to open a new issue

- The Pi Pico will only execute files named code.py, so rename your file if it has another name
