import time

from lib.config import LOOT, SCREEN_CENTER_X, SCREEN_CENTER_Y, SQM_SIZE
from lib.utils.console import Console
from lib.utils.keyboard import Key, Keyboard
from lib.utils.mouse import Mouse

_hasLoot = False


def hasLoot():
    if not LOOT:
        return False
    return _hasLoot


def setLoot(value):
    global _hasLoot
    _hasLoot = value


def loot():
    if Mouse.is_locked():
        time.sleep(0.1)
        return loot()
    Console.log("looting...")
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    time.sleep(0.3)
    Keyboard.hold(Key.alt)
    Mouse.click_left((SCREEN_CENTER_X + SQM_SIZE, SCREEN_CENTER_Y - SQM_SIZE))
    Mouse.click_left((SCREEN_CENTER_X, SCREEN_CENTER_Y - SQM_SIZE))
    Mouse.click_left((SCREEN_CENTER_X - SQM_SIZE, SCREEN_CENTER_Y - SQM_SIZE))
    Mouse.click_left((SCREEN_CENTER_X - SQM_SIZE, SCREEN_CENTER_Y))
    Mouse.click_left((SCREEN_CENTER_X - SQM_SIZE, SCREEN_CENTER_Y + SQM_SIZE))
    Mouse.click_left((SCREEN_CENTER_X, SCREEN_CENTER_Y + SQM_SIZE))
    Mouse.click_left((SCREEN_CENTER_X + SQM_SIZE, SCREEN_CENTER_Y + SQM_SIZE))
    Mouse.click_left((SCREEN_CENTER_X + SQM_SIZE, SCREEN_CENTER_Y))
    Mouse.click_left((SCREEN_CENTER_X, SCREEN_CENTER_Y))
    Keyboard.release(Key.alt)
    Mouse.set_pos(_initPos)
    Mouse.lock(False)
    setLoot(False)
