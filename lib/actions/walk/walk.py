import time
import pyautogui
import win32api
import win32con
from datetime import datetime
from os.path import isfile, join
from os import listdir
from pyscreeze import Box
from config import *
from lib.utils.keyboard import keyboard_controller
from lib.utils.mouse import isMouseLocked, lockMouse, unlockMouse
from lib.utils.log import log

_dir = "C:/dev/kleber/lib/actions/walk/waypoints"
_waypoints = [_dir +
              f for f in listdir(_dir) if isfile(join(_dir, f))]

dirMap = "C:/dev/kleber/images/waypoints/map/"
dirScreen = "C:/dev/kleber/images/waypoints/screen/"

waypointsMap = [dirMap + f for f in listdir(dirMap) if isfile(join(dirMap, f))]
waypointsScreen = [dirScreen +
                   f for f in listdir(dirScreen) if isfile(join(dirScreen, f))]

_lastWalkTime = datetime.now()


def locateOnMap(image):
    _region = (MAP_AREA_LEFT, MAP_AREA_TOP,
               MAP_AREA_WIDTH, MAP_AREA_HEIGHT)
    box = pyautogui.locateOnScreen(
        image, region=_region, grayscale=True, confidence=0.9)
    if box != None:
        return box


def locateOnScreen(image):
    _region = (WALK_AREA_LEFT, WALK_AREA_TOP,
               WALK_AREA_WIDTH, WALK_AREA_HEIGHT)
    box = pyautogui.locateOnScreen(
        image, region=_region, grayscale=True, confidence=0.7)
    if box != None:
        return box


def _getWaypointName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux)-1]
    return aux


def _walk(box: Box, isMap: bool):
    keyboard_controller.tap(STOP_ALL_ACTIONS_KEY)
    lockMouse()
    _initPos = pyautogui.position()
    offset = 4 if isMap else int(SQM_SIZE / 2)
    win32api.SetCursorPos((box.left-960+offset, box.top+offset))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.SetCursorPos(_initPos)
    unlockMouse()
    global _lastWalkTime
    _lastWalkTime = datetime.now()
    time.sleep(3)


def _onCooldown():
    return (datetime.now() - _lastWalkTime).seconds < WALK_COOLDOWN


def walk():
    if _onCooldown():
        return
    for image in waypointsMap:
        _box = locateOnMap(image)
        _found = type(_box) == Box
        if _found and not isMouseLocked():
            log("walking {}...".format(_getWaypointName(image)))
            return _walk(_box, True)
    for image in waypointsScreen:
        _box = locateOnScreen(image)
        _found = type(_box) == Box
        if _found and not isMouseLocked():
            log("walking {}...".format(_getWaypointName(image)))
            return _walk(_box, False)
