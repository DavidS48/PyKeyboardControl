import time
from keyboard import *

# Write some functions:

def print_hello():
    print("Hello!")

def print_dot():
    print(".")
    time.sleep(0.1)

def print_goodbye():
    print("Goodbye!")

# Attach them to keys...

# One to be run once when "a" is pressed:
keyboard_controls.add_press_action("a", print_hello)
# One to be repeated for as long as "a" is held:
keyboard_controls.add_hold_action("a", print_dot)
# And one to be run once when "a" is released again:
keyboard_controls.add_release_action("a", print_goodbye)

# Then go!
keyboard_controls.go()


