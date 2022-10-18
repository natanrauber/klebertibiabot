import threading
import time
import pyautogui
from pyscreeze import Box
from config import *
from lib.utils.log import log
from lib.utils.keyboard import Keyboard


_DIR = "C:/dev/kleber/images/healthbar/"
_YELLOW = ["yellow.png"]
_RED = ["red1.png", "red2.png"]

_HEAL_COLORS = _RED if not HEAL_ON_YELLOW else _RED + _YELLOW

images = [_DIR + i for i in _HEAL_COLORS]


def locate(image):
    _region = (HEALTH_BAR_LEFT, HEALTH_BAR_TOP,
               HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
    _box = pyautogui.locateOnScreen(image, region=_region)
    if _box != None:
        return _box


def _getImageName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux)-1]
    return aux


def isWounded():
    for _image in images:
        _box = locate(_image)
        _found = type(_box) == Box
        if _found:
            log('healing on {}...'.format(_getImageName(_image)))
            return True
    return False


def heal():
    global _healing
    _healing = True
    if isWounded():
        Keyboard.tap(HEAL_KEY)
        time.sleep(0.5)
    _healing = False


_healing = False


def healing():
    return _healing


class Healer (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        heal()
