import time
from datetime import datetime
from os import listdir
from os.path import isfile, join
from typing import Optional

import pyautogui
from pyscreeze import Box

from lib.actions.attack.attack import (attack, disable_attack, enable_attack,
                                       hasTarget)
from lib.config import *
from lib.utils.console import Colors, Console
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import getMap, locateMap
from lib.utils.keyboard import Keyboard
from lib.utils.mouse import Mouse
from lib.utils.status import Status

_lastWalkTime = None
_walk_cooldown = 1

_try = 0


def getHuntList() -> list:
    list = [
        d
        for d in os.listdir(WAYPOINTS_DIR)
        if os.path.isdir(os.path.join(WAYPOINTS_DIR, d))
    ]
    list.insert(0, "")
    return list


SELECTED_HUNT: str = ""
_waypoints = []


def setHunt(value: str):
    global SELECTED_HUNT
    SELECTED_HUNT = f"{WAYPOINTS_DIR}/{value}/"
    global _waypoints
    _waypoints = [
        SELECTED_HUNT + f
        for f in listdir(SELECTED_HUNT)
        if isfile(join(SELECTED_HUNT, f))
    ]


def setupWalk():
    locateMap()


def _locateOnMap(image):
    return ImageLocator.get_pos_on_region(image, getMap(), grayscale=True)


def _locateOnMapCenter(image, size=28) -> Optional[Box]:
    if type(getMap()) == Box:
        _centerx = int(getMap().left + (getMap().width / 2))
        _centery = int(getMap().top + (getMap().height / 2))
        _region = Box(
            int(_centerx - (size / 2)), int(_centery - (size / 2)), size, size
        )
        return ImageLocator.get_pos_on_region(image, region=_region, grayscale=True)


def _getWaypointName(image):
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux) - 1]
    return aux


def _walk(box: Box):
    if Status.is_paused():
        return
    if Mouse.is_locked():
        time.sleep(0.1)
        return _walk(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    if getProjector():
        Mouse.click_left((box.left + 3, box.top + 3 + 350))
    else:
        Mouse.click_left((box.left + 3, box.top + 3))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)
    global _lastWalkTime
    _lastWalkTime = datetime.now()
    global _try
    _try = _try + 1


def walkOnCooldown():
    if _lastWalkTime == None:
        return False
    return (datetime.now() - _lastWalkTime).seconds < _walk_cooldown


def _repeatLastWaypoint():
    _waypoint = _waypoints[len(_waypoints) - 1]
    _waypoints.remove(_waypoint)
    _waypoints.insert(0, _waypoint)

    global _maybe_stuck
    _maybe_stuck = True
    pyautogui.screenshot(f"{TEMP_DIR}/lastgetMap()_view.png", region=getMap())


def _reachedLastWaypoint():
    _waypoint = _waypoints[len(_waypoints) - 1]
    _name = _getWaypointName(_waypoint)
    _box = None

    if _try == 10:
        for i in range(10):
            _stack_items()
        for i in range(3):
            _destroy_items()
        for i in range(10):
            _stack_items()
        return True

    if "stairs" in _name or "hole" in _name:
        return not _isLastWaypointVisible()
    elif "ladder" in _name or "ropespot" in _name:
        if not _isLastWaypointVisible():
            return True
        _box = _locateOnMapCenter(_waypoint, size=8)
    else:
        _box = _locateOnMapCenter(_waypoint)

    return type(_box) == Box


def _isLastWaypointVisible():
    _waypoint = _waypoints[len(_waypoints) - 1]
    _box = ImageLocator.get_pos_on_region(_waypoint, getMap(), grayscale=True)
    if type(_box) == Box:
        return True
    return False


_maybe_stuck = False


def _maybeStuck():
    global _maybe_stuck
    return _maybe_stuck


def _isStuck():
    if _maybeStuck():
        _last_map_view = f"{TEMP_DIR}/lastgetMap()_view.png"
        _box = ImageLocator.get_pos(_last_map_view)
        if type(_box) == Box:
            return True
    return False


def _unstuck():
    global _maybe_stuck
    _maybe_stuck = False
    if hasTarget():
        attack()


