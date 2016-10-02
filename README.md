# PyKeyboardControl
Simple module for attaching python functions to keystrokes.

This module was inspired by a sprint at PyCon UK 2016, which attempted to create a module to allow Code Club students to trigger Python code with keypresses while playing Minecraft: Pi Edition.

The actual outcome of that sprint was Superkeys:
https://github.com/martinohanlon/superkeys
but I was left wondering whether another approach would also work.

This module is the other approach.

The really clever stuff is done by Zeth's Inputs library. The stuff for reading in key presses is cribbed from superkeys. The rest is basically a noddy event loop wrapped around that.
