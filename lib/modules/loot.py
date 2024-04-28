import time

import pyautogui
from pyscreeze import Box

from lib.config import *
from lib.utils.colors import Colors
from lib.utils.console import Console
from lib.utils.cwd import CWD
from lib.utils.image_locator import ImageLocator
from lib.utils.keyboard import Key, Keyboard
from lib.utils.mouse import Mouse
from lib.utils.status import Status

_hasLoot = False


def hasLoot():
    if not getLoot():
        return False
    return _hasLoot


def setHasLoot(value):
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
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() - getSqmSize()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX(), getScreenCenterY() - getSqmSize()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() - getSqmSize()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() + getSqmSize()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX(), getScreenCenterY() + getSqmSize()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() + getSqmSize()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY()),
        duration=0.05,
    )
    Mouse.click_left(
        (getScreenCenterX(), getScreenCenterY()),
        duration=0.05,
    )
    Keyboard.release(Key.alt)
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)
    setHasLoot(False)
