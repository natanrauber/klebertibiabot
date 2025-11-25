import datetime as dt
import threading
import tkinter as tk
from ctypes import byref, c_int, sizeof, windll
from tkinter import StringVar, ttk

from lib.config import (
    FOOD_KEY,
    HASTE_KEY,
    HEAL_KEY,
    RING_KEY,
    STRIKE_KEY,
    UTURA_KEY,
    Config,
)
from lib.main_loop import main_loop
from lib.modules.attack import disable_attack, enable_attack, setupAttack
from lib.modules.walk import getHuntList, setHunt
from lib.uid import uid
from lib.utils.console import Console
from lib.utils.dir import Dir
from lib.utils.folder_manager import FolderManager
from lib.utils.interface import GameUI
from lib.utils.status import Status


class GUIManager:

    def __init__(self):
        # root
        self.rootWindow = tk.Tk()
        self.rootWindow.attributes(  # type: ignore
            "-topmost",
            not self.rootWindow.attributes("-topmost"),  # type: ignore
        )
        self.frame = ttk.Frame(self.rootWindow, style="Custom.TFrame")
        self.buttons_frame = ttk.Frame(self.frame, style="Custom.TFrame")
        self.button_resume = ttk.Button(
            self.buttons_frame,
            text="Resume",
            command=self.resume,
            state=tk.NORMAL,
            style="Resume.TButton",
        )

        # buttons
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
        self.button_reload = ttk.Button(
            self.buttons_frame,
            text="Reload",
            command=self.reload,
            state=tk.NORMAL,
            style="Reload.TButton",
        )

        # checkboxes
        self.option_vars: list[tk.BooleanVar] = []
        for _ in range(100):
            option_var = tk.BooleanVar()
            option_var.set(False)
            self.option_vars.append(option_var)
        self.checkbox_separator1 = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.checkbox_frame1 = ttk.Frame(self.frame, style="Custom.TFrame")
        self.checkbox_otserver = ttk.Checkbutton(
            self.checkbox_frame1,
            text="OTServer",
            variable=self.option_vars[0],
            style="Custom.TCheckbutton",
            command=self.toggle_otserver,
        )
        self.checkbox_walk = ttk.Checkbutton(
            self.checkbox_frame1,
            text="Walk",
            variable=self.option_vars[1],
            style="Custom.TCheckbutton",
            command=self.toggleWalk,
        )
        self.checkbox_loot = ttk.Checkbutton(
            self.checkbox_frame1,
            text="Loot",
            variable=self.option_vars[2],
            style="Custom.TCheckbutton",
            command=self.toggleLoot,
        )
        self.checkbox_drop = ttk.Checkbutton(
            self.checkbox_frame1,
            text="Drop",
            variable=self.option_vars[3],
            style="Custom.TCheckbutton",
            command=self.toggleDrop,
        )
        self.checkbox_separator2 = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.checkbox_frame2 = ttk.Frame(self.frame, style="Custom.TFrame")
        self.checkbox_heal = ttk.Checkbutton(
            self.checkbox_frame2,
            text=f"Heal [{HEAL_KEY.name.upper()}]",  # type: ignore
            variable=self.option_vars[4],
            style="Custom.TCheckbutton",
            command=self.toggleHeal,
        )
        self.checkbox_attack = ttk.Checkbutton(
            self.checkbox_frame2,
            text="Attack",
            variable=self.option_vars[5],
            style="Custom.TCheckbutton",
            command=self.toggleAttack,
        )
        self.checkbox_strike = ttk.Checkbutton(
            self.checkbox_frame2,
            text=f"Strike [{STRIKE_KEY.name.upper()}]",  # type: ignore
            variable=self.option_vars[6],
            style="Custom.TCheckbutton",
            command=self.toggleStrike,
        )
        self.checkbox_separator3 = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.checkbox_frame3 = ttk.Frame(self.frame, style="Custom.TFrame")
        self.checkbox_eat = ttk.Checkbutton(
            self.checkbox_frame3,
            text=f"Eat [{FOOD_KEY.name.upper()}]",  # type: ignore
            variable=self.option_vars[7],
            style="Custom.TCheckbutton",
            command=self.toggleEat,
        )
        self.checkbox_ring = ttk.Checkbutton(
            self.checkbox_frame3,
            text=f"Ring [{RING_KEY.name.upper()}]",  # type: ignore
            variable=self.option_vars[8],
            style="Custom.TCheckbutton",
            command=self.toggleRing,
        )
        self.checkbox_utura = ttk.Checkbutton(
            self.checkbox_frame3,
            text=f"Utura [{UTURA_KEY.name.upper()}]",  # type: ignore
            variable=self.option_vars[9],
            style="Custom.TCheckbutton",
            command=self.toggleUtura,
        )
        self.checkbox_haste = ttk.Checkbutton(
            self.checkbox_frame3,
            text=f"Haste [{HASTE_KEY.name.upper()}]",  # type: ignore
            variable=self.option_vars[10],
            style="Custom.TCheckbutton",
            command=self.toggleHaste,
        )

        # dropdowns
        selected_hunt = tk.StringVar(self.frame)
        selected_hunt.set(getHuntList()[1])
        self.selectHunt(value=getHuntList()[1])
        self.dropdown_separator1 = ttk.Frame(
            self.frame, height=10, width=10, style="Custom.TFrame"
        )
        self.dropdown_frame = ttk.Frame(self.frame, style="Custom.TFrame")
        self.dropdown_hunt = ttk.OptionMenu(
            self.dropdown_frame,
            selected_hunt,
            *getHuntList(),
            command=self.selectHunt,
        )
        selected_container = tk.StringVar(self.frame)
        selected_container.set(GameUI.getContainerList()[1])
        GameUI.setContainer(GameUI.getContainerList()[1])
        self.dropdown_separator2 = ttk.Frame(
            self.dropdown_frame, height=10, width=8, style="Custom.TFrame"
        )
        self.dropdown_container = ttk.OptionMenu(
            self.dropdown_frame,
            selected_container,
            *GameUI.getContainerList(),
            command=self.selectContainer,
        )

        # console
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
        self.button_reload.config(state=tk.DISABLED)
        loop_thread = threading.Thread(
            target=main_loop
        )  # create a "loop_thread" thread to run "main_loop"
        loop_thread.start()  # start the "loop_thread"

    def pause(self):
        self.rootWindow.focus()
        Status.pause()  # stops the "main_loop"
        self.button_resume.config(state=tk.NORMAL, text="Resume")
        self.button_pause.config(state=tk.DISABLED, text="Paused")
        self.button_reload.config(state=tk.NORMAL)

    def reload(self):
        self.rootWindow.focus()
        Console.log("Reloading...")
        FolderManager.clear_folder(Dir.SESSION)
        Config.logScreenInfo()
        if Config.getAttack():
            setupAttack()
        if Config.getHeal():
            GameUI.locateHealthBar()
        if Config.getWalk():
            GameUI.locateMap()
        if Config.getLoot() or Config.getDrop():
            GameUI.locateGameWindow()
        if Config.getEat() or Config.getDrop():
            GameUI.locateDropContainer()
        if Config.anyStat():
            GameUI.locateStatsWindow()
        if Config.getRing():
            GameUI.locateRingSlot()

        Console.log("Reload complete")

    def toggle_otserver(self):
        self.checkbox_otserver.state(  # type: ignore
            ["!selected" if Config.getOTServer() else "selected"],
        )
        if Config.getOTServer():
            Config.setOTServer(False)
        else:
            Config.setOTServer(True)
        self.reload()
        Console.log(f"OTServer: {Config.getOTServer()}")

    def toggleAttack(self):
        self.checkbox_attack.state(  # type: ignore
            ["!selected" if Config.getAttack() else "selected"],
        )
        if Config.getAttack():
            Config.setAttack(False)
            disable_attack()
            FolderManager.delete_file(f"{Dir.SESSION}/battle.png")
        else:
            Config.setAttack(True)
            enable_attack()
            setupAttack()
        Console.log(f"Attack: {Config.getAttack()}")

    def toggleHeal(self):
        self.checkbox_heal.state(  # type: ignore
            ["!selected" if Config.getHeal() else "selected"],
        )
        if Config.getHeal():
            Config.setHeal(False)
        else:
            Config.setHeal(True)
            GameUI.locateHealthBar()
        Console.log(f"Heal: {Config.getHeal()}")

    def toggleWalk(self):
        self.checkbox_walk.state(  # type: ignore
            ["!selected" if Config.getWalk() else "selected"],
        )
        if Config.getWalk():
            Config.setWalk(False)
        else:
            Config.setWalk(True)
            GameUI.locateMap()
        Console.log(f"Walk: {Config.getWalk()}")

    def toggleLoot(self):
        self.checkbox_loot.state(  # type: ignore
            ["!selected" if Config.getLoot() else "selected"],
        )
        if Config.getLoot():
            Config.setLoot(False)
        else:
            Config.setLoot(True)
        Console.log(f"Loot: {Config.getLoot()}")

    def toggleEat(self):
        self.checkbox_eat.state(  # type: ignore
            ["!selected" if Config.getEat() else "selected"],
        )
        if Config.getEat():
            Config.setEat(False)
        else:
            Config.setEat(True)
            GameUI.locateStatsWindow()
            if not Config.getDrop():
                GameUI.locateDropContainer()
        Console.log(f"Eat: {Config.getEat()}")

    def toggleDrop(self):
        self.checkbox_drop.state(  # type: ignore
            ["!selected" if Config.getDrop() else "selected"],
        )
        if Config.getDrop():
            Config.setDrop(False)
        else:
            Config.setDrop(True)
            GameUI.locateDropContainer()
            GameUI.locateGameWindow()
        Console.log(f"Drop: {Config.getDrop()}")

    def toggleHaste(self):
        self.checkbox_haste.state(  # type: ignore
            ["!selected" if Config.getHaste() else "selected"],
        )
        if Config.getHaste():
            Config.setHaste(False)
        else:
            Config.setHaste(True)
            GameUI.locateStatsWindow()
        Console.log(f"Haste: {Config.getHaste()}")

    def toggleRing(self):
        self.checkbox_ring.state(  # type: ignore
            ["!selected" if Config.getRing() else "selected"],
        )
        if Config.getRing():
            Config.setRing(False)
        else:
            Config.setRing(True)
            GameUI.locateRingSlot()
        Console.log(f"Ring: {Config.getRing()}")

    def toggleUtura(self):
        self.checkbox_utura.state(  # type: ignore
            ["!selected" if Config.getUtura() else "selected"],
        )
        if Config.getUtura():
            Config.setUtura(False)
        else:
            Config.setUtura(True)
            GameUI.locateStatsWindow()
        Console.log(f"Utura: {Config.getUtura()}")

    def toggleStrike(self):
        self.checkbox_strike.state(  # type: ignore
            ["!selected" if Config.getStrike() else "selected"],
        )
        if Config.getStrike():
            Config.setStrike(False)
        else:
            Config.setStrike(True)
        Console.log(f"Strike: {Config.getStrike()}")

    def selectHunt(self, value: StringVar | str) -> None:
        if isinstance(value, StringVar):
            setHunt(value.get())
        else:
            setHunt(value)
        self.reload()
        Console.log(f"Selected hunt: {value}")

    def selectContainer(self, value: StringVar | str):
        if isinstance(value, StringVar):
            GameUI.setContainer(value.get())
        else:
            GameUI.setContainer(value)
        self.reload()
        Console.log(f"Selected container: {value}")

    def configure_widgets(self):
        style = ttk.Style(self.rootWindow)
        # style.theme_use('clam')
        style.configure("Custom.TFrame", background="#f9f9f9")  # type: ignore
        style.configure(  # type: ignore
            "Pause.TButton",
            padding=5,
            width=16,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.map(  # type: ignore
            "Pause.TButton",
            foreground=[("disabled", "red")],
        )
        style.configure(  # type: ignore
            "Resume.TButton",
            padding=5,
            width=16,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.map(  # type: ignore
            "Resume.TButton",
            foreground=[("disabled", "green")],
        )
        style.configure(  # type: ignore
            "Reload.TButton",
            padding=5,
            width=16,
            borderRadius=11,
            background="#f9f9f9",
        )
        style.configure(  # type: ignore
            "Custom.TCheckbutton",
            background="#f9f9f9",
            foreground="red",
            width=10,
        )
        style.map(  # type: ignore
            "Custom.TCheckbutton",
            foreground=[("selected", "green")],
        )

        self.rootWindow.title(uid)
        self.rootWindow.geometry("382x352")
        self.rootWindow.configure(bg="#f9f9f9")
        self.rootWindow.resizable(False, False)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # buttons
        self.buttons_frame.pack()
        self.button_resume.pack(side=tk.LEFT)
        self.button_separator1.pack(side=tk.LEFT)
        self.button_pause.pack(side=tk.LEFT)
        self.button_separator2.pack(side=tk.LEFT)
        self.button_reload.pack(side=tk.LEFT)

        # checkboxes
        self.checkbox_separator1.pack()
        self.checkbox_frame1.pack(fill=tk.BOTH, expand=True)
        self.checkbox_otserver.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_walk.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_loot.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_drop.pack(side=tk.LEFT, padx=(0, 0))
        self.checkbox_separator2.pack()
        self.checkbox_frame2.pack(fill=tk.BOTH, expand=True)
        self.checkbox_heal.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_attack.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_strike.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_separator3.pack()
        self.checkbox_frame3.pack(fill=tk.BOTH, expand=True)
        self.checkbox_eat.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_ring.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_utura.pack(side=tk.LEFT, padx=(0, 10))
        self.checkbox_haste.pack(side=tk.LEFT, padx=(0, 0))

        # dropdowns
        self.dropdown_separator1.pack()
        self.dropdown_frame.pack()
        self.dropdown_container.configure(width=24)
        self.dropdown_container.pack(side=tk.LEFT)
        self.dropdown_separator2.pack(side=tk.LEFT)
        self.dropdown_hunt.configure(width=24)
        self.dropdown_hunt.pack(side=tk.LEFT)

        # console
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
        self.configure_widgets()
        self.toggle_otserver()
        self.rootWindow.mainloop()


if __name__ == "__main__":
    gui_manager = GUIManager()
    gui_manager.start()
