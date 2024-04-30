import time
from datetime import datetime

import pyautogui
from pyscreeze import Box

from lib.config import ROPE_KEY, STOP_ALL_ACTIONS_KEY, Config
from lib.modules.attack import attack, disable_attack, enable_attack, hasTarget
from lib.modules.unstuck import destroy_items, rope_all, stack_items
from lib.utils.console import Console
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.interface import GameUI
from lib.utils.keyboard import Keyboard
from lib.utils.mouse import Mouse
from lib.utils.status import Status

_lastWalkTime = None
_walk_cooldown = 1

_try = 0


def getHuntList() -> list[str]:
    hunt_list = Dir.getFolders(Dir.WAYPOINTS, fullPath=False)
    hunt_list.insert(0, "")
    return hunt_list


selected_hunt_dir: str = ""
_waypoints = []


def setHunt(value: str):
    global selected_hunt_dir
    selected_hunt_dir = f"{Dir.WAYPOINTS}/{value}/"
    global _waypoints
    _waypoints = Dir.getFiles(selected_hunt_dir)


def _locateOnMap(image: str) -> Box | None:
    return ImageLocator.get_pos_on_region(
        image,
        GameUI.getMap(),
        grayscale=True,
    )


def _locateOnMapCenter(image: str, size: int = 28) -> Box | None:
    if type(GameUI.getMap()) == Box:
        _centerx = int(GameUI.getMap().left + (GameUI.getMap().width / 2))
        _centery = int(GameUI.getMap().top + (GameUI.getMap().height / 2))
        _region = Box(
            int(_centerx - (size / 2)),
            int(_centery - (size / 2)),
            size,
            size,
        )
        return ImageLocator.get_pos_on_region(
            image,
            region=_region,
            grayscale=True,
        )


def _getWaypointName(image: str) -> str:
    aux = image.split(".")[0]
    aux = aux.split("/")
    aux = aux[len(aux) - 1]
    return aux


def _walk(box: Box) -> None:
    if Status.is_paused():
        return
    if Mouse.is_locked():
        time.sleep(0.1)
        return _walk(box)
    # Keyboard.press(STOP_ALL_ACTIONS_KEY)
    # time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.click_left((box.left + 3, box.top + 3))
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)
    global _lastWalkTime
    _lastWalkTime = datetime.now()
    global _try
    _try = _try + 1


def walkOnCooldown():
    if _lastWalkTime is None:
        return False
    return (datetime.now() - _lastWalkTime).seconds < _walk_cooldown


def _repeatLastWaypoint():
    _waypoint = _waypoints[len(_waypoints) - 1]
    _waypoints.remove(_waypoint)
    _waypoints.insert(0, _waypoint)

    global _maybe_stuck
    _maybe_stuck = True
    pyautogui.screenshot(
        f"{Dir.TEMP}/lastGameUI.getMap()_view.png",
        region=GameUI.getMap(),
    )


def _reachedLastWaypoint():
    _waypoint = _waypoints[len(_waypoints) - 1]
    _name = _getWaypointName(_waypoint)
    _box = None

    if _try == 10:
        for _ in range(5):
            stack_items()
            time.sleep(0.5)
        for _ in range(3):
            destroy_items()
        for _ in range(5):
            stack_items()
            time.sleep(0.5)
        return True

    if "stairs" in _name or "hole" in _name:
        return not _isLastWaypointVisible()
    elif "ladder" in _name or "ropespot" in _name:
        if not _isLastWaypointVisible():
            return True
        _box = _locateOnMapCenter(_waypoint, size=8)
    else:
        _box = _locateOnMapCenter(_waypoint)

    return isinstance(_box, Box)


def _isLastWaypointVisible():
    _waypoint = _waypoints[len(_waypoints) - 1]
    _box = ImageLocator.get_pos_on_region(
        _waypoint,
        GameUI.getMap(),
        grayscale=True,
    )
    if isinstance(_box, Box):
        return True
    return False


_maybe_stuck = False


def _maybeStuck():
    global _maybe_stuck
    return _maybe_stuck


def _isStuck():
    if _maybeStuck():
        _last_map_view = f"{Dir.TEMP}/lastGameUI.getMap()_view.png"
        _box = ImageLocator.get_pos(_last_map_view)
        if isinstance(_box, Box):
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


def _useLadder() -> None:
    if Mouse.is_locked():
        time.sleep(0.1)
        return _useLadder()
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)


def _useRope() -> None:
    if Mouse.is_locked():
        time.sleep(0.1)
        return _useRope()
    if _try == 10:
        return rope_all()
    Keyboard.press(STOP_ALL_ACTIONS_KEY)
    time.sleep(0.5)
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)


def walk():
    if len(_waypoints) == 0:
        Console.log("No hunt selected")
        return
    if _lastWalkTime is not None:
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
    if isinstance(_box, Box):
        Console.log(f"walking to waypoint {_getWaypointName(_waypoint)}")
        _walk(_box)
    _waypoints.remove(_waypoint)
    _waypoints.append(_waypoint)
