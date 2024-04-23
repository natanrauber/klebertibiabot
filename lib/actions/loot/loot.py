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
_localChat = CWD + "/images/interface/local_chat.png"
_storeButton = CWD + "/images/interface/store_button.png"


def locateScreenCenter():
    _screen_center = None
    try:
        _box1 = ImageLocator.get_pos(_localChat)
        _box2 = ImageLocator.get_pos(_storeButton)
        if type(_box1) == Box and type(_box2) == Box:
            _box1 = Box(_box1.left + 23, _box1.top - 11, 50, 50)
            _box2 = Box(_box2.left - 12, _box2.top + 22, 50, 50)
            width = _box2.left - _box1.left
            height = _box1.top - _box2.top
            setScreenCenter(_box1.left + (width // 2), _box2.top + (height // 2))
            setSqmSize(width // 15)
            _screen_center = Box(
                getScreenCenterX() - (getSqmSize() // 2),
                getScreenCenterY() - (getSqmSize() // 2),
                getSqmSize(),
                getSqmSize(),
            )
            screenshot_path = f"{SESSION_DIR}/screen_center.png"
            pyautogui.screenshot(screenshot_path, region=_screen_center)
        if _screen_center == None:
            Status.exit()
    except:
        Console.log("Cannot find health bar", color=Colors.red)
        Status.exit()


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
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    Mouse.click_left((getScreenCenterX(), getScreenCenterY() - getSqmSize()))
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    Mouse.click_left((getScreenCenterX() - getSqmSize(), getScreenCenterY()))
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    Mouse.click_left((getScreenCenterX(), getScreenCenterY() + getSqmSize()))
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    Mouse.click_left((getScreenCenterX() + getSqmSize(), getScreenCenterY()))
    Mouse.click_left((getScreenCenterX(), getScreenCenterY()))
    Keyboard.release(Key.alt)
    Mouse.set_pos(_initPos)
    Mouse.lock(False)
    setHasLoot(False)
