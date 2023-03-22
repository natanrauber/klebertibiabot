import os

import cv2
import numpy as np
import pyautogui
from pyscreeze import Box
from screeninfo import get_monitors
from win32gui import GetForegroundWindow, GetWindowText

from config import SESSION_DIR
from lib.utils.character import _CHAR_NAME
from lib.utils.wsh import wsh

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
    wsh.AppActivate('Kleber')
    wsh.AppActivate(f'Tibia - {_CHAR_NAME}')


def getPos(image, grayscale=False, confidence=0.9):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(
        image, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)
    if len(loc[0]) > 0:
        left = loc[1][0]
        top = loc[0][0]
        right = left + template.shape[1]
        bottom = top + template.shape[0]
        return Box(left, top, right, bottom)
    else:
        return None


def getAllPos(image, grayscale=False, confidence=0.9):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(
        image, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)
    boxes = []
    for pt in zip(*loc[::-1]):
        left = pt[0]
        top = pt[1]
        right = left + template.shape[1]
        bottom = top + template.shape[0]
        boxes.append(Box(left, top, right, bottom))
    return boxes


def getPosOnRegion(image, region, grayscale=False, confidence=0.9):
    _box = pyautogui.locateOnScreen(
        image, region=region, grayscale=grayscale, confidence=confidence)
    return _box


def locateWindow(image, save_as=None):
    header = getPos(image)
    if header is None:
        return None
    try:
        footer = None
        for i in range(int((get_monitors()[0].height - header.top) / 100)):
            region = (header.left, header.top, header.width, (i + 1) * 100)
            footer = getPosOnRegion(_window_footer, region)
            if footer is not None:
                break
        if footer is None:
            region = (header.left, header.top, header.width,
                      get_monitors()[0].height - header.top)
            footer = getPosOnRegion(_window_footer, region)
        if footer is None:
            return None
        window = Box(header.left, header.top, footer.left + footer.width -
                     header.left, footer.top + footer.height - header.top)
        if save_as is not None and isinstance(window, Box):
            screenshot_path = f"{SESSION_DIR}/{save_as}.png"
            pyautogui.screenshot(screenshot_path, region=window)
        return window
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def locateAllWindows(image, save_as=None):
    windows = []
    try:
        for header in getAllPos(image):
            footer = None
            for i in range(int(get_monitors()[0].height - header.top) // 100):
                region = (header.left, header.top, header.width, (i + 1) * 100)
                footer = getPosOnRegion(_window_footer, region)
                if footer is not None:
                    break
            if footer is None:
                region = (header.left, header.top, header.width,
                          get_monitors()[0].height - header.top)
                footer = getPosOnRegion(_window_footer, region)
            if isinstance(footer, Box):
                window = Box(header.left, header.top, footer.left + footer.width -
                             header.left, footer.top + footer.height - header.top)
                if isinstance(window, Box):
                    if save_as is not None:
                        screenshot_path = f"{SESSION_DIR}/{save_as}{len(windows)}.png"
                        pyautogui.screenshot(screenshot_path, region=window)
                    windows.append(window)
        return windows
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def openFolder(folder):
    os.startfile(folder)
