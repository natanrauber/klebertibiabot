from win32gui import GetWindowText, GetForegroundWindow
from lib.utils.wsh import wsh
from lib.utils.character import _CHAR_NAME


def checkActiveWindows():
    if isTibiaActive():
        return
    activateAllWindows()


def getWindowName():
    return GetWindowText(GetForegroundWindow())


def isTibiaActive():
    if "Tibia" in getWindowName():
        return True
    return False


def activateAllWindows():
    wsh.AppActivate("Projetor em janela (prévia)")
    wsh.AppActivate(f"Tibia - {_CHAR_NAME}")
