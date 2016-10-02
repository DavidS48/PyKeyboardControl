from threading import Thread

from inputs import get_key


key_states = {}

class Key:
    """
    Holds the current state of an individual key, and any actions attached to
    it.
    """

    def __init__(self,
                 code,
                 on_pressed = None,
                 while_held = None,
                 when_released = None):
        """
        code is the key code, as in the inputs library. This will be, eg, KEY_A
        for the "a" key and so on.
        """
        self.code = code
        self.on_pressed = on_pressed
        self.while_held = while_held
        self.when_released = when_released
        self.current_state = 0

    def check_state(self):
        """
        Check for changes to the state of this key in key_states, and kick off
        any behaviour associated with them.
        """
        updates = key_states.get(self.code, [])
        try:
            while True:
                new_state = updates.pop()
                if new_state in [1, 2] and self.current_state == 0:
                    self.current_state = new_state
                    self._start_actions()
                elif new_state == 0 and self.current_state in [1, 2]:
                    self.current_state = new_state
                    self._finish_actions()
        except IndexError:
            pass
   
    def _finish_actions(self):
        if self.when_released:
            when_released_thread = Thread(target = self.when_released)
            when_released_thread.start()
 
    def _start_actions(self):
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
        """
        Add an action to be triggered when the given key is pressed.

	The key name should be a letter, and is case insensitive. The action
        should be a function taking no arguments.
        """
        key_code = "KEY_" + key_name.upper()
        try:
            self.keys[key_code].on_pressed = action
        except KeyError:
            self.keys[key_code] = Key(key_code, on_pressed = action)
        key_states[key_code] = []

    def add_hold_action(self, key_name, action):
        """
        Add an action to be run repeatedly while the given key is heldd.

	The key name should be a letter, and is case insensitive. The action
        should be a function taking no arguments.
        """

        key_code = "KEY_" + key_name.upper()
        try:
            self.keys[key_code].while_held = action
        except KeyError:
            self.keys[key_code] = Key(key_code, while_held = action)
        key_states[key_code] = []

    def add_release_action(self, key_name, action):
        """
        Add an action to be triggered when the given key is released.

	The key name should be a letter, and is case insensitive. The action
        should be a function taking no arguments.
        """
        key_code = "KEY_" + key_name.upper()
        try:
            self.keys[key_code].when_released = action
        except KeyError:
            self.keys[key_code] = Key(key_code, when_released = action)
        key_states[key_code] = []


    def _update_state_store(self):
        events = get_key()
        for event in events:
            if event.ev_type == "Key":
                try:
                    key_states[event.code].append(event.state)
                except KeyError:
                    pass

    def go(self):
        """
        Wait for key presses and act on them when they happen.
        """
        while True:
            self._update_state_store()
            for key in self.keys.values():
                key.check_state()

# Pre-instantiate a Keyboard for zero-boilerplate use.
keyboard_controls = Keyboard()


