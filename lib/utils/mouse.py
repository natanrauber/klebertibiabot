import random
import time
from ctypes import windll
from typing import Optional

import win32api
import win32con

from lib.config import getOTServer, getScreenCenterX, getScreenCenterY, getSqmSize
from lib.utils.console import Console
from lib.utils.math import Math


class Mouse:
    """
    A class for simulating mouse input.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    _lock: bool = False

    @staticmethod
    def is_locked() -> bool:
        """
        Returns True if the mouse is locked, False otherwise.

        Returns:
            bool: True if the mouse is locked, False otherwise.
        """
        return Mouse._lock

    @staticmethod
    def lock(value: bool) -> None:
        """
        Locks or unlocks the mouse.

        Args:
            value (bool): True to lock the mouse, False to unlock it.
        """
        Mouse._lock = value
        windll.user32.BlockInput(value)

    @staticmethod
    def get_pos() -> tuple:
        """
        Returns the current position of the mouse.

        Returns:
            tuple: The x and y coordinates of the mouse position.
        """
        return win32api.GetCursorPos()

    @staticmethod
    def set_pos(
        end_pos: tuple,
        duration: float = 0.1,
        useOffSet: Optional[bool] = None,
    ) -> None:
        if useOffSet == None:
            useOffSet = not getOTServer()
        if getOTServer():
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
                noise_x = random.randint(-10, 10)  # Adjust the range of noise as needed
                noise_y = random.randint(-10, 10)  # Adjust the range of noise as needed
                new_x += noise_x
                new_y += noise_y
                win32api.SetCursorPos((new_x, new_y))
            win32api.SetCursorPos(end_pos)

    @staticmethod
    def click_left(pos: tuple, duration: float = 0.1) -> None:
        """
        Simulates a left mouse click at the specified position.

        Args:
            pos (tuple): The x and y coordinates of the mouse position.
        """
        Mouse.set_pos(pos, duration=duration)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    @staticmethod
    def press_left(pos: tuple) -> None:
        """
        Simulates a left mouse button press at the specified position.

        Args:
            pos (tuple): The x and y coordinates of the mouse position.
        """
        Mouse.set_pos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

    @staticmethod
    def release_left(pos: tuple) -> None:
        """
        Simulates a left mouse button release at the specified position.

        Args:
            pos (tuple): The x and y coordinates of the mouse position.
        """
        Mouse.set_pos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