def _checkLastWaypointSpecial():
    _waypoint = _waypoints[len(_waypoints) - 1]

    if "ladder" in _getWaypointName(_waypoint):
        if _isLastWaypointVisible():
            _useLadder()
    if "ropespot" in _getWaypointName(_waypoint):
        if _isLastWaypointVisible():
            _useRope()
    if "enable_attack" in _getWaypointName(_waypoint):
        enable_attack()
    elif "disable_attack" in _getWaypointName(_waypoint):
        disable_attack()


def _stack_items():
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX(), getScreenCenterY() - getSqmSize()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX() - getSqmSize(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX(), getScreenCenterY() + getSqmSize()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX() + getSqmSize(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left(
        (
            getScreenCenterX() + (getSqmSize() * 2),
            getScreenCenterY() - (getSqmSize() * 2),
        )
    )
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX(), getScreenCenterY() - getSqmSize()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY() - (getSqmSize() * 2)))
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left(
        (
            getScreenCenterX() - (getSqmSize() * 2),
            getScreenCenterY() - (getSqmSize() * 2),
        )
    )
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX() - getSqmSize(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX() - (getSqmSize() * 2), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left(
        (
            getScreenCenterX() - (getSqmSize() * 2),
            getScreenCenterY() + (getSqmSize() * 2),
        )
    )
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX(), getScreenCenterY() + getSqmSize()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX(), getScreenCenterY() + (getSqmSize() * 2)))
    time.sleep(0.01)
    Mouse.press_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(0.01)
    Mouse.release_left(
        (
            getScreenCenterX() + (getSqmSize() * 2),
            getScreenCenterY() + (getSqmSize() * 2),
        )
    )
    time.sleep(0.01)
    Mouse.press_left((getScreenCenterX() + getSqmSize(), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.release_left((getScreenCenterX() + (getSqmSize() * 2), getScreenCenterY()))
    time.sleep(0.01)
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def _destroy_items():
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    time.sleep(0.01)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left((getScreenCenterX(), getScreenCenterY() - getSqmSize()))
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left((getScreenCenterX() - getSqmSize(), getScreenCenterY()))
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left((getScreenCenterX(), getScreenCenterY() + getSqmSize()))
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left((getScreenCenterX() + getSqmSize(), getScreenCenterY()))
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left((getScreenCenterX(), getScreenCenterY()))
    time.sleep(0.3)
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def _useLadder():
    if Mouse.is_locked():
        time.sleep(0.1)
        return _useLadder()
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.click_left((getScreenCenterX(), getScreenCenterY()))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def _useRope():
    if Mouse.is_locked():
        time.sleep(0.1)
        return _useRope()
    if _try == 10:
        return _rope_all()
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(ROPE_KEY)
    Mouse.click_left((getScreenCenterX(), getScreenCenterY()))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def _rope_all():
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left((getScreenCenterX(), getScreenCenterY() - getSqmSize()))
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() - getSqmSize())
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left((getScreenCenterX() - getSqmSize(), getScreenCenterY()))
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (getScreenCenterX() - getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left((getScreenCenterX(), getScreenCenterY() + getSqmSize()))
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (getScreenCenterX() + getSqmSize(), getScreenCenterY() + getSqmSize())
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left((getScreenCenterX() + getSqmSize(), getScreenCenterY()))
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left((getScreenCenterX(), getScreenCenterY()))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def walk():
    if len(_waypoints) == 0:
        Console.log(f"No hunt selected")
        return
    if not _lastWalkTime == None:
        if _reachedLastWaypoint():
            _checkLastWaypointSpecial()
            global _try
            _try = 0
        else:
            if _isLastWaypointVisible():
                if _isStuck():
                    return _unstuck()
                _repeatLastWaypoint()
    _waypoint = _waypoints[0]
    _box = _locateOnMap(_waypoint)
    if type(_box) == Box:
        Console.log(f"walking to waypoint {_getWaypointName(_waypoint)}")
        _walk(_box)
    _waypoints.remove(_waypoint)
    _waypoints.append(_waypoint)
