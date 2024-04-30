import threading
import time
from typing import Any

from pyscreeze import Box

from lib.config import MAX_CLEANER_AMOUNT, Config
from lib.modules.eat import eat, food_list, isFood, isHungry
from lib.utils.console import Console
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.mouse import Mouse
from lib.utils.status import Status

_active_cleaners: list[int] = []
_last_checked: list[int] = []
_lock_drop: bool = False
_blackList: list[str] = food_list + Dir.getFiles(Dir.BLACKLIST)


def cleanerAmount():
    return len(_active_cleaners)


def _isLocked():
    return _lock_drop


def _lockDrop(value: bool):
    global _lock_drop
    _lock_drop = value


def _drop(box: Box) -> None:
    if Mouse.is_locked():
        time.sleep(0.1)
        return _drop(box)
    Mouse.lock(True)
    _initPos: tuple[Any, Any] = Mouse.get_pos()
    Mouse.press_left((box.left + 16, box.top + 16))
    Mouse.release_left((Config.getScreenCenterX(), Config.getScreenCenterY()))
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)


def _getItemName(image: str) -> str:
    aux: list[str] = image.split(".")[0].split("/")
    name: str = aux[len(aux) - 1]
    return name


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


def activeCleaners() -> list[int]:
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
    while not Status.is_paused() and (Config.getEat() or Config.getDrop()):
        if GameUI.getContainerWindows():
            for _window in GameUI.getContainerWindows():
                for _image in _list:
                    _box = ImageLocator.get_pos_on_region(
                        _image, _window, grayscale=True
                    )
                    _found = isinstance(_box, Box)
                    if _found and not _isLocked():
                        _lockDrop(True)
                        if Config.getEat() and isFood(_image) and isHungry():
                            Console.log(f"Eating {_getItemName(_image)}")
                            eat(_box)
                        elif Config.getDrop():
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
