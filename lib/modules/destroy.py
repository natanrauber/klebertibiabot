import threading
import time

from pyscreeze import Box

from lib.config import DESTROY_KEY, STOP_ALL_ACTIONS_KEY, Config
from lib.utils.console import Console
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.keyboard import Keyboard
from lib.utils.mouse import Mouse
from lib.utils.status import Status

_barriers = Dir.getFiles(Dir.DESTROY)


def setup_destroy():
    GameUI.locateGameWindow()


def _getImageName(image: str) -> str:
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux) - 1]
    return aux


def locateAndDestroy():
    for _image in _barriers:
        _box = ImageLocator.get_pos(_image, confidence=0.8)
        if isinstance(_box, Box):
            Status.sleep(3)
            if "move" in _image:
                Console.log(f"moving {_getImageName(_image)}")
                _move(_box)
            else:
                Console.log(f"destroying {_getImageName(_image)}")
                _doDestroy(_box)


_destroying = False


def destroy():
    global _destroying
    _destroying = True
    while not Status.is_paused():
        locateAndDestroy()
    _destroying = False


def _move(box: Box) -> None:
    if Mouse.is_locked():
        time.sleep(0.1)
        return _move(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.press_left((box.left + 10, box.top + 10))
    Mouse.release_left((Config.getScreenCenterX(), Config.getScreenCenterY()))
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)


def _doDestroy(box: Box) -> None:
    if Mouse.is_locked():
        time.sleep(0.1)
        return _doDestroy(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(DESTROY_KEY)
    Mouse.click_left((box.left - 900 + 10, box.top + 10))
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)


def destroying():
    return _destroying


class Destroyer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        destroy()
