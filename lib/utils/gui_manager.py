import datetime as dt
import threading
import tkinter as tk
from ctypes import byref, c_int, sizeof, windll
from os import listdir
from os.path import isfile, join
from tkinter import ttk

import lib.config as cfg
from lib.actions.attack.attack import *
from lib.actions.clean.clean import setupDrop
from lib.actions.heal.heal import setupHeal
from lib.actions.walk.walk import HUNT_LIST, setHunt, setupWalk
from lib.main_loop import main_loop
from lib.uid import uid
from lib.utils.console import Console
from lib.utils.folder_manager import FolderManager
from lib.utils.status import Status


def toggleAttack():
    if cfg.ATTACK == True:
        cfg.setAttack(False)
        disable_attack()
        FolderManager.delete_file(f"{cfg.SESSION_DIR}/battle.png")
    else:
        cfg.setAttack(True)
        enable_attack()
        setupAttack()
    Console.log(f"Attack: {cfg.ATTACK}")


def toggleHeal():
    if cfg.HEAL == True:
        cfg.setHeal(False)
    else:
        cfg.setHeal(True)
        setupHeal()
    Console.log(f"Heal: {cfg.HEAL}")


def toggleWalk():
    if cfg.WALK == True:
        cfg.setWalk(False)
        FolderManager.delete_file(f"{cfg.SESSION_DIR}/map.png")
    else:
        cfg.setWalk(True)
        setupWalk()
    Console.log(f"Walk: {cfg.WALK}")


def toggleEat():
    if cfg.EAT:
        cfg.setEat(False)
        if cfg.DROP == False:
            folder_path = cfg.SESSION_DIR
            for file_name in os.listdir(folder_path):
                if "container" in file_name:
                    os.remove(os.path.join(folder_path, file_name))
    else:
        cfg.setEat(True)
        if cfg.DROP == False:
            setupDrop()
    Console.log(f"Eat: {cfg.DROP}")


def toggleDrop():
    if cfg.DROP:
        cfg.setDrop(False)
        if cfg.EAT == False:
            folder_path = cfg.SESSION_DIR
            for file_name in os.listdir(folder_path):
                if "container" in file_name:
                    os.remove(os.path.join(folder_path, file_name))
    else:
        cfg.setDrop(True)
        if cfg.EAT == False:
            setupDrop()
    Console.log(f"Drop: {cfg.DROP}")


def selectHunt(value):
    setHunt(value)
    Console.log(f"Selected hunt: {value}")


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
        option_vars (list): List to hold the variables for the checkboxes.

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
        self.checkbox_separator = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.option_vars = []
        for i in range(6):
            option_var = tk.BooleanVar()
            option_var.set(False)
            self.option_vars.append(option_var)
        self.checkbox_frame = ttk.Frame(self.frame, style="Custom.TFrame")
        self.checkbox_attack = ttk.Checkbutton(
            self.checkbox_frame,
            text=f"Attack",
            variable=self.option_vars[0],
            style="Custom.TCheckbutton",
            command=toggleAttack,
        )
        self.checkbox_heal = ttk.Checkbutton(
            self.checkbox_frame,
            text=f"Heal",
            variable=self.option_vars[1],
            style="Custom.TCheckbutton",
            command=toggleHeal,
        )
        self.checkbox_walk = ttk.Checkbutton(
            self.checkbox_frame,
            text=f"Walk",
            variable=self.option_vars[2],
            style="Custom.TCheckbutton",
            command=toggleWalk,
        )
        self.checkbox_loot = ttk.Checkbutton(
            self.checkbox_frame,
            text=f"Loot",
            variable=self.option_vars[3],
            style="Custom.TCheckbutton",
            # command=toggleLoot,
        )
        self.checkbox_eat = ttk.Checkbutton(
            self.checkbox_frame,
            text=f"Eat",
            variable=self.option_vars[4],
            style="Custom.TCheckbutton",
            command=toggleEat,
        )
        self.checkbox_drop = ttk.Checkbutton(
            self.checkbox_frame,
            text=f"Drop",
            variable=self.option_vars[5],
            style="Custom.TCheckbutton",
            command=toggleDrop,
        )
        self.dropdown_separator = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        selected_hunt = tk.StringVar(self.frame)
        selected_hunt.set(HUNT_LIST[0])
        self.dropdown = tk.OptionMenu(
            self.frame,
            selected_hunt,
            *HUNT_LIST,
            command=selectHunt,
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
        style.configure("Custom.TFrame", background="#f9f9f9")
        style.configure(
            "Pause.TButton",
            padding=5,
            width=10,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.map("Pause.TButton", foreground=[("disabled", "red")])
        style.configure(
            "Resume.TButton",
            padding=5,
            width=10,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.map("Resume.TButton", foreground=[("disabled", "green")])
        style.configure(
            "Custom.TCheckbutton",
            padding=10,
            background="#f9f9f9",
        )

        self.rootWindow.title(uid)
        self.rootWindow.geometry("668x200")
        self.rootWindow.configure(bg="#f9f9f9")
        self.rootWindow.resizable(False, False)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.buttons_frame.pack()
        self.pause_button.pack(side=tk.LEFT)
        self.buttons_separator.pack(side=tk.LEFT)
        self.resume_button.pack(side=tk.LEFT)
        self.checkbox_separator.pack()
        self.checkbox_frame.pack()
        self.checkbox_attack.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_heal.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_walk.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_loot.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_eat.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_drop.pack(side=tk.LEFT, padx=(0, 10))
        self.dropdown_separator.pack()
        self.dropdown.pack()
        self.console_separator.pack()
        self.console.pack(fill="both")

        HWND = windll.user32.GetParent(self.rootWindow.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 35, byref(c_int(0x00140E0C)), sizeof(c_int)
        )
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 36, byref(c_int(0x00FFFFFF)), sizeof(c_int)
        )
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 34, byref(c_int(0x00312C8D)), sizeof(c_int)
        )

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
