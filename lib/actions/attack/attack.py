import time
import pyautogui
from config import *
from lib.utils.gui import *
from lib.utils.keyboard import Keyboard
from lib.utils.log import Colors, log
from lib.actions.loot.loot import setLoot
from pyscreeze import Box

_battle_window_title = 'C:/dev/kleber/lib/actions/attack/images/battle_window_title.png'
# _target_health_bar = 'C:/dev/kleber/lib/actions/attack/images/target_health.png'
_is_attacking = 'C:/dev/kleber/lib/actions/attack/images/is_attacking.png'
_battle_window = None
_target_pixel_x = None
_target_pixel_y = None


def setupAttack():
    _locateBattle()
    _defTargetPixel()


def _locateBattle():
    global _battle_window
    _battle_window = locateWindow(_battle_window_title, save_as='battle')
    if _battle_window == None:
        log('cannot find battle window', color=Colors.red)
        exit()


def _defTargetPixel():
    global _target_pixel_x
    _target_pixel_x = int(_battle_window.left + 28)
    global _target_pixel_y
    _target_pixel_y = int(_battle_window.top + 32)


# def targetHealthBar():
#     return _target_health_bar


# def targetHealthBarBox():
#     return (_target_pixel_x-2, _target_pixel_y-2, 132, 5)


# def saveTargetHealth():
#     pyautogui.screenshot(_target_health_bar, region=targetHealthBarBox())


def hasTarget():
    _pixel = pyautogui.pixel(_target_pixel_x, _target_pixel_y)
    _hasTarget = _pixel[0] > 90 or _pixel[1] > 90
    return _hasTarget


def isAttacking():
    _box = getPosOnRegion(_is_attacking, _battle_window, confidence=0.8)
    if type(_box) == Box:
        return True
    return False


def attack():
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    log('attacking...')
    # global _last_check_is_attacking
    # _last_check_is_attacking = [datetime.now(), True]
    # saveTargetHealth()
    Keyboard.press(ATTACK_KEY)
    setLoot(True)
    time.sleep(0.1)
