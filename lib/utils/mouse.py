import random
import time
from ctypes import windll
from typing import Any, Optional

import win32api
import win32con

from lib.config import Config
from lib.utils.math import Math


class Mouse:

    _lock: bool = False

    @staticmethod
    def is_locked() -> bool:
        return Mouse._lock

    @staticmethod
    def lock(value: bool) -> None:
        Mouse._lock = value
        windll.user32.BlockInput(value)

    @staticmethod
    def get_pos() -> tuple[Any, Any]:
        return win32api.GetCursorPos()

    @staticmethod
    def set_pos(
        end_pos: tuple[Any, Any],
        duration: float = 0.1,
        useOffSet: Optional[bool] = None,
    ) -> None:
        if useOffSet is None:
            useOffSet = not Config.getOTServer()
        if Config.getOTServer():
            win32api.SetCursorPos(end_pos)
        else:
            if useOffSet:
                end_pos = (end_pos[0], end_pos[1] + 350)
            start_pos = Mouse.get_pos()
            start_time = time.time()
            while time.time() - start_time < duration:
                elapsed_time = time.time() - start_time
                t = min(elapsed_time / duration, 1.0)
                # Calculate point on bezier curve
                new_x, new_y = Math.bezier_curve(start_pos, end_pos, t)
                # Add noise to the curve
                noise_x = random.randint(-10, 10)
                noise_y = random.randint(-10, 10)
                new_x += noise_x
                new_y += noise_y
                win32api.SetCursorPos((new_x, new_y))
            win32api.SetCursorPos(end_pos)

    @staticmethod
    def click_left(pos: tuple[Any, Any], duration: float = 0.1) -> None:
        Mouse.set_pos(pos, duration=duration)
        win32api.mouse_event(  # type: ignore
            win32con.MOUSEEVENTF_LEFTDOWN,
            0,
            0,
        )
        win32api.mouse_event(  # type: ignore
            win32con.MOUSEEVENTF_LEFTUP,
            0,
            0,
        )

    @staticmethod
    def press_left(pos: tuple[Any, Any]) -> None:
        Mouse.set_pos(pos)
        win32api.mouse_event(  # type: ignore
            win32con.MOUSEEVENTF_LEFTDOWN,
            0,
            0,
        )

    @staticmethod
    def release_left(pos: tuple[Any, Any]) -> None:
        Mouse.set_pos(pos)
        win32api.mouse_event(  # type: ignore
            win32con.MOUSEEVENTF_LEFTUP,
            0,
            0,
        )

    @staticmethod
    def drag_left(start: tuple[Any, Any], end: tuple[Any, Any]) -> None:
        Mouse.press_left(start)
        Mouse.release_left(end)
