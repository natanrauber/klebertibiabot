import keyboard
from pynput.keyboard import Controller, Key as KEY

Key = KEY


class Keyboard:
    def isPressed(key):
        return keyboard.is_pressed(key)

    def press(key: Key):
        return Controller().tap(key)

    def hold(key: Key):
        return Controller().press(key)

    def release(key: Key):
        return Controller().release(key)
