import time

from lib.utils.log import *
from lib.utils.wsh import wsh
from lib.utils.window import activateAllWindows

_isPaused = True


def status():
    return "PAUSED" if _isPaused else "RUNNING"


def isPaused():
    return _isPaused


def pause(value: bool):
    activateAllWindows()
    global _isPaused
    _isPaused = value
    if value:
        wsh.AppActivate("Administrador: Windows PowerShell")
    log(status(), color=Colors.YELLOW)
    time.sleep(2)
