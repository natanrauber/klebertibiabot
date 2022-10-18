import pyautogui
from pyscreeze import Box


def getPos(image):
    _box = pyautogui.locateOnScreen(image, confidence=0.9)
    if type(_box) == Box:
        return Box(_box.left, _box.top, _box.width, _box.height)
    return None
