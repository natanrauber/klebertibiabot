

from config import LOOT


_hasLoot = False


def hasLoot():
    if not LOOT:
        return False
    return _hasLoot


def setLoot(value):
    global _hasLoot
    _hasLoot = value
