import time

from pyscreeze import Box

from lib.config import RING_KEY
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.keyboard import Keyboard

_empty_ring_slot: str = f"{Dir.INTERFACE}/empty_ring_slot.png"


class Ring:
    @staticmethod
    def status() -> bool:
        _box = ImageLocator.get_pos_on_region(
            _empty_ring_slot,
            GameUI.getRingSlot(),
            grayscale=True,
        )
        _found = isinstance(_box, Box)
        if _found:
            return False
        return True

    @staticmethod
    def use() -> None:
        Keyboard.press(RING_KEY)
        time.sleep(0.5)
