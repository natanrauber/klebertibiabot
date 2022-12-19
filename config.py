
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

HEALTH_BAR_LEFT = 971
HEALTH_BAR_TOP = 36
HEALTH_BAR_WIDTH = 16
HEALTH_BAR_HEIGHT = 16


# ATTACK --------------------------------------------------
ATTACK_KEY = Key.space
ATTACK_TIMEOUT = 0  # 0 to disable


# LOOT --------------------------------------------------
SCREEN_CENTER_X = 500
SCREEN_CENTER_Y = 260
SQM_SIZE = 40


# DROP --------------------------------------------------
DROP_CONTAINER = 'shopping_bag'
MAX_CLEANER_AMOUNT = 3  # each cleaner runs in a thread

SLOT_AREA_LEFT = 1745
SLOT_AREA_TOP = 450
SLOT_AREA_WIDTH = 155
SLOT_AREA_HEIGHT = 40


# WALK --------------------------------------------------
HUNT_NAME = 'poison_spider_cave'
ROPE_KEY = Key.f5
STOP_ALL_ACTIONS_KEY = Key.pause

WALK_AREA_LEFT = 990
WALK_AREA_TOP = 50
WALK_AREA_WIDTH = 755
WALK_AREA_HEIGHT = 560

MAP_AREA_LEFT = 1750
MAP_AREA_TOP = 85
MAP_AREA_WIDTH = 105
MAP_AREA_HEIGHT = 105
