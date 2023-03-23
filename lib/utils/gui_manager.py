import threading
import tkinter as tk
from tkinter import ttk

from lib.utils.status import Status
from main_loop import main_loop


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
        status_separator (ttk.Separator): The separator between the buttons and the status label.
        status_frame (ttk.Frame): The frame containing the status label.
        status_label (ttk.Label): The label displaying the current status of the main loop.

    Methods:
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
            self.buttons_frame, text="Pause", command=self.pause, state=tk.DISABLED, style="Custom.TButton")
        self.buttons_separator = ttk.Separator(
            self.buttons_frame, orient=tk.VERTICAL)
        self.resume_button = ttk.Button(
            self.buttons_frame, text="Resume", command=self.resume, state=tk.NORMAL, style="Custom.TButton")
        self.status_separator = ttk.Separator(self.frame)
        self.status_frame = ttk.Frame(self.frame, style="Custom.TFrame")
        self.status_label = ttk.Label(
            self.status_frame, text="Paused", style="Custom.TLabel", foreground="red")

    def pause(self):
        """
        Pauses the main loop and updates the GUI accordingly.
        """
        Status.pause()  # stops the "main_loop", consequently the "loop_thread" is terminated
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)
        self.status_label.config(text="Paused", foreground="red")

    def resume(self):
        """
        Resumes the main loop and updates the GUI accordingly.
        """
        Status.resume()
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)
        self.status_label.config(text="Running", foreground="green")
        loop_thread = threading.Thread(
            target=main_loop)  # create a "loop_thread" thread to run "main_loop"
        loop_thread.start()  # start the "loop_thread"

    def configure_widgets(self):
        """
        Configures the style and layout of the widgets in the GUI.
        """
        style = ttk.Style()

        # Define custom style for buttons
        style.configure("Custom.TButton", foreground="#333", font=(
            "Helvetica", 12), padding=10, width=15, borderwidth=0, bordercolor="#333", borderRadius=11)

        # Define custom style for labels
        style.configure("Custom.TLabel", foreground="#333",
                        font=("Helvetica", 14), padding=5)

        # Define custom style for disabled buttons
        style.map("Custom.TButton", foreground=[('disabled', '#ccc')])

        self.rootWindow.title("Kleber")
        self.rootWindow.resizable(False, False)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.buttons_frame.pack(side=tk.TOP)
        self.pause_button.pack(side=tk.LEFT)
        self.buttons_separator.pack(side=tk.LEFT, padx=5, fill=tk.Y)
        self.resume_button.pack(side=tk.LEFT)
        self.status_separator.pack(side=tk.TOP, pady=10, fill=tk.X)
        self.status_frame.pack(side=tk.TOP)
        self.status_label.pack()

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
