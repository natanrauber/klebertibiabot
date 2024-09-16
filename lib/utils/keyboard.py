from pynput.keyboard import Controller, Key, KeyCode


class Keyboard:

    @staticmethod
    def press(key: Key | KeyCode) -> None:
        Controller().tap(key)

    @staticmethod
    def hold(key: Key | KeyCode) -> None:
        Controller().press(key)

    @staticmethod
    def release(key: Key | KeyCode) -> None:
        Controller().release(key)
