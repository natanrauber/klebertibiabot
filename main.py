import sys
import ctypes
from config import SESSION_DIR
from lib.actions.action import executeAction
from lib.utils.keyboard import Keyboard
from lib.utils.status import *
from setup import setup
from datetime import datetime
import pyautogui


def run():
    while not (datetime.now().hour == 6 and datetime.now().minute == 0):
        if Keyboard.isPressed('='):
            pause(not isPaused())

        if not isPaused():
            executeAction()

    pyautogui.screenshot(f'{SESSION_DIR}/end.png')


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
        None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
