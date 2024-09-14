from lib.config import Config
from lib.utils.console import Console
from lib.utils.keyboard import Key, Keyboard

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
    Keyboard.press(Key.backspace)
    setHasLoot(False)
