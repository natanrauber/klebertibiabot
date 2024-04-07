import datetime as dt
import os
import threading
import tkinter as tk
from tkinter import ttk

from lib.main_loop import main_loop
from lib.uid import uid
from lib.utils.console import Console
from lib.utils.status import Status


class GUIManager:
    """
    A class for managing the GUI of the Kleber application.

    Attributes:
        rootWindow (Tk): The root window of the GUI.
        frame (ttk.Frame): The frame of the GUI.
        buttons_frame (ttk.Frame): The frame containing the pause and resume buttons.
        pause_button (ttk.Button): The button to pause the main loop.
        buttons_separator (ttk.Separator): The separator between the pause and resume buttons.
        resume_button (ttk.Button): The button to resume the main loop.
        console (Console): The console widget for displaying logs.

    Methods:
        close(): Close the window and quit the application
        pause(): Pauses the main loop and updates the GUI accordingly.
        resume(): Resumes the main loop and updates the GUI accordingly.
        configure_widgets(): Configures the styles and layout of the GUI widgets.
        start(): Starts the GUI loop.

    Usage:
        To start the GUI, create an instance of this class and call its "start" method:
        gui_manager = GUIManager()
        gui_manager.start()

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    def __init__(self):
        """
        Initializes a new instance of the GUIManager class.
        """
        self.rootWindow = tk.Tk()
        self.frame = ttk.Frame(self.rootWindow, style="Custom.TFrame")
        self.buttons_frame = ttk.Frame(self.frame, style="Custom.TFrame")
        self.pause_button = ttk.Button(
            self.buttons_frame,
            text="Paused",
            command=self.pause,
            state=tk.DISABLED,
            style="Pause.TButton",
        )
        self.buttons_separator = ttk.Frame(
            self.buttons_frame, height=8, width=8, style="Custom.TFrame"
        )
        self.resume_button = ttk.Button(
            self.buttons_frame,
            text="Resume",
            command=self.resume,
            state=tk.NORMAL,
            style="Resume.TButton",
        )
        self.console_separator = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.console = Console(self.frame)

        # Schedule the close method to be called at the next 6 AM
        now = dt.datetime.now()
        next_6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now >= next_6am:
            next_6am += dt.timedelta(days=1)
        time_to_wait = (next_6am - now).total_seconds() * 1000
        self.rootWindow.after(int(time_to_wait), self.close)

    def close(self):
        """
        Close the window and quit the application
        """
        self.pause()
        self.rootWindow.destroy()
        self.rootWindow.quit()

    def pause(self):
        """
        Pauses the main loop and updates the GUI accordingly.
        """
        self.rootWindow.focus()
        Status.pause()  # stops the "main_loop", consequently the "loop_thread" is terminated
        self.pause_button.config(state=tk.DISABLED, text="Paused")
        self.resume_button.config(state=tk.NORMAL, text="Resume")

    def resume(self):
        """
        Resumes the main loop and updates the GUI accordingly.
        """
        self.rootWindow.focus()
        Status.resume()
        self.rootWindow.focus()
        self.pause_button.config(state=tk.NORMAL, text="Pause")
        self.resume_button.config(state=tk.DISABLED, text="Running")
        loop_thread = threading.Thread(
            target=main_loop
        )  # create a "loop_thread" thread to run "main_loop"
        loop_thread.start()  # start the "loop_thread"

    def configure_widgets(self):
        """
        Configures the style and layout of the widgets in the GUI.
        """
        style = ttk.Style(self.rootWindow)

        style.configure("Custom.TFrame", background="#F9F9F9")

        # Define custom style for buttons
        style.configure(
            "Pause.TButton",
            background="#F9F9F9",
            foreground="#333",
            padding=5,
            width=10,
            borderRadius=11,
        )
        style.configure(
            "Resume.TButton",
            background="#F9F9F9",
            foreground="#333",
            padding=5,
            width=10,
            borderRadius=11,
        )

        # Define custom style for disabled buttons
        style.map("Pause.TButton", foreground=[("disabled", "red")])
        style.map("Resume.TButton", foreground=[("disabled", "green")])

        self.rootWindow.title(uid)
        self.rootWindow.geometry("668x157")
        self.rootWindow.configure(bg="#F9F9F9")
        self.rootWindow.resizable(False, False)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.buttons_frame.pack()
        self.pause_button.pack(side=tk.LEFT)
        self.buttons_separator.pack(side=tk.LEFT)
        self.resume_button.pack(side=tk.LEFT)
        self.console_separator.pack()
        self.console.pack(fill="both")

    def start(self):
        """
        Starts the Graphical User Interface.
        """
        self.configure_widgets()
        self.rootWindow.mainloop()


"""
This piece of code checks if the module is being executed as the main program, and if so, it creates an instance of the GUIManager class and calls its start() method to start the graphical user interface (GUI) of the Kleber application. If this module is imported as a module in another program, this code block will not be executed.
"""
if __name__ == "__main__":
    gui_manager = GUIManager()
    gui_manager.start()
