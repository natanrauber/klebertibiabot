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
    Keyboard.press(Key.backspace)
    setHasLoot(False)
