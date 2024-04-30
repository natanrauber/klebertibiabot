import os

from lib.utils.cwd import CWD
from lib.utils.folder_manager import FolderManager
from lib.utils.keyboard import Key

SESSION_DIR = CWD + "/images/session"
TEMP_DIR = CWD + "/images/temp"

# Expected Tibia window size: 1020x650
# Expected projector window size: 1020x318


# OT SERVER --------------------------------------------------
_otserver: bool = False


def getOTServer():
    global _otserver
    return _otserver


def setOTServer(value: bool):
    global _otserver
    _otserver = value


# ATTACK --------------------------------------------------
_attack: bool = False
ATTACK_KEY = Key.space
ATTACK_TIMEOUT = 0  # 0 to disable


def getAttack():
    global _attack
    return _attack


def setAttack(value: bool):
    global _attack
    _attack = value


# HEAL --------------------------------------------------
_heal: bool = False
HEAL_KEY = Key.f9
HEAL_ON_YELLOW = True  # if False will heal on red


def getHeal():
    global _heal
    return _heal


def setHeal(value: bool):
    global _heal
    _heal = value
    if _heal is False:
        FolderManager.delete_file(f"{SESSION_DIR}/health.png")


# LOOT --------------------------------------------------
_loot: bool = False
_screenCenterX = 0
_screenCenterY = 0
_sqmSize = 0


def getLoot():
    global _loot
    return _loot


def setLoot(value: bool):
    global _loot
    _loot = value
    if _loot is False and getDrop() is False:
        FolderManager.delete_file(f"{SESSION_DIR}/game_window.png")
        FolderManager.delete_file(f"{SESSION_DIR}/center_sqm.png")


def getScreenCenterX():
    global _screenCenterX
    return _screenCenterX


def getScreenCenterY():
    global _screenCenterY
    return _screenCenterY


def setScreenCenter(x: int, y: int):
    global _screenCenterX
    global _screenCenterY
    _screenCenterX = x
    _screenCenterY = y


def getSqmSize():
    global _sqmSize
    return _sqmSize


def setSqmSize(value: int):
    global _sqmSize
    _sqmSize = value


# WALK --------------------------------------------------
_walk: bool = False
WAYPOINTS_DIR = f"{CWD}/images/waypoints"
ROPE_KEY = Key.f5
STOP_ALL_ACTIONS_KEY = Key.pause


def getWalk():
    global _walk
    return _walk


def setWalk(value: bool):
    global _walk
    _walk = value
    if _walk is False:
        FolderManager.delete_file(f"{SESSION_DIR}/map.png")


# EAT --------------------------------------------------
_eat: bool = False


def getEat():
    global _eat
    return _eat


def setEat(value: bool):
    global _eat
    _eat = value
    if _eat is False:
        FolderManager.delete_file(f"{SESSION_DIR}/stats_window.png")
        if getDrop() is False:
            for file_name in os.listdir(SESSION_DIR):
                if "container" in file_name:
                    os.remove(os.path.join(SESSION_DIR, file_name))


# DROP --------------------------------------------------
_drop: bool = False
CONTAINERS_DIR = f"{CWD}/images/containers"
MAX_CLEANER_AMOUNT = 2  # each cleaner runs in a CPU thread


def getDrop():
    global _drop
    return _drop


def setDrop(value: bool):
    global _drop
    _drop = value
    if getEat() is False and _drop is False:
        for file_name in os.listdir(SESSION_DIR):
            if "container" in file_name:
                os.remove(os.path.join(SESSION_DIR, file_name))
    if _drop is False and not getLoot():
        FolderManager.delete_file(f"{SESSION_DIR}/game_window.png")
        FolderManager.delete_file(f"{SESSION_DIR}/center_sqm.png")


# DESTROY --------------------------------------------------
DESTROY: bool = False
DESTROY_KEY = Key.f4
