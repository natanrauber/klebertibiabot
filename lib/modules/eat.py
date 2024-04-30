from datetime import datetime

from pyscreeze import Box

from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.mouse import Mouse

_stat_hungry: str = f"{Dir.INTERFACE}/stat_hungry.png"
food_list: list[str] = Dir.getFiles(Dir.FOOD)


def isFood(image: str) -> bool:
    return image in food_list


def eat(box: Box):
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.click_left((box.left + 16, box.top + 16))
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)
    global _lastEat
    _lastEat = datetime.now()


def isHungry() -> bool:
    _box = ImageLocator.get_pos_on_region(
        _stat_hungry,
        GameUI.getStatsWindow(),
        grayscale=True,
    )
    _found = isinstance(_box, Box)
    if _found:
        return True
    return False
