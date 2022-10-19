from genericpath import isfile
from os.path import isfile, join
from os import listdir
import threading
import time
import pyautogui
from pyscreeze import Box
from config import *
from lib.utils.gui import *
from lib.utils.log import Colors, log
from lib.utils.keyboard import keyboard_controller
from lib.utils.status import isPaused

_dir = "C:/dev/kleber/lib/actions/heal/images/"
_all_health_bars = [_dir + f for f in listdir(_dir) if isfile(join(_dir, f))]
_yellow = ["health_yellow.png"]
_red = ["health_red1.png", "health_red2.png"]
_heal_colors = [
    _dir + i for i in (_red if not HEAL_ON_YELLOW else _red + _yellow)]
_health_bar_box = None


def setupHeal():
    _locateHealthBar()


def _locateHealthBar():
    global _health_bar_box
    try:
        for i in _all_health_bars:
            _box = getPos(i)
            if type(_box) == Box:
                _health_bar_box = _box
                break
        if _health_bar_box == None:
            exit()
    except:
        log("cannot find health bar", color=Colors.red)
        exit()


def _getImageName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux)-1]
    return aux


def isWounded():
    for _image in _heal_colors:
        _box = getPos(_image)
        if type(_box) == Box:
            log('healing on {}...'.format(_getImageName(_image)))
            return True
    return False


def heal():
    global _healing
    _healing = True
    while 1:
        if not isPaused():
            if isWounded():
                keyboard_controller.tap(HEAL_KEY)
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
