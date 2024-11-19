import time

from pyscreeze import Box

from lib.config import UTURA_KEY
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.keyboard import Keyboard

_stat_utura: str = f"{Dir.INTERFACE}/stat_utura.png"


class Utura:
    @staticmethod
    def status() -> bool:
        _box = ImageLocator.get_pos_on_region(
            _stat_utura,
            GameUI.getStatsWindow(),
            grayscale=True,
        )
        _found = isinstance(_box, Box)
        if _found:
            return True
        return False

    @staticmethod
    def use() -> None:
        Keyboard.press(UTURA_KEY)
        time.sleep(0.5)
