from pynput.keyboard import Controller, Key


class Keyboard:

    @staticmethod
    def press(key: Key) -> None:
        Controller().tap(key)

    @staticmethod
    def hold(key: Key) -> None:
        Controller().press(key)

    @staticmethod
    def release(key: Key) -> None:
        Controller().release(key)
