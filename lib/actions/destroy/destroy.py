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
from lib.utils.mouse import Mouse
from lib.utils.status import Status
from lib.utils.window_manager import *

_dir: str = CWD + "/images/destroy/"
_barriers = [_dir + f for f in listdir(_dir) if isfile(join(_dir, f))]
_game_window = None

_interface_dir: str = CWD + "/images/interface"
_window_header: str = f"{_interface_dir}/header.png"
_window_footer: str = f"{_interface_dir}/footer.png"


def setup_destroy():
    _locate_game_window()


def _locate_game_window():
    global _game_window
    try:
        _box = ImageLocator.locate_window(
            _window_header, _window_footer, save_as="game_window"
        )
        if type(_box) == Box:
            _game_window = _box
        if _game_window == None:
            Status.exit()
    except:
        Console.log("cannot find game window", color=Colors.red)
        Status.exit()


def _getImageName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux) - 1]
    return aux


def locateAndDestroy():
    for _image in _barriers:
        _box = ImageLocator.get_pos(_image, confidence=0.8)
        if type(_box) == Box:
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


def _move(box: Box):
    if Mouse.is_locked():
        time.sleep(0.1)
        return _move(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    if getProjector():
        Mouse.press_left((box.left + 10, box.top + 10 + 350))
    else:
        Mouse.press_left((box.left + 10, box.top + 10))
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def _doDestroy(box: Box):
    if Mouse.is_locked():
        time.sleep(0.1)
        return _doDestroy(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(DESTROY_KEY)
    Mouse.click_left((box.left - 900 + 10, box.top + 10))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def destroying():
    return _destroying


class Destroyer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        destroy()
