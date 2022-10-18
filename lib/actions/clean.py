import asyncio
from datetime import datetime
import threading
import time
import win32api
import win32con
import pyautogui
from pyscreeze import Box
from config import *
from lib.actions.eat import canEat, eat, isFood
from lib.utils.log import log
from lib.utils.items import blackList
from lib.utils.mouse import isMouseLocked, lockMouse, unlockMouse

_activeCleaners = []
_lock = False


def cleanerAmount():
    return len(_activeCleaners)


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


def locateItem(image):
    _region = (SLOT_AREA_LEFT, SLOT_AREA_TOP,
               SLOT_AREA_WIDTH, SLOT_AREA_HEIGHT)
    box = pyautogui.locateOnScreen(
        image, region=_region, grayscale=True, confidence=0.9)
    if box != None:
        return box


def _getItemName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux)-1]
    return aux


def getCleanerId():
    for i in range(MAX_CLEANER_AMOUNT):
        if i not in activeCleaners():
            return i


def getList(id: int):
    _len = len(blackList)
    _eachLen = int(_len / MAX_CLEANER_AMOUNT)
    _start = (_eachLen * (id+1)) - _eachLen
    _end = (_eachLen * (id+1))
    if (_end-1 + _eachLen) > _len:
        _end = _len
    return blackList[_start:_end]


def activeCleaners() -> list:
    return _activeCleaners


def addCleaner(id: int):
    global _activeCleaners
    _activeCleaners.append(id)


def removeCleaner(id: int):
    global _activeCleaners
    _activeCleaners.remove(id)


def dropBlackList():
    _id = getCleanerId()
    addCleaner(_id)
    _list = getList(_id)
    for image in _list:
        _box = locateItem(image)
        _found = type(_box) == Box
        if _found and not isLocked():
            lock(True)
            if canEat() and isFood(image):
                log(f"eating {_getItemName(image)}...")
                eat(_box)
            else:
                log(f"dropping {_getItemName(image)}...")
                asyncio.run(_drop(_box))
            lock(False)
    removeCleaner(_id)


class Cleaner (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dropBlackList()
