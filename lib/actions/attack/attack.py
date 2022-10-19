from datetime import datetime
import time
import pyautogui
from config import *
from lib.utils.gui import *
from lib.utils.log import Colors, log
from lib.utils.keyboard import keyboard_controller
from lib.actions.loot.loot import setLoot
from pyscreeze import Box

_last_check_is_attacking = [datetime.now(), False]
_battle_window_title = "C:/dev/kleber/lib/actions/attack/images/battle_window_title.png"
_target_health_bar = "C:/dev/kleber/lib/actions/attack/images/target_health.png"
_is_attacking = "C:/dev/kleber/lib/actions/attack/images/is_attacking.png"
_battle_window = None
_target_pixel_x = None
_target_pixel_y = None


def targetHealthBar():
    return _target_health_bar


def targetHealthBarBox():
    return (_target_pixel_x-2, _target_pixel_y-2, 132, 5)


def setupAttack():
    _locateBattle()
    _defTargetPixel()


def _locateBattle():
    global _battle_window
    _battle_window = locateWindow(_battle_window_title)
    if _battle_window == None:
        log("cannot find battle window", color=Colors.red)
        exit()
    return


def _defTargetPixel():
    global _target_pixel_x
    _target_pixel_x = int(_battle_window.left + 28)
    global _target_pixel_y
    _target_pixel_y = int(_battle_window.top + 32)


def saveTargetHealth():
    pyautogui.screenshot(_target_health_bar, region=targetHealthBarBox())


def hasTarget():
    _pixel = pyautogui.pixel(_target_pixel_x, _target_pixel_y)
    _hasTarget = _pixel[0] > 90 or _pixel[1] > 90
    return _hasTarget


def isAttacking():
    global _last_check_is_attacking
    if (datetime.now()-_last_check_is_attacking[0]).seconds <= 1:
        return _last_check_is_attacking[1]
    _box = getPosOnRegion(_is_attacking, _battle_window, confidence=0.8)
    if type(_box) == Box:
        _last_check_is_attacking = [datetime.now(), True]
        return True
    _last_check_is_attacking = [datetime.now(), False]
    return False


def attack():
    log("attacking...")
    global _last_check_is_attacking
    _last_check_is_attacking = [datetime.now(), True]
    saveTargetHealth()
    keyboard_controller.tap(ATTACK_KEY)
    setLoot(True)
    time.sleep(0.1)
