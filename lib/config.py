import os

from lib.utils.dir import Dir
from lib.utils.folder_manager import FolderManager
from lib.utils.keyboard import Key

# Expected Tibia window size: 1020x650
# Expected projector window size: 1020x318


# OT Server
otserver: bool = False

# Attack
attack: bool = False
ATTACK_KEY = Key.space

# Heal
heal: bool = False
HEAL_KEY = Key.f9

# Loot
loot: bool = False
screenCenterX = 0
screenCenterY = 0
sqmSize = 0

# Walk
walk: bool = False
ROPE_KEY = Key.f5
STOP_ALL_ACTIONS_KEY = Key.pause

# Eat
eat: bool = False

# Drop
drop: bool = False
MAX_CLEANER_AMOUNT = 2  # each cleaner runs in a CPU thread

# Destroy
DESTROY: bool = False
DESTROY_KEY = Key.f4


class Config:
    # OT Server
    @staticmethod
    def getOTServer():
        global otserver
        return otserver

    @staticmethod
    def setOTServer(value: bool):
        global otserver
        otserver = value

    # Attack
    @staticmethod
    def getAttack():
        global attack
        return attack

    @staticmethod
    def setAttack(value: bool):
        global attack
        attack = value

    # Heal
    @staticmethod
    def getHeal():
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
    def getLoot():
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
    def getScreenCenterX():
        global screenCenterX
        return screenCenterX

    @staticmethod
    def getScreenCenterY():
        global screenCenterY
        return screenCenterY

    @staticmethod
    def setScreenCenter(x: int, y: int):
        global screenCenterX
        global screenCenterY
        screenCenterX = x
        screenCenterY = y

    @staticmethod
    def getSqmSize():
        global sqmSize
        return sqmSize

    @staticmethod
    def setSqmSize(value: int):
        global sqmSize
        sqmSize = value

    # Walk
    @staticmethod
    def getWalk():
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
    def getEat():
        global eat
        return eat

    @staticmethod
    def setEat(value: bool):
        global eat
        eat = value
        if eat is False:
            FolderManager.delete_file(f"{Dir.SESSION}/stats_window.png")
            if Config.getDrop() is False:
                for file_name in os.listdir(Dir.SESSION):
                    if "container" in file_name:
                        os.remove(os.path.join(Dir.SESSION, file_name))

    # Drop
    @staticmethod
    def getDrop():
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
