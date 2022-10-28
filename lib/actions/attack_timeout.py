import threading
import pyautogui
from pyscreeze import Box
from config import *
from lib.actions.attack.attack import *

_timeout = False
_checkingTimeout = False


def timeout():
    return _timeout


def setTimeout(value: bool):
    global _timeout
    _timeout = value


def checkingTimeout():
    return _checkingTimeout


def _checking(value: bool):
    global _checkingTimeout
    _checkingTimeout = value


def _checkTimeout():
    _checking(True)
    while isAttacking():
        _box = pyautogui.locateOnScreen(
            targetHealthBar(), region=targetHealthBarBox(), confidence=0.9)
        if type(_box) == Box:
            log('attack timeout')
            global _timeout
            setTimeout(True)
        saveTargetHealth()
        time.sleep(ATTACK_TIMEOUT)
    _checking(False)


class AttackTimeoutChecker (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        _checkTimeout()
