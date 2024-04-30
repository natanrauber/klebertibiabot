import win32com.client as comclt
from win32gui import GetForegroundWindow, GetWindowText

wsh = comclt.Dispatch("WScript.Shell")


class WindowManager:

    @staticmethod
    def isActive(name: str) -> bool:
        if name in GetWindowText(GetForegroundWindow()):
            return True
        return False

    @staticmethod
    def activate(name: str) -> None:
        wsh.AppActivate(name)
