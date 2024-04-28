from datetime import datetime
from os import listdir
from os.path import isfile, join

from pyscreeze import Box

from lib.config import getOTServer
from lib.utils.cwd import CWD
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import getStatsWindow
from lib.utils.mouse import Mouse

_stat_hungry = CWD + "/images/interface/stat_hungry.png"
_food_dir = CWD + "/images/food/"

foodList = [_food_dir + f for f in listdir(_food_dir) if isfile(join(_food_dir, f))]


def isFood(image) -> bool:
    return image in foodList


def eat(box: Box):
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    if getOTServer():
        Mouse.click_left((box.left + 16, box.top + 16))
    else:
        Mouse.click_left((box.left + 16, box.top + 16 + 350))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)
    global _lastEat
    _lastEat = datetime.now()


def isHungry() -> bool:
    _box = ImageLocator.get_pos_on_region(
        _stat_hungry,
        getStatsWindow(),
        grayscale=True,
    )
    _found = type(_box) == Box
    if _found:
        return True
    return False
