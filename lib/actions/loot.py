import time
import win32api
import win32con
import pyautogui
from config import SCREEN_CENTER_X, SCREEN_CENTER_Y, SQM_SIZE
from lib.shared import setLoot
from lib.utils.keyboard import Key, Keyboard
from lib.utils.log import log
from lib.utils.mouse import isMouseLocked, lockMouse, unlockMouse


def loot():
    if isMouseLocked():
        time.sleep(0.01)
        return loot()
    log("looting...")

    lockMouse()
    _initPos = pyautogui.position()
    Keyboard.press(Key.alt)
    _loot(SCREEN_CENTER_X+SQM_SIZE, SCREEN_CENTER_Y-SQM_SIZE)
    _loot(SCREEN_CENTER_X, SCREEN_CENTER_Y-SQM_SIZE)
    _loot(SCREEN_CENTER_X-SQM_SIZE, SCREEN_CENTER_Y-SQM_SIZE)
    _loot(SCREEN_CENTER_X-SQM_SIZE, SCREEN_CENTER_Y)
    _loot(SCREEN_CENTER_X-SQM_SIZE, SCREEN_CENTER_Y+SQM_SIZE)
    _loot(SCREEN_CENTER_X, SCREEN_CENTER_Y+SQM_SIZE)
    _loot(SCREEN_CENTER_X+SQM_SIZE, SCREEN_CENTER_Y+SQM_SIZE)
    _loot(SCREEN_CENTER_X+SQM_SIZE, SCREEN_CENTER_Y)
    _loot(SCREEN_CENTER_X, SCREEN_CENTER_Y)
    Keyboard.release(Key.alt)
    win32api.SetCursorPos(_initPos)
    unlockMouse()
    setLoot(False)


def _loot(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
