import threading
import time
from os import listdir
from os.path import isfile, join

from genericpath import isfile
from pyscreeze import Box

from lib.config import *
from lib.utils.console import Colors, Console
from lib.utils.image_locator import ImageLocator
from lib.utils.keyboard import Keyboard
from lib.utils.status import Status
from lib.utils.window_manager import *

_dir = CWD + "/lib/actions/heal/images/"
_all_health_bars = [_dir + f for f in listdir(_dir) if isfile(join(_dir, f))]
_yellow = ["health_yellow.png"]
_red = ["health_red1.png", "health_red2.png"]
_heal_colors = [_dir + i for i in (_red if not HEAL_ON_YELLOW else _red + _yellow)]
_health_bar_box = None


def setupHeal():
    _locateHealthBar()


def _locateHealthBar():
    global _health_bar_box
    try:
        for i in _all_health_bars:
            _box = ImageLocator.get_pos(i)
            if type(_box) == Box:
                _health_bar_box = _box
                break
        if _health_bar_box == None:
            Status.exit()
    except:
        Console.log("cannot find health bar", color=Colors.red)
        Status.exit()


def _getImageName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux) - 1]
    return aux


def isWounded():
    for _image in _heal_colors:
        _box = ImageLocator.get_pos_on_region(_image, _health_bar_box, confidence=0.95)
        if type(_box) == Box:
            Console.log(f"healing on {_getImageName(_image)}")
            return True
    return False


_healing = False


def heal():
    global _healing
    _healing = True
    while not Status.is_paused():
        if isWounded():
            Keyboard.press(HEAL_KEY)
        time.sleep(0.5)
    _healing = False


def healing():
    return _healing


class Healer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        heal()
