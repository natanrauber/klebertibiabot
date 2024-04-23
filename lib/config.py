import os

from lib.utils.cwd import CWD
from lib.utils.folder_manager import FolderManager
from lib.utils.keyboard import Key

SESSION_DIR = CWD + "/images/session"
TEMP_DIR = CWD + "/images/temp"

# Expected Tibia window size: 1020x650
# Expected projector window size: 1020x318


# PROJECTOR --------------------------------------------------
PROJECTOR: bool = False


def getProjector():
    global PROJECTOR
    return PROJECTOR


def setProjector(value: bool):
    global PROJECTOR
    PROJECTOR = value


# ATTACK --------------------------------------------------
ATTACK: bool = False
ATTACK_KEY = Key.space
ATTACK_TIMEOUT = 0  # 0 to disable


def getAttack():
    global ATTACK
    return ATTACK


def setAttack(value: bool):
    global ATTACK
    ATTACK = value


# HEAL --------------------------------------------------
HEAL: bool = False
HEAL_KEY = Key.f9
HEAL_ON_YELLOW = True  # if False will heal on red


def getHeal():
    global HEAL
    return HEAL


def setHeal(value: bool):
    global HEAL
    HEAL = value
    if HEAL == False:
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
    if _loot == False and DROP == False:
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
WALK: bool = False
WAYPOINTS_DIR = f"{CWD}/images/waypoints"
ROPE_KEY = Key.f5
STOP_ALL_ACTIONS_KEY = Key.pause


def getWalk():
    global WALK
    return WALK


def setWalk(value: bool):
    global WALK
    WALK = value
    if WALK == False:
        FolderManager.delete_file(f"{SESSION_DIR}/map.png")


# EAT --------------------------------------------------
EAT: bool = False


def getEat():
    global EAT
    return EAT


def setEat(value: bool):
    global EAT
    EAT = value
    if EAT == False and DROP == False:
        for file_name in os.listdir(SESSION_DIR):
            if "container" in file_name:
                os.remove(os.path.join(SESSION_DIR, file_name))


# DROP --------------------------------------------------
DROP: bool = False
DROP_CONTAINER = "shopping_bag"
MAX_CLEANER_AMOUNT = 4  # each cleaner runs in a CPU thread


def getDrop():
    global DROP
    return DROP


def setDrop(value: bool):
    global DROP
    DROP = value
    if EAT == False and DROP == False:
        for file_name in os.listdir(SESSION_DIR):
            if "container" in file_name:
                os.remove(os.path.join(SESSION_DIR, file_name))
    if DROP == False and not getLoot():
        FolderManager.delete_file(f"{SESSION_DIR}/screen_center.png")


# DESTROY --------------------------------------------------
DESTROY: bool = False
DESTROY_KEY = Key.f4
