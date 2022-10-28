import time
from config import SESSION_DIR

from lib.utils.log import *
from lib.utils.wsh import wsh
from lib.utils.gui import activateAllWindows
import pyautogui

_isPaused = True


def status():
    return 'PAUSED' if _isPaused else 'RUNNING'


def isPaused():
    return _isPaused


def pause(value: bool):
    activateAllWindows()
    global _isPaused
    _isPaused = value
    if _isPaused:
        wsh.AppActivate('Administrador: Windows PowerShell')
        pyautogui.screenshot(f'{SESSION_DIR}/end.png')
    log(status(), color=Colors.yellow)
    time.sleep(2)
