import time
from datetime import datetime

from lib.config import STRIKE_KEY
from lib.utils.keyboard import Keyboard

_last_used_time: datetime = datetime.now()


class Strike:
    @staticmethod
    def use() -> None:
        global _last_used_time
        _last_used_time = datetime.now()
        Keyboard.press(STRIKE_KEY)
        time.sleep(0.1)

    @staticmethod
    def onCooldown() -> bool:
        if (datetime.now() - _last_used_time).seconds < 1:
            return True
        return False
