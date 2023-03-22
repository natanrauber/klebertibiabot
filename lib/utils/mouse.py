from ctypes import windll

import win32api
import win32con


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
    def set_pos(pos: tuple) -> None:
        """
        Sets the position of the mouse.

        Args:
            pos (tuple): The x and y coordinates of the mouse position.
        """
        win32api.SetCursorPos(pos)

    @staticmethod
    def click_left(pos: tuple) -> None:
        """
        Simulates a left mouse click at the specified position.

        Args:
            pos (tuple): The x and y coordinates of the mouse position.
        """
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,  0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    @staticmethod
    def press_left(pos: tuple) -> None:
        """
        Simulates a left mouse button press at the specified position.

        Args:
            pos (tuple): The x and y coordinates of the mouse position.
        """
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,  0, 0)

    @staticmethod
    def release_left(pos: tuple) -> None:
        """
        Simulates a left mouse button release at the specified position.

        Args:
            pos (tuple): The x and y coordinates of the mouse position.
        """
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
