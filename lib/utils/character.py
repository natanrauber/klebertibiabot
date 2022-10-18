from win32gui import GetWindowText, GetForegroundWindow
from lib.utils.wsh import wsh
from lib.utils.log import log

_CHAR_NAME = ""


def charName():
    return _CHAR_NAME


def validName():
    wsh.AppActivate("Tibia - {}".format(_CHAR_NAME))
    if "Tibia - {}".format(_CHAR_NAME) == GetWindowText(GetForegroundWindow()):
        wsh.AppActivate("Windows PowerShell")
        return True
    wsh.AppActivate("Windows PowerShell")
    log("cannot found Tibia window with given character name")
    return False


def getCharacterName():
    global _CHAR_NAME
    _CHAR_NAME = input("character name: ")
    while not validName():
        _CHAR_NAME = input("character name: ")
