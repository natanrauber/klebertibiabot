import sys
import tkinter as tk
from tkinter import ttk

from lib.utils.datetime import dateTime


class Console(ttk.Frame):

    def __init__(self, master: ttk.Frame):
        ttk.Frame.__init__(self, master=master)
        self.text = tk.Text(self, wrap="word", bg="#F9F9F9")
        self.text.pack(side="left", fill="both", expand=True)
        sys.stdout = self
        sys.stderr = self

    def write(self, message: str):
        self.text.insert("end", message)
        self.text.see("end")

    def flush(self):
        """
        Does nothing.
        Required for compatibility with sys.stdout and sys.stderr.
        """
        pass

    _last_msg = ""

    @staticmethod
    def log(msg: str) -> None:
        if msg == Console._last_msg:
            return
        Console._last_msg = msg
        print(f"[{dateTime()}] {msg}")
