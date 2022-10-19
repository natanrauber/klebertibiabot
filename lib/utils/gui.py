from win32gui import GetWindowText, GetForegroundWindow
from lib.utils.wsh import wsh
from lib.utils.character import _CHAR_NAME
import pyautogui
from pyscreeze import Box
from screeninfo import get_monitors


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


def getPos(image, confidence=0.9):
    _box = pyautogui.locateOnScreen(image, confidence=confidence)
    if type(_box) == Box:
        return Box(_box.left, _box.top, _box.width, _box.height)
    return None


def getPosOnRegion(image, region, grayscale=False, confidence=0.9):
    _box = pyautogui.locateOnScreen(
        image, region=region, grayscale=grayscale, confidence=confidence)
    if type(_box) == Box:
        return _box
    return None


def locateWindow(image, print=False):
    _window_footer = "C:/dev/kleber/images/other/window_footer.png"
    _header = getPos(image)
    if _header == None:
        return None
    try:
        for i in range(int((get_monitors()[0].height-_header.top)/100)):
            _region = (_header.left, _header.top, get_monitors()
                       [0].width - _header.left, (i+1)*100)
            _footer = getPosOnRegion(
                _window_footer, _region)
            if _footer != None:
                break
        if _footer == None:
            _region = (_header.left, _header.top, get_monitors()
                       [0].width - _header.left, get_monitors()[0].height-_header.top)
            _footer = getPosOnRegion(
                _window_footer, (_header.left, _header.top, get_monitors()[0].width - _header.left, get_monitors()[0].height-_header.top))
        if _footer == None:
            return None
        global _window
        _window = Box(
            _header.left, _header.top, _footer.left+_footer.width-_header.left, _footer.top+_footer.height-_header.top)
        if print and type(_window) == Box:
            pyautogui.screenshot(
                "C:/dev/kleber/images/window.png", region=_window)
        return _window
    except:
        return None
