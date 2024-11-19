import random
import time
from typing import Any

from lib.config import Config
from lib.utils.console import Console
from lib.utils.keyboard import Key, Keyboard
from lib.utils.mouse import Mouse

_hasLoot: bool = False


def hasLoot() -> bool:
    if not Config.getLoot():
        return False
    return _hasLoot


def setHasLoot(value: bool):
    global _hasLoot
    _hasLoot = value


def loot() -> None:
    if Mouse.is_locked():
        time.sleep(0.1)
        return loot()
    Console.log("looting...")
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    time.sleep(0.3)
    Keyboard.hold(Key.alt)
    sqm_list: list[tuple[Any, Any]] = [
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    ]
    random.shuffle(sqm_list)
    for i in range(len(sqm_list)):
        Mouse.click_left(sqm_list[i], duration=0.05)

    Keyboard.release(Key.alt)
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)
    setHasLoot(False)
