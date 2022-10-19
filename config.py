
from lib.utils.keyboard import key

# ACTIONS --------------------------------------------------
HEAL = True
ATTACK = True
LOOT = True
DROP = True
WALK = True

# HEAL --------------------------------------------------
HEAL_KEY = key.f9
HEAL_ON_YELLOW = False  # if False will heal on red

HEALTH_BAR_LEFT = 971
HEALTH_BAR_TOP = 36
HEALTH_BAR_WIDTH = 16
HEALTH_BAR_HEIGHT = 16


# ATTACK --------------------------------------------------
ATTACK_KEY = key.space
ATTACK_TIMEOUT = 0  # 0 to disable


# LOOT --------------------------------------------------
SCREEN_CENTER_X = 405
SCREEN_CENTER_Y = 330
SQM_SIZE = 50

# DROP --------------------------------------------------
DROP_CONTAINER = "backpack"
MAX_CLEANER_AMOUNT = 4  # each cleaner is a thread

SLOT_AREA_LEFT = 1745
SLOT_AREA_TOP = 450
SLOT_AREA_WIDTH = 155
SLOT_AREA_HEIGHT = 40

# WALK --------------------------------------------------
STOP_ALL_ACTIONS_KEY = key.pause
WALK_COOLDOWN = 60

WALK_AREA_LEFT = 990
WALK_AREA_TOP = 50
WALK_AREA_WIDTH = 755
WALK_AREA_HEIGHT = 560

MAP_AREA_LEFT = 1750
MAP_AREA_TOP = 85
MAP_AREA_WIDTH = 105
MAP_AREA_HEIGHT = 105
