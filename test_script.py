import time

from keyboard import *

def print_hello():
    print("Hello!")

def print_dot():
    time.sleep(0.1)
    print(".")

def print_goodbye():
    print("Goodbye!")

keyboard_controls.add_press_action("a", print_hello)
keyboard_controls.add_release_action("a", print_goodbye)
keyboard_controls.add_hold_action("a", print_dot)

keyboard_controls.add_press_action("b", print_goodbye)
keyboard_controls.add_release_action("b", print_hello)
keyboard_controls.add_hold_action("b", print_dot)


keyboard_controls.go()


