import time
from datetime import datetime

import pyautogui
from pyscreeze import Box

from lib.config import ATTACK_KEY, STOP_ALL_ACTIONS_KEY
from lib.modules.loot import setHasLoot
from lib.utils.console import Console
from lib.utils.interface import GameUI
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
        Console.log("attack enabled")


def disable_attack():
    global _enabled
    if _enabled:
        _enabled = False
        Console.log("attack disabled")


def setupAttack():
    GameUI.locateBattleWindow()
    _defTargetPixel()


def _defTargetPixel():
    if type(GameUI.getBattleWindow()) == Box:
        global _target_pixel_x
        global _target_pixel_y
        _target_pixel_x = int(GameUI.getBattleWindow().left + 27)
        _target_pixel_y = int(GameUI.getBattleWindow().top + 32)


def hasTarget():
    global _target_pixel_x
    global _target_pixel_y
    _pixel = pyautogui.pixel(_target_pixel_x, _target_pixel_y)
    _hasTarget = _pixel[0] > 90 or _pixel[1] > 90
    if not _hasTarget:
        global _attack_start_time
        _attack_start_time = datetime(1, 1, 1)
        return False
    time = datetime.now() - _attack_start_time
    if time.seconds > 20 and time.seconds < 40:
        return False
    return True


def isAttacking():
    for i in range(2):
        if (datetime.now() - _attack_start_time).seconds > 20:
            Keyboard.press(STOP_ALL_ACTIONS_KEY)
            return False
        for i in range(int(GameUI.getBattleWindow().height / 20)):
            _pixel = pyautogui.pixel(
                int(GameUI.getBattleWindow().left + 23),
                int(GameUI.getBattleWindow().top + (i * 20)),
            )
            _is_attacking = _pixel[0] > 250
            if _is_attacking:
                return True
        time.sleep(0.05)
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
