import time

from keyboard import *

def print_hello():
    time.sleep(1)
    print("Hello!")

def print_goodbye():
    print("Goodbye!")

keyboard_controls.add_press_action("a", print_hello)
keyboard_controls.add_press_action("b", print_goodbye)
keyboard_controls.add_hold_action("b", print_hello)
keyboard_controls.add_release_action("c", print_goodbye)

keyboard.go()


