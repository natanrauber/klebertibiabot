import threading
import time

from pyscreeze import Box

from lib.config import HEAL_KEY, Config
from lib.utils.console import Console
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.keyboard import Keyboard
from lib.utils.status import Status

_low_health_list = [
    f"{Dir.HEALTH}/health_yellow.png",
    f"{Dir.HEALTH}/health_red1.png",
    f"{Dir.HEALTH}/health_red2.png",
]
healing = False


class Healer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global healing
        healing = True
        while not Status.is_paused() and Config.getHeal():
            if self.isWounded():
                Console.log("Healing...")
                Keyboard.press(HEAL_KEY)
            time.sleep(0.5)
        healing = False

    def isWounded(self):
        for _image in _low_health_list:
            _box = ImageLocator.get_pos_on_region(
                _image, GameUI.getHealthBar(), confidence=0.95
            )
            if isinstance(_box, Box):
                return True
        return False

    @staticmethod
    def active():
        global healing
        return healing
