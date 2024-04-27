import time
from datetime import datetime

import pyautogui
from pyscreeze import Box

from lib.actions.loot.loot import setHasLoot
from lib.config import *
from lib.utils.console import Colors, Console
from lib.utils.interface import getBattleWindow, locateBattleWindow
from lib.utils.keyboard import Keyboard
from lib.utils.status import Status

_enabled = True  # local controller, keep this on
_target_pixel_x: int
_target_pixel_y: int
_attack_start_time = datetime.now()


def isAttackEnabled():
    global _enabled
    return _enabled


def enable_attack():
    global _enabled
    if not _enabled:
        _enabled = True
        Console.log("attack enabled", color=Colors.green)


def disable_attack():
    global _enabled
    if _enabled:
        _enabled = False
        Console.log("attack disabled", color=Colors.red)


def setupAttack():
    locateBattleWindow()
    _defTargetPixel()


def _defTargetPixel():
    if type(getBattleWindow()) == Box:
        global _target_pixel_x
        _target_pixel_x = int(getBattleWindow().left + 27)
        global _target_pixel_y
        _target_pixel_y = int(getBattleWindow().top + 32)


def hasTarget():
    _pixel = pyautogui.pixel(_target_pixel_x, _target_pixel_y)
    _hasTarget = _pixel[0] > 90 or _pixel[1] > 90
    if not _hasTarget:
        global _attack_start_time
        _attack_start_time = datetime(1, 1, 1)
        return False
    time = datetime.now() - _attack_start_time
    if time.seconds > 30 and time.seconds < 40:
        return False
    return True


def isAttacking():
    for i in range(2):
        if type(getBattleWindow()) is Box:
            if (datetime.now() - _attack_start_time).seconds > 30:
                Keyboard.press(STOP_ALL_ACTIONS_KEY)
                return False
            for i in range(int(getBattleWindow().height / 20)):
                _pixel = pyautogui.pixel(
                    int(getBattleWindow().left + 23),
                    int(getBattleWindow().top + (i * 20)),
                )
                _is_attacking = _pixel[0] > 250
                if _is_attacking:
                    return True
            time.sleep(0.1)
    return False


def attack():
    if Status.is_paused():
        return
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    global _attack_start_time
    _attack_start_time = datetime.now()
    Console.log("attacking...")
    Keyboard.press(ATTACK_KEY)
    setHasLoot(True)
    time.sleep(0.1)
