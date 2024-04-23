import datetime as dt
import threading
import tkinter as tk
from ctypes import byref, c_int, sizeof, windll
from tkinter import ttk

import lib.config as cfg
from lib.actions.attack.attack import *
from lib.actions.clean.clean import locateDropContainer
from lib.actions.heal.heal import setupHeal
from lib.actions.loot.loot import locateScreenCenter
from lib.actions.walk.walk import getHuntList, setHunt, setupWalk
from lib.main_loop import main_loop
from lib.uid import uid
from lib.utils.console import Console
from lib.utils.folder_manager import FolderManager
from lib.utils.status import Status


def toggleAttack():
    if cfg.getAttack() == True:
        cfg.setAttack(False)
        disable_attack()
        FolderManager.delete_file(f"{cfg.SESSION_DIR}/battle.png")
    else:
        cfg.setAttack(True)
        enable_attack()
        setupAttack()
    Console.log(f"Attack: {cfg.getAttack()}")


def toggleHeal():
    if cfg.getHeal() == True:
        cfg.setHeal(False)
    else:
        cfg.setHeal(True)
        setupHeal()
    Console.log(f"Heal: {cfg.getHeal()}")


def toggleWalk():
    if cfg.getWalk() == True:
        cfg.setWalk(False)
    else:
        cfg.setWalk(True)
        setupWalk()
    Console.log(f"Walk: {cfg.getWalk()}")


def toggleLoot():
    if cfg.getLoot() == True:
        cfg.setLoot(False)
    else:
        cfg.setLoot(True)
        if cfg.getDrop() == False:
            locateScreenCenter()
    Console.log(f"Loot: {cfg.getLoot()}")


def toggleEat():
    if cfg.getEat():
        cfg.setEat(False)
    else:
        cfg.setEat(True)
        if cfg.getDrop() == False:
            locateDropContainer()
    Console.log(f"Eat: {cfg.getEat()}")


def toggleDrop():
    if cfg.getDrop():
        cfg.setDrop(False)
    else:
        cfg.setDrop(True)
        if cfg.getEat() == False:
            locateDropContainer()
        if cfg.getLoot() == False:
            locateScreenCenter()
    Console.log(f"Drop: {cfg.getDrop()}")


