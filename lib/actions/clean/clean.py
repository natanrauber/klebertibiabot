import asyncio
import threading
import time
import win32api
import win32con
import pyautogui
from pyscreeze import Box
from config import *
from lib.actions.eat import canEat, eat, isFood
from lib.utils.gui import getPosOnRegion, locateWindow
from lib.utils.log import Colors, log
from lib.utils.items import foodList
from lib.utils.mouse import isMouseLocked, lockMouse, unlockMouse
from os.path import isfile, join
from os import listdir

_active_cleaners = []
_last_checked = []
_lock = False
_blacklist_dir = "C:/dev/kleber/lib/actions/clean/images/blacklist/"
_blackList = foodList + [_blacklist_dir +
                         f for f in listdir(_blacklist_dir) if isfile(join(_blacklist_dir, f))]
_loot_window = None


def getContainerImage(name):
    if name == 'backpack':
        return "C:/dev/kleber/lib/actions/clean/images/containers/backpack.png"


def setupDrop():
    _locateDropContainer()


def _locateDropContainer():
    global _loot_window
    _loot_window = locateWindow(getContainerImage(DROP_CONTAINER), print=True)
    if _loot_window == None:
        log("cannot find loot container", color=Colors.red)
        exit()
    return


def cleanerAmount():
    return len(_active_cleaners)


def isLocked():
    return _lock


def lock(value: bool):
    global _lock
    _lock = value


async def _drop(box: Box):
    if isMouseLocked():
        time.sleep(0.01)
        return _drop(box)
    lockMouse()
    _initPos = pyautogui.position()
    win32api.SetCursorPos((box.left-944, box.top+16))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.SetCursorPos((SCREEN_CENTER_X, SCREEN_CENTER_Y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.SetCursorPos(_initPos)
    unlockMouse()
    time.sleep(0.5)


def _getItemName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux)-1]
    return aux


def getCleanerId():
    if _last_checked == []:
        for i in range(MAX_CLEANER_AMOUNT):
            _last_checked.append(i)
    return _last_checked[0]


def getList(id: int):
    _len = len(_blackList)
    _eachLen = int(_len / MAX_CLEANER_AMOUNT)
    _start = (_eachLen * (id+1)) - _eachLen
    _end = (_eachLen * (id+1))
    if (_end-1 + _eachLen) > _len:
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
    addCleaner(_id)
    _list = getList(_id)
    for _image in _list:
        _box = getPosOnRegion(_image, _loot_window,
                              grayscale=True)
        _found = type(_box) == Box
        if _found and not isLocked():
            lock(True)
            if canEat() and isFood(_image):
                log(f"eating {_getItemName(_image)}...")
                eat(_box)
            else:
                log(f"dropping {_getItemName(_image)}...")
                asyncio.run(_drop(_box))
            lock(False)
    removeCleaner(_id)


class Cleaner (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dropBlackList()
