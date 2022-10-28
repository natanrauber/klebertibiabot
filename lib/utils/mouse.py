from ctypes import *

import win32api
import win32con

_lock = False


class Mouse:
    def isLocked():
        return _lock

    def lock(value: bool):
        global _lock
        _lock = value
        windll.user32.BlockInput(value)

    def getPos():
        return win32api.GetCursorPos()

    def setPos(pos: tuple):
        win32api.SetCursorPos(pos)

    def clickLeft(pos: tuple):
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,  0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def pressLeft(pos: tuple):
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,  0, 0)

    def releaseLeft(pos: tuple):
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
