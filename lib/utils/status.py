import os
import time

import pyautogui

from lib.config import SESSION_DIR, STOP_ALL_ACTIONS_KEY
from lib.uid import uid
from lib.utils.console import Colors, Console
from lib.utils.keyboard import Keyboard


class Status:
    """
    A class for managing the status of an operation.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    _is_paused: bool = True
    _sleeping: bool = False

    @staticmethod
    def get_status() -> str:
        """
        Returns the current status of the operation.

        Returns:
            str: The current status, either "PAUSED" or "RUNNING".
        """
        return "PAUSED" if Status._is_paused else "RUNNING"

    @staticmethod
    def is_paused() -> bool:
        """
        Returns whether the operation is currently paused.

        Returns:
            bool: Whether the operation is currently paused.
        """
        return Status._is_paused

    @staticmethod
    def pause() -> None:
        """
        Pauses the operation.
        """
        Status._is_paused = True
        Keyboard.press(STOP_ALL_ACTIONS_KEY)
        Console.log(Status.get_status(), color=Colors.yellow)

    @staticmethod
    def resume() -> None:
        """
        Resumes the operation.
        """
        Status._is_paused = False
        Console.log(Status.get_status(), color=Colors.yellow)

    @staticmethod
    def sleep(duration: int) -> None:
        """ """
        Status._sleep = True
        time.sleep(duration)
        Status._sleep = False

    @staticmethod
    def is_sleeping() -> bool:
        """
        Returns whether the operation is currently paused.

        Returns:
            bool: Whether the operation is currently paused.
        """
        return Status._sleeping

    @staticmethod
    def exit() -> None:
        Status.pause()
        os.system(f"taskkill /f /im {uid}.exe")
