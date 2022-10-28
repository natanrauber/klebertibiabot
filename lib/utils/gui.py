import os
import pyautogui
from config import SESSION_DIR
from lib.utils.character import _CHAR_NAME
from lib.utils.wsh import wsh
from pyscreeze import Box
from screeninfo import get_monitors
from win32gui import GetForegroundWindow, GetWindowText


_interface_dir = 'C:/dev/kleber/images/interface'
_window_footer = f'{_interface_dir}/window_footer.png'


def checkActiveWindows():
    if isTibiaActive():
        return
    activateAllWindows()


def getWindowName():
    return GetWindowText(GetForegroundWindow())


def isTibiaActive():
    if 'Tibia' in getWindowName():
        return True
    return False


def activateAllWindows():
    wsh.AppActivate('Projetor em janela (prévia)')
    wsh.AppActivate(f'Tibia - {_CHAR_NAME}')


def getPos(image, grayscale=False, confidence=0.9):
    _box = pyautogui.locateOnScreen(
        image, grayscale=grayscale, confidence=confidence)
    return _box


def getAllPos(image, grayscale=False, confidence=0.9):
    return pyautogui.locateAllOnScreen(
        image, grayscale=grayscale, confidence=confidence)


def getPosOnRegion(image, region, grayscale=False, confidence=0.9):
    _box = pyautogui.locateOnScreen(
        image, region=region, grayscale=grayscale, confidence=confidence)
    return _box


def locateWindow(image, save_as=None):
    _header = getPos(image)
    if _header == None:
        return None
    try:
        for i in range(int((get_monitors()[0].height-_header.top)/100)):
            _region = (_header.left, _header.top, _header.width, (i+1)*100)
            _footer = getPosOnRegion(_window_footer, _region)
            if _footer != None:
                break
        if _footer == None:
            _region = (_header.left, _header.top, _header.width,
                       get_monitors()[0].height-_header.top)
            _footer = getPosOnRegion(_window_footer, _region)
        if _footer == None:
            return None
        global _window
        _window = Box(
            _header.left, _header.top, _footer.left+_footer.width-_header.left, _footer.top+_footer.height-_header.top)
        if save_as != None and type(_window) == Box:
            pyautogui.screenshot(
                f'{SESSION_DIR}/{save_as}.png', region=_window)
        return _window
    except:
        return None


def locateAllWindows(image, save_as=None):
    try:
        _windows = []
        for _header in getAllPos(image):
            for i in range(int((get_monitors()[0].height-_header.top)/100)):
                _region = (_header.left, _header.top,
                           _header.width, (i+1)*100)
                _footer = getPosOnRegion(_window_footer, _region)
                if _footer != None:
                    break
            if _footer == None:
                _region = (_header.left, _header.top, _header.width,
                           get_monitors()[0].height-_header.top)
                _footer = getPosOnRegion(_window_footer, _region)
            if type(_footer) == Box:
                global _window
                _window = Box(
                    _header.left, _header.top, _footer.left+_footer.width-_header.left, _footer.top+_footer.height-_header.top)
                if type(_window) == Box:
                    if save_as != None and type(_window) == Box:
                        pyautogui.screenshot(
                            f'{SESSION_DIR}/{save_as}{len(_windows)}.png', region=_window)
                    _windows.append(_window)
        return _windows
    except:
        return None


def openFolder(folder):
    os.startfile(folder)
