from ctypes import *


_lock = False


def isMouseLocked():
    return _lock


def lockMouse():
    global _lock
    _lock = True
    windll.user32.BlockInput(True)
    return False


def unlockMouse():
    global _lock
    _lock = False
    windll.user32.BlockInput(False)
