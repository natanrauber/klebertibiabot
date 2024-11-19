from pynput.keyboard import Controller, Key, KeyCode

from lib.utils.window_manager import WindowManager


class Keyboard:

    @staticmethod
    def press(key: Key | KeyCode) -> None:
        WindowManager.activate("Tibia -")
        Controller().tap(key)

    @staticmethod
    def hold(key: Key | KeyCode) -> None:
        WindowManager.activate("Tibia -")
        Controller().press(key)

    @staticmethod
    def release(key: Key | KeyCode) -> None:
        WindowManager.activate("Tibia -")
        Controller().release(key)
