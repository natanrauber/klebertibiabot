from pynput.keyboard import Controller, Key


class Keyboard:
    """
    A class for simulating keyboard input.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    @staticmethod
    def press(key: Key) -> None:
        """
        Presses a key.

        Args:
            key (Key): The key to press.
        """
        Controller().tap(key)

    @staticmethod
    def hold(key: Key) -> None:
        """
        Holds a key down.

        Args:
            key (Key): The key to hold down.
        """
        Controller().press(key)

    @staticmethod
    def release(key: Key) -> None:
        """
        Releases a key.

        Args:
            key (Key): The key to release.
        """
        Controller().release(key)
