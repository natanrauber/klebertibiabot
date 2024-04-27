import os

from lib.utils.cwd import CWD
from lib.utils.folder_manager import FolderManager
from lib.utils.keyboard import Key

SESSION_DIR = CWD + "/images/session"
TEMP_DIR = CWD + "/images/temp"

# Expected Tibia window size: 1020x650
# Expected projector window size: 1020x318


# PROJECTOR --------------------------------------------------
_projector: bool = False


def getProjector():
    global _projector
    return _projector


def setProjector(value: bool):
    global _projector
    _projector = value


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
    if _heal == False:
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
    if _loot == False and getDrop() == False:
        FolderManager.delete_file(f"{SESSION_DIR}/screen_center.png")


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
    if _walk == False:
        FolderManager.delete_file(f"{SESSION_DIR}/map.png")


# EAT --------------------------------------------------
_eat: bool = False


def getEat():
    global _eat
    return _eat


def setEat(value: bool):
    global _eat
    _eat = value
    if _eat == False and getDrop() == False:
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
    if getEat() == False and _drop == False:
        for file_name in os.listdir(SESSION_DIR):
            if "container" in file_name:
                os.remove(os.path.join(SESSION_DIR, file_name))
    if _drop == False and not getLoot():
        FolderManager.delete_file(f"{SESSION_DIR}/screen_center.png")


# DESTROY --------------------------------------------------
DESTROY: bool = False
DESTROY_KEY = Key.f4
