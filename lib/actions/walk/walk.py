import time
from datetime import datetime
from os import listdir
from os.path import isfile, join
from typing import Optional

import pyautogui
from pyscreeze import Box

from config import *
from lib.actions.attack.attack import (attack, disable_attack, enable_attack,
                                       hasTarget)
from lib.utils.console import Colors, Console
from lib.utils.image_locator import ImageLocator
from lib.utils.keyboard import Keyboard
from lib.utils.mouse import Mouse

_map_controls = 'C:/dev/kleber/lib/actions/walk/images/map_controls.png'
_map: Optional[Box] = None

_waypoints_dir = f'C:/dev/kleber/lib/actions/walk/waypoints/{HUNT_NAME}/'
_waypoints = [_waypoints_dir +
              f for f in listdir(_waypoints_dir) if isfile(join(_waypoints_dir, f))]

_lastWalkTime = None
_walk_cooldown = 1


def setupWalk():
    _locateMap()


def _locateMap():
    _box = ImageLocator.get_pos(_map_controls)
    if _box == None:
        Console.log('cannot find map', color=Colors.red)
        exit()
    global _map
    _map = Box(_box.left-117, _box.top-50, 106, 109)
    pyautogui.screenshot(
        f'{SESSION_DIR}/map.png', region=_map)
    pyautogui.screenshot(
        f'{TEMP_DIR}/last_map_view.png', region=_map)


def _locateOnMap(image):
    return ImageLocator.get_pos_on_region(image, _map, grayscale=True)


def _locateOnMapCenter(image, size=28) -> Optional[Box]:
    if type(_map) == Box:
        _centerx = int(_map.left + (_map.width/2))
        _centery = int(_map.top + (_map.height/2))
        _region = Box(int(_centerx-(size/2)),
                      int(_centery-(size/2)), size, size)
        return ImageLocator.get_pos_on_region(image, region=_region, grayscale=True)


def _getWaypointName(image):
    aux = image.split('.')[0]
    aux = aux.split('/')
    aux = aux[len(aux)-1]
    return aux


def _walk(box: Box):
    if Mouse.is_locked():
        time.sleep(0.1)
        return _walk(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.click_left((box.left-900+3, box.top+3))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)
    global _lastWalkTime
    _lastWalkTime = datetime.now()


def walkOnCooldown():
    if _lastWalkTime == None:
        return False
    return (datetime.now() - _lastWalkTime).seconds < _walk_cooldown


def _repeatLastWaypoint():
    _waypoint = _waypoints[len(_waypoints)-1]
    _waypoints.remove(_waypoint)
    _waypoints.insert(0, _waypoint)

    global _maybe_stuck
    _maybe_stuck = True
    pyautogui.screenshot(
        f'{TEMP_DIR}/last_map_view.png', region=_map)


def _reachedLastWaypoint():
    _waypoint = _waypoints[len(_waypoints)-1]
    _name = _getWaypointName(_waypoint)
    _box = None

    if 'stairs' in _name or 'hole' in _name:
        return not _isLastWaypointVisible()
    elif 'ladder' in _name or 'ropespot' in _name:
        if not _isLastWaypointVisible():
            return True
        _box = _locateOnMapCenter(_waypoint, size=8)
    else:
        _box = _locateOnMapCenter(_waypoint)

    return type(_box) == Box


def _isLastWaypointVisible():
    _waypoint = _waypoints[len(_waypoints)-1]
    _box = ImageLocator.get_pos_on_region(_waypoint, _map, grayscale=True)
    if type(_box) == Box:
        return True
    return False


_maybe_stuck = False


def _maybeStuck():
    global _maybe_stuck
    return _maybe_stuck


def _isStuck():
    if _maybeStuck():
        _last_map_view = f'{TEMP_DIR}/last_map_view.png'
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
    _waypoint = _waypoints[len(_waypoints)-1]

    if 'ladder' in _getWaypointName(_waypoint):
        if _isLastWaypointVisible():
            _useLadder()
    if 'ropespot' in _getWaypointName(_waypoint):
        if _isLastWaypointVisible():
            _useRope()
    if 'enable_attack' in _getWaypointName(_waypoint):
        enable_attack()
    elif 'disable_attack' in _getWaypointName(_waypoint):
        disable_attack()


def _useLadder():
    if Mouse.is_locked():
        time.sleep(0.1)
        return _useLadder()
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.click_left((SCREEN_CENTER_X, SCREEN_CENTER_Y))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def _useRope():
    if Mouse.is_locked():
        time.sleep(0.1)
        return _useRope()
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(ROPE_KEY)
    Mouse.click_left((SCREEN_CENTER_X, SCREEN_CENTER_Y))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)


def walk():
    if not _lastWalkTime == None:
        if _reachedLastWaypoint():
            _checkLastWaypointSpecial()
        else:
            if _isLastWaypointVisible():
                if _isStuck():
                    return _unstuck()
                _repeatLastWaypoint()
    _waypoint = _waypoints[0]
    _box = _locateOnMap(_waypoint)
    if type(_box) == Box:
        Console.log(f'walking to waypoint {_getWaypointName(_waypoint)}')
        _walk(_box)
    _waypoints.remove(_waypoint)
    _waypoints.append(_waypoint)
