
from lib.utils.keyboard import Key

# ACTIONS --------------------------------------------------
HEAL = True
ATTACK = True
LOOT = True
DROP = True
WALK = True

# HEAL --------------------------------------------------
HEAL_KEY = Key.f9
HEAL_ON_YELLOW = False  # if False will heal on red

HEALTH_BAR_LEFT = 971
HEALTH_BAR_TOP = 36
HEALTH_BAR_WIDTH = 16
HEALTH_BAR_HEIGHT = 16


# ATTACK --------------------------------------------------
ATTACK_KEY = Key.space
ATTACK_TIMEOUT = 0  # 0 to disable

TARGET_PIXEL_X = 1770
TARGET_PIXEL_Y = 410

IS_ATTACKING_PIXEL_X = 1745
IS_ATTACKING_PIXEL_Y = 400

TARGET_HEALTH_LEFT = 1765
TARGET_HEALTH_TOP = 406
TARGET_HEALTH_WIDTH = 136
TARGET_HEALTH_HEIGHT = 9

# LOOT --------------------------------------------------
SCREEN_CENTER_X = 405
SCREEN_CENTER_Y = 330
SQM_SIZE = 50

# DROP --------------------------------------------------
MAX_CLEANER_AMOUNT = 4  # each cleaner is a thread

SLOT_AREA_LEFT = 1745
SLOT_AREA_TOP = 450
SLOT_AREA_WIDTH = 155
SLOT_AREA_HEIGHT = 40

# WALK --------------------------------------------------
STOP_ALL_ACTIONS_KEY = Key.pause
WALK_COOLDOWN = 60

WALK_AREA_LEFT = 990
WALK_AREA_TOP = 50
WALK_AREA_WIDTH = 755
WALK_AREA_HEIGHT = 560

MAP_AREA_LEFT = 1750
MAP_AREA_TOP = 85
MAP_AREA_WIDTH = 105
MAP_AREA_HEIGHT = 105
