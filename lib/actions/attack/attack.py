from datetime import datetime
import time
import pyautogui
from config import *
from lib.utils.getpos import getPos
from lib.utils.log import log
from lib.utils.keyboard import Keyboard
from lib.actions.loot import setLoot

_startAttackTime = datetime.now()
_battle_window_title = "C:/dev/kleber/lib/actions/attack/images/battle_window_title.png"
_targetHealthBar = "C:/dev/kleber/lib/actions/attack/images/target_health.png"
_target_pixel_x = None
_target_pixel_y = None
_is_attacking_pixel_x = None
_is_attacking_pixel_y = None


def targetHealthBar():
    return _targetHealthBar


def targetHealthBarBox():
    return (_target_pixel_x-2, _target_pixel_y-2, 132, 6)


def setupAttack():
    _pos = getPos(_battle_window_title)
    if _pos == None:
        log("cannot find battle window")
        exit()
    global _target_pixel_x
    _target_pixel_x = int(_pos.left + 23)
    global _target_pixel_y
    _target_pixel_y = int(_pos.top + 28)
    global _is_attacking_pixel_x
    _is_attacking_pixel_x = int(_pos.left + 18)
    global _is_attacking_pixel_y
    _is_attacking_pixel_y = int(_pos.top + 30)


def saveTargetHealth():
    pyautogui.screenshot(_targetHealthBar, region=targetHealthBarBox())


def hasTarget():
    _pixel = pyautogui.pixel(_target_pixel_x, _target_pixel_y)
    _hasTarget = _pixel[0] > 90 or _pixel[1] > 90
    return _hasTarget


def isAttacking():
    if attackOnCooldown():
        return True
    _isAttacking = pyautogui.pixel(
        _is_attacking_pixel_x, _is_attacking_pixel_y)[0] > 100
    return _isAttacking


def attackOnCooldown():
    return (datetime.now() - _startAttackTime).seconds < ATTACK_TIMEOUT


def attack():
    log("attacking...")
    global _startAttackTime
    _startAttackTime = datetime.now()
    saveTargetHealth()
    Keyboard.tap(ATTACK_KEY)
    time.sleep(0.5)
    setLoot(True)
