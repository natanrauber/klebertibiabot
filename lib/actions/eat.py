from datetime import datetime
import pyautogui
from pyscreeze import Box
import win32api
import win32con

from lib.utils.mouse import lockMouse, unlockMouse
from lib.utils.items import foodList


_lastEat = datetime.now()


def canEat() -> bool:
    return (datetime.now() - _lastEat).seconds > 30


def isFood(image) -> bool:
    return image in foodList


def eat(box: Box):
    lockMouse()
    _initPos = pyautogui.position()
    win32api.SetCursorPos((box.left-944, box.top+16))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.SetCursorPos(_initPos)
    unlockMouse()
    global _lastEat
    _lastEat = datetime.now()
