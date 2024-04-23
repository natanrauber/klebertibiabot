import time
from datetime import datetime
from typing import Optional

import pyautogui
from pyscreeze import Box

from lib.actions.loot.loot import setHasLoot
from lib.config import *
from lib.utils.console import Colors, Console
from lib.utils.image_locator import ImageLocator
from lib.utils.keyboard import Keyboard
from lib.utils.status import Status

_enabled = True  # local controller, keep this on
_battle_window_header = CWD + "/images/interface/battle_window_title.png"
_battle_window_footer = CWD + "/images/interface/window_footer.png"
_battle_window: Optional[Box]
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
    _locateBattle()
    _defTargetPixel()


def _locateBattle():
    global _battle_window
    _battle_window = ImageLocator.locate_window(
        _battle_window_header, _battle_window_footer, save_as="battle"
    )
    if _battle_window == None:
        Console.log("cannot find battle window", color=Colors.red)
        Status.exit()


def _defTargetPixel():
    if type(_battle_window) == Box:
        global _target_pixel_x
        _target_pixel_x = int(_battle_window.left + 27)
        global _target_pixel_y
        _target_pixel_y = int(_battle_window.top + 32)


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
        if type(_battle_window) is Box:
            if (datetime.now() - _attack_start_time).seconds > 30:
                Keyboard.press(STOP_ALL_ACTIONS_KEY)
                return False
            for i in range(int(_battle_window.height / 20)):
                _pixel = pyautogui.pixel(
                    int(_battle_window.left + 23), int(_battle_window.top + (i * 20))
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
