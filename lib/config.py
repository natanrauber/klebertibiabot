import os

from screeninfo import get_monitors

from lib.utils.console import Console
from lib.utils.dir import Dir
from lib.utils.folder_manager import FolderManager
from lib.utils.keyboard import Key, KeyCode

# Expected Tibia window size: 1020x650
# Expected projector window size: 1020x318

# Screen
monitor: int = 1
visible_taskbar: bool = False

# OT Server
otserver: bool = False

# Attack
attack: bool = False
ATTACK_KEY: Key | KeyCode = Key.space

# Heal
heal: bool = False
HEAL_KEY: Key | KeyCode = Key.f1

# Loot
loot: bool = False
screenCenterX = 0
screenCenterY = 0
sqmSize = 0
LOOT_KEY: Key | KeyCode = Key.backspace

# Walk
walk: bool = False
ROPE_KEY: Key | KeyCode = Key.f5
STOP_ALL_ACTIONS_KEY: Key | KeyCode = Key.pause

# Eat
eat: bool = False
FOOD_KEY: Key | KeyCode = Key.f9

# Drop
drop: bool = False
MAX_CLEANER_AMOUNT = 2  # each cleaner runs in a CPU thread

# Haste
haste: bool = False
HASTE_KEY: Key | KeyCode = Key.f12

# Ring
ring: bool = False
RING_KEY: Key | KeyCode = Key.f10

# Utura
utura: bool = False
UTURA_KEY: Key | KeyCode = Key.f11

# Strike
strike: bool = False
STRIKE_KEY: Key | KeyCode = Key.f5

# Destroy
DESTROY: bool = False
DESTROY_KEY: Key | KeyCode = Key.f4


class Config:
    # Screen
    @staticmethod
    def getMonitor() -> int:
        global monitor
        return monitor

    @staticmethod
    def getMonitorWidth() -> int:
        return int((get_monitors()[Config.getMonitor()].width))

    @staticmethod
    def getMonitorHeight() -> int:
        return int((get_monitors()[Config.getMonitor()].height))

    @staticmethod
    def getVisibleTaskbar() -> bool:
        global visible_taskbar
        return visible_taskbar

    @staticmethod
    def logScreenInfo():
        width: int = Config.getMonitorWidth()
        height: int = Config.getMonitorHeight()
        taskbar: str = "visible" if Config.getVisibleTaskbar() else "hidden"
        Console.log("--------------------")
        Console.log(f"Selected monitor: {Config.getMonitor()}")
        Console.log(f"Screen size: {width}x{height}")
        Console.log(f"Taskbar: {taskbar}")
        Console.log("--------------------")

    # OT Server
    @staticmethod
    def getOTServer() -> bool:
        global otserver
        return otserver

    @staticmethod
    def setOTServer(value: bool):
        global otserver
        otserver = value

    # Attack
    @staticmethod
    def getAttack() -> bool:
        global attack
        return attack

    @staticmethod
    def setAttack(value: bool):
        global attack
        attack = value

    # Heal
    @staticmethod
    def getHeal() -> bool:
        global heal
        return heal

    @staticmethod
    def setHeal(value: bool):
        global heal
        heal = value
        if heal is False:
            FolderManager.delete_file(f"{Dir.SESSION}/health.png")

    # Loot
    @staticmethod
    def getLoot() -> bool:
        global loot
        return loot

    @staticmethod
    def setLoot(value: bool):
        global loot
        loot = value
        if loot is False and Config.getDrop() is False:
            FolderManager.delete_file(f"{Dir.SESSION}/game_window.png")
            FolderManager.delete_file(f"{Dir.SESSION}/center_sqm.png")

    @staticmethod
    def getScreenCenterX() -> int:
        global screenCenterX
        return screenCenterX

    @staticmethod
    def getScreenCenterY() -> int:
        global screenCenterY
        return screenCenterY

    @staticmethod
    def setScreenCenter(x: int, y: int):
        global screenCenterX
        global screenCenterY
        screenCenterX = x
        screenCenterY = y

    @staticmethod
    def getSqmSize() -> int:
        global sqmSize
        return sqmSize

    @staticmethod
    def setSqmSize(value: int):
        global sqmSize
        sqmSize = value

    # Walk
    @staticmethod
    def getWalk() -> bool:
        global walk
        return walk

    @staticmethod
    def setWalk(value: bool):
        global walk
        walk = value
        if walk is False:
            FolderManager.delete_file(f"{Dir.SESSION}/map.png")

    # Eat
    @staticmethod
    def getEat() -> bool:
        global eat
        return eat

    @staticmethod
    def setEat(value: bool):
        global eat
        eat = value
        if eat is False:
            if Config.getDrop() is False:
                for file_name in os.listdir(Dir.SESSION):
                    if "container" in file_name:
                        os.remove(os.path.join(Dir.SESSION, file_name))
        if Config.anyStat() is False:
            FolderManager.delete_file(f"{Dir.SESSION}/stats_window.png")

    # Drop
    @staticmethod
    def getDrop() -> bool:
        global drop
        return drop

    @staticmethod
    def setDrop(value: bool):
        global drop
        drop = value
        if Config.getEat() is False and drop is False:
            for file_name in os.listdir(Dir.SESSION):
                if "container" in file_name:
                    os.remove(os.path.join(Dir.SESSION, file_name))
        if drop is False and not Config.getLoot():
            FolderManager.delete_file(f"{Dir.SESSION}/game_window.png")
            FolderManager.delete_file(f"{Dir.SESSION}/center_sqm.png")

    # Haste
    @staticmethod
    def getHaste() -> bool:
        global haste
        return haste

    @staticmethod
    def setHaste(value: bool):
        global haste
        haste = value
        if Config.anyStat() is False:
            FolderManager.delete_file(f"{Dir.SESSION}/stats_window.png")

    # Ring
    @staticmethod
    def getRing() -> bool:
        global ring
        return ring

    @staticmethod
    def setRing(value: bool):
        global ring
        ring = value
        if ring is False:
            FolderManager.delete_file(f"{Dir.SESSION}/ring_slot.png")

    # Utura
    @staticmethod
    def getUtura() -> bool:
        global utura
        return utura

    @staticmethod
    def setUtura(value: bool):
        global utura
        utura = value
        if Config.anyStat() is False:
            FolderManager.delete_file(f"{Dir.SESSION}/stats_window.png")

    # Strike
    @staticmethod
    def getStrike() -> bool:
        global strike
        return strike

    @staticmethod
    def setStrike(value: bool):
        global strike
        strike = value

    @staticmethod
    def anyStat() -> bool:
        if Config.getEat():
            return True
        if Config.getHaste():
            return True
        if Config.getUtura():
            return True
        return False
