import os
import sys
import tkinter as tk

from lib.utils.colors import Colors
from lib.utils.datetime import dateTime


class Console(tk.Frame):
    """
    A class for creating a console window.

    Attributes:
        text (Text): The tkinter Text widget where console messages are displayed.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    def __init__(self, master=None, **kw):
        """
        Initializes the console window.

        Args:
            master (Optional[Tk]): The tkinter master window. Defaults to None.
            **kw: Additional keyword arguments to pass to the tkinter Frame.
        """
        tk.Frame.__init__(self, master=master, **kw)
        self.text = tk.Text(self, wrap="word", bg="#F9F9F9")
        self.text.pack(side="left", fill="both", expand=True)
        sys.stdout = self
        sys.stderr = self

    def write(self, message):
        """
        Writes a message to the console.

        Args:
            message (str): The message to write.
        """
        self.text.insert("end", message)
        self.text.see("end")

    def flush(self):
        """
        Does nothing. Required for compatibility with sys.stdout and sys.stderr.
        """
        pass

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
        print(f'[{dateTime()}] {msg}')

    @staticmethod
    def clear() -> None:
        """
        Clears the console screen.

        Returns:
            None
        """
        os.system("cls")
