import time
from pyscreeze import Box

from lib.config import HASTE_KEY
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.keyboard import Keyboard

_stat_haste: str = f"{Dir.INTERFACE}/stat_haste.png"


class Haste:
    @staticmethod
    def status() -> bool:
        _box = ImageLocator.get_pos_on_region(
            _stat_haste,
            GameUI.getStatsWindow(),
            grayscale=True,
        )
        _found = isinstance(_box, Box)
        if _found:
            return True
        return False

    @staticmethod
    def use() -> None:
        Keyboard.press(HASTE_KEY)
        time.sleep(0.5)
