import win32com.client as comclt
from win32gui import GetForegroundWindow, GetWindowText

wsh = comclt.Dispatch("WScript.Shell")


class WindowManager:
    """
    A class that provides methods for managing windows.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    @staticmethod
    def isActive(name: str) -> bool:
        if name in GetWindowText(GetForegroundWindow()):
            return True
        return False

    @staticmethod
    def activate(name: str) -> None:
        wsh.AppActivate(name)
