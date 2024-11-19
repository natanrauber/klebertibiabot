import time

from pyscreeze import Box

from lib.config import FOOD_KEY
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.keyboard import Keyboard

_stat_hungry: str = f"{Dir.INTERFACE}/stat_hungry.png"


class Food:

    @staticmethod
    def use() -> None:
        Keyboard.press(FOOD_KEY)
        time.sleep(0.5)

    @staticmethod
    def status() -> bool:
        _box = ImageLocator.get_pos_on_region(
            _stat_hungry,
            GameUI.getStatsWindow(),
            grayscale=True,
        )
        _found = isinstance(_box, Box)
        if _found:
            return False
        return True
