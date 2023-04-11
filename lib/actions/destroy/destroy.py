import threading
import time
from os import listdir
from os.path import isfile, join

from genericpath import isfile
from pyscreeze import Box

from config import *
from lib.utils.console import Colors, Console
from lib.utils.image_locator import ImageLocator
from lib.utils.keyboard import Keyboard
from lib.utils.mouse import Mouse
from lib.utils.status import Status
from lib.utils.window_manager import *

_dir: str = 'C:/dev/kleber/lib/actions/destroy/images/'
_barriers = [_dir + f for f in listdir(_dir) if isfile(join(_dir, f))]
_game_window = None

_interface_dir: str = 'C:/dev/kleber/lib/actions/destroy'
_window_header: str = f'{_interface_dir}/header.png'
_window_footer: str = f'{_interface_dir}/footer.png'


def setup_destroy():
    _locate_game_window()


def _locate_game_window():
    global _game_window
    try:
        _box = ImageLocator.locate_window(
            _window_header, _window_footer, save_as='game_window')
        if type(_box) == Box:
            _game_window = _box
        if _game_window == None:
            exit()
    except:
        Console.log('cannot find game window', color=Colors.red)
        exit()


def _getImageName(image):
    aux = image.split('.')[0]
    aux = aux.split('/')
    aux = aux[len(aux)-1]
    return aux


def locateAndDestroy():
    for _image in _barriers:
        _box = ImageLocator.get_pos(
            _image,  confidence=0.8)
        if type(_box) == Box:
            Console.log(f'destroying {_getImageName(_image)}')
            _doDestroy(_box)
            time.sleep(3)


_destroying = False


def destroy():
    global _destroying
    _destroying = True
    while not Status.is_paused():
        locateAndDestroy()
    _destroying = False


def _doDestroy(box: Box):
    if Mouse.is_locked():
        time.sleep(0.1)
        return _doDestroy(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(DESTROY_KEY)
    Mouse.click_left((box.left-900+10, box.top+10))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def destroying():
    return _destroying


class Destroyer (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        destroy()
