import threading
import tkinter as tk
from tkinter import ttk

from lib.utils.status import pause
from main_loop import loop

rootWindow = tk.Tk()
rootWindow.title("Kleber")
rootWindow.resizable(False, False)  # Disable window resizing


def callPauseButton():
    pause(True)
    pause_button.config(state=tk.DISABLED)
    resume_button.config(state=tk.NORMAL)
    status_label.config(text="Paused", foreground="red")


def callResumeButton():
    pause(False)
    pause_button.config(state=tk.NORMAL)
    resume_button.config(state=tk.DISABLED)
    status_label.config(text="Running", foreground="green")
    loop_thread = threading.Thread(target=loop)
    loop_thread.start()


style = ttk.Style()


# Define custom style for buttons
style.configure("Custom.TButton",
                foreground="#333", font=("Helvetica", 12), padding=10, width=15, borderwidth=0,
                bordercolor="#333",  borderRadius=11)


# Define custom style for labels
style.configure("Custom.TLabel", foreground="#333",
                font=("Helvetica", 14), padding=5)

# Define custom style for disabled buttons
style.map("Custom.TButton", foreground=[('disabled', '#ccc')])

frame = ttk.Frame(rootWindow)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

buttons_frame = ttk.Frame(frame)
buttons_frame.pack(side=tk.TOP)

pause_button = ttk.Button(buttons_frame, text="Pause",
                          command=callPauseButton, style="Custom.TButton")
pause_button.pack(side=tk.LEFT)

buttons_separator = ttk.Separator(buttons_frame, orient=tk.VERTICAL)
buttons_separator.pack(side=tk.LEFT, padx=5, fill=tk.Y)

resume_button = ttk.Button(
    buttons_frame, text="Resume", command=callResumeButton, state=tk.DISABLED, style="Custom.TButton")
resume_button.pack(side=tk.LEFT)

status_separator = ttk.Separator(frame)
status_separator.pack(side=tk.TOP, pady=10, fill=tk.X)


status_frame = ttk.Frame(frame)
status_frame.pack(side=tk.TOP)

status_label = ttk.Label(status_frame, text="Running",
                         style="Custom.TLabel", foreground="green")
status_label.pack()