def toggleProjector():
    if cfg.getProjector():
        cfg.setProjector(False)
    else:
        cfg.setProjector(True)
    Console.log(f"Projector: {cfg.getProjector()}")


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
        button_pause (ttk.Button): The button to pause the main loop.
        buttons_separator (ttk.Separator): The separator between the pause and resume buttons.
        button_resume (ttk.Button): The button to resume the main loop.
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
        self.button_resume = ttk.Button(
            self.buttons_frame,
            text="Resume",
            command=self.resume,
            state=tk.NORMAL,
            style="Resume.TButton",
        )
        self.button_separator1 = ttk.Frame(
            self.buttons_frame, height=8, width=13, style="Custom.TFrame"
        )
        self.button_pause = ttk.Button(
            self.buttons_frame,
            text="Paused",
            command=self.pause,
            state=tk.DISABLED,
            style="Pause.TButton",
        )
        self.button_separator2 = ttk.Frame(
            self.buttons_frame, height=8, width=13, style="Custom.TFrame"
        )
        self.button_refresh = ttk.Button(
            self.buttons_frame,
            text="Refresh",
            command=self.refresh,
            state=tk.NORMAL,
            style="Refresh.TButton",
        )
        self.option_vars = []
        for i in range(7):
            option_var = tk.BooleanVar()
            option_var.set(False)
            self.option_vars.append(option_var)
        self.checkbox_separator1 = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.checkbox_frame1 = ttk.Frame(self.frame, style="Custom.TFrame")
        self.checkbox_attack = ttk.Checkbutton(
            self.checkbox_frame1,
            text=f"Attack",
            variable=self.option_vars[0],
            style="Custom.TCheckbutton",
            command=toggleAttack,
        )
        self.checkbox_heal = ttk.Checkbutton(
            self.checkbox_frame1,
            text=f"Heal",
            variable=self.option_vars[1],
            style="Custom.TCheckbutton",
            command=toggleHeal,
        )
        self.checkbox_walk = ttk.Checkbutton(
            self.checkbox_frame1,
            text=f"Walk",
            variable=self.option_vars[2],
            style="Custom.TCheckbutton",
            command=toggleWalk,
        )
        self.checkbox_loot = ttk.Checkbutton(
            self.checkbox_frame1,
            text=f"Loot",
            variable=self.option_vars[3],
            style="Custom.TCheckbutton",
            command=toggleLoot,
        )
        self.checkbox_separator2 = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.checkbox_frame2 = ttk.Frame(self.frame, style="Custom.TFrame")
        self.checkbox_eat = ttk.Checkbutton(
            self.checkbox_frame2,
            text=f"Eat",
            variable=self.option_vars[4],
            style="Custom.TCheckbutton",
            command=toggleEat,
        )
        self.checkbox_drop = ttk.Checkbutton(
            self.checkbox_frame2,
            text=f"Drop",
            variable=self.option_vars[5],
            style="Custom.TCheckbutton",
            command=toggleDrop,
        )
        self.checkbox_projector = ttk.Checkbutton(
            self.checkbox_frame2,
            text=f"Projector",
            variable=self.option_vars[6],
            style="Custom.TCheckbutton",
            command=toggleProjector,
        )
        selected_hunt = tk.StringVar(self.frame)
        selected_hunt.set(getHuntList()[1])
        selectHunt(getHuntList()[1])
        self.dropdown_separator = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.dropdown = ttk.OptionMenu(
            self.frame,
            selected_hunt,
            *getHuntList(),
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
        self.pause()
        self.rootWindow.destroy()
        self.rootWindow.quit()

    def resume(self):
        self.rootWindow.focus()
        Status.resume()
        self.rootWindow.focus()
        self.button_pause.config(state=tk.NORMAL, text="Pause")
        self.button_resume.config(state=tk.DISABLED, text="Running")
        loop_thread = threading.Thread(
            target=main_loop
        )  # create a "loop_thread" thread to run "main_loop"
        loop_thread.start()  # start the "loop_thread"

    def pause(self):
        self.rootWindow.focus()
        Status.pause()  # stops the "main_loop", consequently the "loop_thread" is terminated
        self.button_pause.config(state=tk.DISABLED, text="Paused")
        self.button_resume.config(state=tk.NORMAL, text="Resume")

    def refresh(self):
        self.rootWindow.focus()
        if not Status.is_paused():
            self.pause()  # stops the "main_loop", consequently the "loop_thread" is terminated
        if getAttack():
            setupAttack()
        if getHeal():
            setupHeal()
        if getWalk():
            setupWalk()
        if getLoot() or getDrop():
            locateScreenCenter()
        if getEat() or getDrop():
            locateDropContainer()
        Console.log("Refresh complete")

        self.button_pause.config(state=tk.DISABLED, text="Paused")
        self.button_resume.config(state=tk.NORMAL, text="Resume")

    def configure_widgets(self):
        """
        Configures the style and layout of the widgets in the GUI.
        """
        style = ttk.Style(self.rootWindow)
        # style.theme_use('clam')
        style.configure("Custom.TFrame", background="#f9f9f9")
        style.configure(
            "Pause.TButton",
            padding=5,
            width=13,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.map("Pause.TButton", foreground=[("disabled", "red")])
        style.configure(
            "Resume.TButton",
            padding=5,
            width=13,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.map("Resume.TButton", foreground=[("disabled", "green")])
        style.configure(
            "Refresh.TButton",
            padding=5,
            width=13,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.configure(
            "Custom.TCheckbutton",
            background="#f9f9f9",
            width=8,
        )

        self.rootWindow.title(uid)
        self.rootWindow.geometry("334x300")
        self.rootWindow.configure(bg="#f9f9f9")
        self.rootWindow.resizable(False, False)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.buttons_frame.pack()
        self.button_resume.pack(side=tk.LEFT)
        self.button_separator1.pack(side=tk.LEFT)
        self.button_pause.pack(side=tk.LEFT)
        self.button_separator2.pack(side=tk.LEFT)
        self.button_refresh.pack(side=tk.LEFT)
        self.checkbox_separator1.pack()
        self.checkbox_frame1.pack(fill=tk.BOTH, expand=True)
        self.checkbox_attack.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_heal.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_walk.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_loot.pack(side=tk.LEFT, padx=(0, 0))
        self.checkbox_separator2.pack()
        self.checkbox_frame2.pack(fill=tk.BOTH, expand=True)
        self.checkbox_eat.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_drop.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_projector.pack(side=tk.LEFT, padx=(0, 0))
        self.dropdown_separator.pack()
        self.dropdown.pack()
        self.console_separator.pack()
        self.console.pack(fill=tk.BOTH)

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
