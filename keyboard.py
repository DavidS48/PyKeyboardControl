from threading import Thread

from inputs import get_key


key_states = {}

class Key:
    def __init__(self,
                 code,
                 on_pressed = None,
                 while_held = None,
                 when_released = None):
        self.code = code
        self.on_pressed = on_pressed
        self.while_held = while_held
        self.when_released = when_released
        self.current_state = 0

    def check_state(self):
        updates = key_states.get(self.code, [])
        try:
            while True:
                new_state = updates.pop()
                if new_state in [1, 2] and self.current_state == 0:
                    self.current_state = new_state
                    self.start_actions()
                elif new_state == 0 and self.current_state in [1, 2]:
                    self.current_state = new_state
                    self.finish_actions()
        except IndexError:
            pass
   
    def finish_actions(self):
        if self.when_released:
            self.when_released()
 
    def start_actions(self):
        if self.on_pressed:
            on_pressed_thread = Thread(target = self.on_pressed)
            on_pressed_thread.start()
        if self.while_held:
            def repeat_while_held():
                while self.current_state != 0:
                    self.while_held()
            while_held_thread = Thread(target = repeat_while_held)
            while_held_thread.start()

class Keyboard:
    def __init__(self):
        self.keys = {}

    def add_press_action(self, key_name, action):
        key_code = "KEY_" + key_name.upper()
        try:
            self.keys[key_code].on_pressed = action
        except KeyError:
            self.keys[key_code] = Key(key_code, on_pressed = action)
        key_states[key_code] = []

    def add_hold_action(self, key_name, action):
        key_code = "KEY_" + key_name.upper()
        try:
            self.keys[key_code].while_held = action
        except KeyError:
            self.keys[key_code] = Key(key_code, while_held = action)
        key_states[key_code] = []

    def add_release_action(self, key_name, action):
        key_code = "KEY_" + key_name.upper()
        try:
            self.keys[key_code].when_released = action
        except KeyError:
            self.keys[key_code] = Key(key_code, when_released = action)
        key_states[key_code] = []


    def update_state(self):
        events = get_key()
        for event in events:
            if event.ev_type == "Key":
                try:
                    key_states[event.code].append(event.state)
                except KeyError:
                    pass

    def go(self):
        while True:
            self.update_state()
            for key in self.keys.values():
                key.check_state()

keyboard_controls = Keyboard()

###########################

import time

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


