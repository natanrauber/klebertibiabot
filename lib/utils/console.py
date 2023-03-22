import os

from lib.utils.colors import Colors
from lib.utils.datetime import dateTime


class Console:
    """
    A utility class for console-related functionality.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    _last_msg = ''

    @staticmethod
    def log(msg: str, color: str = Colors.default) -> None:
        """
        Logs a message with a timestamp and an optional color.

        Args:
            msg (str): The message to log.
            color (str, optional): The color to use for the message. Defaults to Colors.default.

        Returns:
            None
        """
        if msg == Console._last_msg:
            return
        Console._last_msg = msg
        print(f'[{dateTime()}] {color}{msg}{Colors.default}')

    @staticmethod
    def clear() -> None:
        """
        Clears the console screen.

        Returns:
            None
        """
        os.system("cls")
