from lib.config import LOOT_KEY, Config
from lib.utils.console import Console
from lib.utils.keyboard import Keyboard

_hasLoot: bool = False


def hasLoot() -> bool:
    if not Config.getLoot():
        return False
    return _hasLoot


def setHasLoot(value: bool):
    global _hasLoot
    _hasLoot = value


def loot() -> None:
    Console.log("looting...")
    Keyboard.press(LOOT_KEY)
    setHasLoot(False)
