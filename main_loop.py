import threading
from datetime import datetime

import pyautogui

from config import SESSION_DIR
from lib.actions.action import executeAction
from lib.utils.status import isPaused


def loop():
    while not (datetime.now().hour == 6 and datetime.now().minute == 0):
        if isPaused():
            break
        executeAction()

    pyautogui.screenshot(f'{SESSION_DIR}/end.png')


loop_thread = threading.Thread(target=loop)
loop_thread.start()
