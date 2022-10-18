from datetime import datetime
import sys
import ctypes
import time
import keyboard
from lib.actions.action import executeAction
from lib.utils.status import pause, isPaused, status
from setup import setup

# _start = datetime.now()


def run():
    # global _start
    # while (datetime.now()-_start).seconds < 18000:
    while 1:

        if keyboard.is_pressed('='):
            pause(not isPaused())

        if not isPaused():
            executeAction()

        time.sleep(0.1)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    setup()
    run()
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
