import os
import time

from lib.config import STOP_ALL_ACTIONS_KEY
from lib.uid import uid
from lib.utils.console import Console
from lib.utils.keyboard import Keyboard


class Status:

    _is_paused: bool = True
    _sleeping: bool = False

    @staticmethod
    def get_status() -> str:
        return "PAUSED" if Status._is_paused else "RUNNING"

    @staticmethod
    def is_paused() -> bool:
        return Status._is_paused

    @staticmethod
    def pause() -> None:
        Status._is_paused = True
        Keyboard.press(STOP_ALL_ACTIONS_KEY)
        Console.log(Status.get_status())

    @staticmethod
    def resume() -> None:
        Status._is_paused = False
        Console.log(Status.get_status())

    @staticmethod
    def sleep(duration: int) -> None:
        Status._sleep = True
        time.sleep(duration)
        Status._sleep = False

    @staticmethod
    def is_sleeping() -> bool:
        return Status._sleeping

    @staticmethod
    def exit() -> None:
        Status.pause()
        os.system(f"taskkill /f /im {uid}.exe")
