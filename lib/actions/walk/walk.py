import time
from datetime import datetime
from os import listdir
from os.path import isfile, join

from config import *
from lib.utils.gui import getPos, getPosOnRegion
from lib.utils.keyboard import Keyboard
from lib.utils.log import Colors, log
from lib.utils.mouse import Mouse
from pyscreeze import Box

_map_controls = 'C:/dev/kleber/lib/actions/walk/images/map_controls.png'
_map = None

_waypoints_dir = f'C:/dev/kleber/lib/actions/walk/waypoints/{HUNT_NAME}/'
_waypoints = [_waypoints_dir +
              f for f in listdir(_waypoints_dir) if isfile(join(_waypoints_dir, f))]

_lastWalkTime = datetime.now()
_walk_cooldown = 1


def setupWalk():
    _locateMap()


def _locateMap():
    _box = getPos(_map_controls)
    if _box == None:
        log('cannot find map', color=Colors.red)
        exit()
    global _map
    _map = Box(_box.left-117, _box.top-50, 106, 109)


def _locateOnMap(image):
    return getPosOnRegion(image, _map, grayscale=True)


def _locateOnMapCenter(image):
    _centerx = int(_map.left + (_map.width/2))
    _centery = int(_map.top + (_map.height/2))
    _region = (_centerx-14, _centery-14, 28, 28)
    return getPosOnRegion(image, region=_region, grayscale=True)


def _getWaypointName(image):
    aux = image.split('.')[0]
    aux = aux.split('/')
    aux = aux[len(aux)-1]
    return aux


def _walk(box: Box):
    if Mouse.isLocked():
        time.sleep(0.1)
        return _walk(box)
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.getPos()
    Mouse.clickLeft((box.left-960+3, box.top+3))
    Mouse.setPos(_initPos)
    Mouse.lock(False)
    global _lastWalkTime
    _lastWalkTime = datetime.now()


def walkOnCooldown():
    return (datetime.now() - _lastWalkTime).seconds < _walk_cooldown


def _repeatLastWaypoint():
    _waypoint = _waypoints[len(_waypoints)-1]
    _waypoints.remove(_waypoint)
    _waypoints.insert(0, _waypoint)
    log('repeating last waypoint')


def _reachedLastWaypoint():
    _waypoint = _waypoints[len(_waypoints)-1]
    if 'stairs' in _getWaypointName(_waypoint):
        return not _isLastWaypointVisible()
    _box = _locateOnMapCenter(_waypoint)
    if type(_box) == Box:
        return True
    return False


def _isLastWaypointVisible():
    _waypoint = _waypoints[len(_waypoints)-1]
    _box = getPosOnRegion(_waypoint, _map, grayscale=True)
    if type(_box) == Box:
        return True
    return False


def walk():
    if not _reachedLastWaypoint():
        if _isLastWaypointVisible():
            _repeatLastWaypoint()
    _waypoint = _waypoints[0]
    _box = _locateOnMap(_waypoint)
    if type(_box) == Box:
        log(f'walking to waypoint {_getWaypointName(_waypoint)}')
        _walk(_box)
    _waypoints.remove(_waypoint)
    _waypoints.append(_waypoint)
