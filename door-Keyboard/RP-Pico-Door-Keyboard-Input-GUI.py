# RP-Pico-Door-Tab-Close
# https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input
# creates a python script for the Raspberry Pi Pico
# after following th GUI and pressing GO it will write a code.py file
# drag the code.py file onto the Raspberry Pi Pico
# read the github page for further information and libraries
from ast import Break
import time, webbrowser, os
import PySimpleGUI as sg
sg.theme("DarkAmber")
script = open("code.py", "w") # creates the code.py file
code = ["# RP-Pico-Door-Tab-Close", "# https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input", "import time, board, usb_hid, digitalio, adafruit_hcsr04", "from adafruit_hid.keyboard import Keyboard", "from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS", "from adafruit_hid.keycode import Keycode", "keyboard = Keyboard(usb_hid.devices)", "keyboard_layout = KeyboardLayoutUS(keyboard)", "led = digitalio.DigitalInOut(board.GP25)", "led.direction = digitalio.Direction.OUTPUT", "led.value = False", "sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP9, echo_pin=board.GP10, timeout = 1)", "resetstate = 0", "reset = digitalio.DigitalInOut(board.GP2)", "reset.direction = digitalio.Direction.INPUT", "reset.pull = digitalio.Pull.DOWN"] # first part of code.py, gets added to the list code and is writen to code.py at the end
combinations = []   # creates a list for the keycombinations
Buttonstate = 0 # Sets if a button has changed color and needs to be reset
lowerGUI =  [sg.Frame("keycombinations you entered",[
            [sg.Text("", key = "Keycombinations")]
            ], element_justification="center")]
upperGUI = [sg.Frame("", [[sg.Text("Select the distance to the door here (in cm)"), sg.Slider(range = (10, 400), default_value = 50, orientation = "horizontal", key = "Distance")],
            [sg.HSeparator()],
            [sg.Text("Enter the key combinations you want and press ad for each combination")],
            [sg.Text("Reference on github (use Keyboard.KEY, example Keyboard.WINDOWS; Keyboard.ONE)")],
            [sg.InputText("Keycode.",key="KEYS")], # combinations input
            [sg.Text("")],  #spacer
            [sg.Text("Enter delay to next Keypress (in ms)"), sg.Slider(range = (1, 1000), default_value = 50, orientation ="horizontal", key="Delay")],
            [sg.Button("Add combination", key="ADD")],
            [sg.Button("Remove previous combination", key="REMOVE")],
            [sg.HSeparator()],
            [sg.Text("When finished, press "), sg.Button("GO", key = "GO")],
            [sg.Button("Github", key = "Github")]
            ], element_justification="center")]

layout = [  [upperGUI], # window layout
            [sg.Text("")], # spacer
            [lowerGUI]]

window = sg.Window("RP-Pico-Door-Tab-Close editor", layout, resizable=False, element_justification="center") #main window

while True:
    if Buttonstate == 1:    # resets the GO button to amber
        time.sleep(1) 
        window.find_element("GO").Update("GO", button_color=("black", "LightGoldenrod1"))
    if Buttonstate == 2:
        time.sleep(1)
        window.find_element("ADD").Update("Add combination", button_color=("black", "LightGoldenrod1"))
    event, values = window.read()
    time.sleep(0.1)
    if event == "GO":
        if combinations:    # writes code.py files
            code.append("distancedoor = {}".format(values["Distance"]))
            code.append("while True:\n    while resetstate == 1:\n        time.sleep(0.4)\n        try:\n            distance = sonar.distance\n            while distance < 10:\n                time.sleep(0.5)\n                distance = sonar.distance\n            distancemed = (distance + distanceold) / 2\n            if distancemed < distancedoor:")    #second part of code.py
            code.extend(combinations)
            code.append("                resetstate = 0\n                led.value = False\n            distanceold = distance\n        except RuntimeError:\n            distance = 55\n    while resetstate == 0:\n        time.sleep(0.1)\n        if reset.value:\n            for i in range(8):\n                led.value = True\n                time.sleep(0.5)\n                led.value = False\n                time.sleep(0.5)\n            led.value = True\n            resetstate = 1\n            distance = distancedoor + 5\n            distanceold = distancedoor + 5")
            codestr = "\n".join(code)
            script.write(codestr)
            script.close()
            window.find_element("GO").Update("Done!", button_color=("black", "green"))
        else:   # if combinations list is empty, this will make the button red
            window.find_element("GO").Update("No Combinations added!", button_color=("black", "red"))
            Buttonstate = 1
    if event == "ADD":  # adds combinations from input texbox to combinations list
        window.find_element("ADD").Update("added Combination", button_color=("black", "green")) # confirms that the combination was added to list
        combinations.append("                keyboard.send({})\n                time.sleep({})".format(values["KEYS"], int(values["Delay"]) / 1000))
        window.find_element("Keycombinations").Update("{}".format("\n".join(combinations)))
        Buttonstate = 2
    if event == "REMOVE":   # removes last entry from combinations list
        combinations.pop()
        window.find_element("Keycombinations").Update("{}".format("\n".join(combinations)))
    if event == "Github":   # opens github page
        webbrowser.open("https://github.com/HeyJoFlyer/RP-Pico-Door-Keyboard-Input")
    if event == sg.WIN_CLOSED: #closes window
        script.close() #cloes code.py
        read_file = open("code.py", "r") # opens code.py as read
        char = read_file.read(1) # first character of code.py 
        if not char: # deletes code.py if empty
            os.remove("code.py")
        break # closes window
    window.refresh() #refreshes the window to change the button color
