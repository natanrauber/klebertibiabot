import os

from lib.utils.cwd import CWD
from lib.utils.keyboard import Key

SESSION_DIR = CWD + "/images/session"
TEMP_DIR = CWD + "/images/temp"

# Expected Tibia window size: 1020x650
# Expected projector window size: 1020x318


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


# LOOT --------------------------------------------------
LOOT: bool = False
SCREEN_CENTER_X = 585
SCREEN_CENTER_Y = 635
SQM_SIZE = 40


def setLoot(value: bool):
    global LOOT
    LOOT = value


# WALK --------------------------------------------------
WALK: bool = False
WAYPOINTS_DIR = f"{CWD}/lib/actions/walk/waypoints"
ROPE_KEY = Key.f5
STOP_ALL_ACTIONS_KEY = Key.pause


def getWalk():
    global WALK
    return WALK


def setWalk(value: bool):
    global WALK
    WALK = value


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


# EAT --------------------------------------------------
EAT: bool = False


def getEat():
    global EAT
    return EAT


def setEat(value: bool):
    global EAT
    EAT = value


# DESTROY --------------------------------------------------
DESTROY: bool = False
DESTROY_KEY = Key.f4
