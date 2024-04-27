import threading
import time
from os import listdir
from os.path import isfile, join

from pyscreeze import Box

from lib.actions.eat import eat, foodList, isFood, isHungry
from lib.config import *
from lib.utils.console import Console
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import getContainerWindows
from lib.utils.mouse import Mouse
from lib.utils.status import Status

_active_cleaners = []
_last_checked = []
_lock_drop = False
_blacklist_dir = CWD + "/images/blacklist/"
_blackList = foodList + [
    _blacklist_dir + f
    for f in listdir(_blacklist_dir)
    if isfile(join(_blacklist_dir, f))
]


def cleanerAmount():
    return len(_active_cleaners)


def _isLocked():
    return _lock_drop


def _lockDrop(value):
    global _lock_drop
    _lock_drop = value


def _drop(box: Box):
    if Mouse.is_locked():
        time.sleep(0.1)
        return _drop(box)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    if getProjector():
        Mouse.press_left((box.left + 16, box.top + 16 + 350))
    else:
        Mouse.press_left((box.left + 16, box.top + 16))
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def _getItemName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux) - 1]
    return aux


def getCleanerId():
    if _last_checked == []:
        for i in range(MAX_CLEANER_AMOUNT):
            _last_checked.append(i)
    return _last_checked[0]


def getList(id: int):
    _len = len(_blackList)
    _eachLen = int(_len / MAX_CLEANER_AMOUNT)
    _start = (_eachLen * (id + 1)) - _eachLen
    _end = _eachLen * (id + 1)
    if (_end - 1 + _eachLen) > _len:
        _end = _len
    return _blackList[_start:_end]


def activeCleaners() -> list:
    return _active_cleaners


def addCleaner(id: int):
    global _active_cleaners
    _active_cleaners.append(id)
    global _last_checked
    _last_checked.remove(id)


def removeCleaner(id: int):
    global _active_cleaners
    _active_cleaners.remove(id)
    global _last_checked
    _last_checked.append(id)


def dropBlackList():
    _id = getCleanerId()
    _list = getList(_id)
    addCleaner(_id)
    while not Status.is_paused() and (getEat() or getDrop()):
        if getContainerWindows():
            for _window in getContainerWindows():
                for _image in _list:
                    _box = ImageLocator.get_pos_on_region(
                        _image, _window, grayscale=True
                    )
                    _found = type(_box) == Box
                    if _found and not _isLocked():
                        _lockDrop(True)
                        if getEat() and isFood(_image) and isHungry():
                            Console.log(f"Eating {_getItemName(_image)}")
                            eat(_box)
                        elif getDrop():
                            Console.log(f"Dropping {_getItemName(_image)}")
                            _drop(_box)
                        time.sleep(0.5)
                        _lockDrop(False)
    Console.log(f"Removing cleaner {_id}")
    removeCleaner(_id)


class Cleaner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dropBlackList()
