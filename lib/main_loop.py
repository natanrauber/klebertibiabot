from datetime import datetime

from lib.action import executeAction
from lib.utils.status import Status


def main_loop() -> None:
    """
    Executes actions until the current time is 06:00.
    If the program is paused, execution is stopped.
    """
    while not (datetime.now().hour == 6 and datetime.now().minute == 0):
        if Status.is_paused():
            break
        executeAction()

    if datetime.now().hour == 6 and datetime.now().minute == 0:
        Status.exit()
