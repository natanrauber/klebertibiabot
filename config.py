
from lib.utils.keyboard import Key

SESSION_DIR = 'C:/dev/kleber/images/session'
TEMP_DIR = 'C:/dev/kleber/images/temp'


# ACTIONS --------------------------------------------------
HEAL = True
ATTACK = True
LOOT = True
DROP = True
WALK = True

# HEAL --------------------------------------------------
HEAL_KEY = Key.f9
HEAL_ON_YELLOW = True  # if False will heal on red


# ATTACK --------------------------------------------------
ATTACK_KEY = Key.space
ATTACK_TIMEOUT = 0  # 0 to disable


# LOOT --------------------------------------------------
SCREEN_CENTER_X = 530
SCREEN_CENTER_Y = 285
SQM_SIZE = 40


# DROP --------------------------------------------------
DROP_CONTAINER = 'shopping_bag'
MAX_CLEANER_AMOUNT = 3  # each cleaner runs in a CPU thread


# WALK --------------------------------------------------
HUNT_NAME = 'secret_spider_lair'
ROPE_KEY = Key.f5
STOP_ALL_ACTIONS_KEY = Key.pause
