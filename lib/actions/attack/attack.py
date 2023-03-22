import time

import pyautogui
from pyscreeze import Box

from config import *
from lib.actions.loot.loot import setLoot
from lib.utils.console import Colors, Console
from lib.utils.image_locator import ImageLocator
from lib.utils.keyboard import Keyboard

_enabled = True  # local controller, keep this on
_battle_window_title = 'C:/dev/kleber/lib/actions/attack/images/battle_window_title.png'
_is_attacking = 'C:/dev/kleber/lib/actions/attack/images/is_attacking.png'
_battle_window = None
_target_pixel_x = None
_target_pixel_y = None


def isAttackEnabled():
    global _enabled
    return _enabled


def enable_attack():
    global _enabled
    if not _enabled:
        _enabled = True
        Console.log('attack enabled', color=Colors.green)


def disable_attack():
    global _enabled
    if _enabled:
        _enabled = False
        Console.log('attack disabled', color=Colors.red)


def setupAttack():
    _locateBattle()
    _defTargetPixel()


def _locateBattle():
    global _battle_window
    _battle_window = ImageLocator.locate_window(
        _battle_window_title, save_as='battle')
    if _battle_window == None:
        Console.log('cannot find battle window', color=Colors.red)
        exit()


def _defTargetPixel():
    global _target_pixel_x
    _target_pixel_x = int(_battle_window.left + 28)
    global _target_pixel_y
    _target_pixel_y = int(_battle_window.top + 32)


def hasTarget():
    _pixel = pyautogui.pixel(_target_pixel_x, _target_pixel_y)
    _hasTarget = _pixel[0] > 90 or _pixel[1] > 90
    return _hasTarget


def isAttacking():
    _box = ImageLocator.get_pos_on_region(
        _is_attacking, _battle_window, confidence=0.8)
    if type(_box) == Box:
        return True
    return False


def attack():
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Console.log('attacking...')
    Keyboard.press(ATTACK_KEY)
    setLoot(True)
    time.sleep(0.1)
