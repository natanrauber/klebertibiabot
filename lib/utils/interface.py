from ntpath import join
from os import listdir
from typing import List, Optional

import pyautogui
from genericpath import isfile
from pyscreeze import Box

from lib.config import *
from lib.utils.colors import Colors
from lib.utils.console import Console
from lib.utils.cwd import CWD
from lib.utils.image_locator import ImageLocator
from lib.utils.status import Status

# BATTLE
_battle_window_header = CWD + "/images/interface/battle_window_title.png"
_battle_window_footer = CWD + "/images/interface/window_footer.png"
_battle_window: Box = Box(0, 0, 0, 0)


def getBattleWindow() -> Box:
    global _battle_window
    return _battle_window


def locateBattleWindow():
    global _battle_window
    try:
        _box = ImageLocator.locate_window(
            _battle_window_header, _battle_window_footer, save_as="battle"
        )
        if type(_box) == Box:
            _battle_window = _box
        else:
            Console.log("cannot find battle window", color=Colors.red)
            Status.exit()
    except:
        Console.log("cannot find battle window", color=Colors.red)
        Status.exit()


# STATS
_stop_button = CWD + "/images/interface/stop_button.png"
_stats_window: Box = Box(0, 0, 0, 0)


def getStatsWindow() -> Box:
    global _stats_window
    return _stats_window


def locateStatsWindow():
    global _stats_window
    try:
        _box = ImageLocator.get_pos(_stop_button)
        if type(_box) == Box:
            _stats_window = Box(_box.left - 118, _box.top, 108, 13)
            screenshot_path = f"{SESSION_DIR}/stats_window.png"
            pyautogui.screenshot(screenshot_path, region=_stats_window)
        else:
            Console.log("Cannot find stats window", color=Colors.red)
            Status.exit()
    except:
        Console.log("Cannot find stats window", color=Colors.red)
        Status.exit()


# SCREEN CENTER
_local_chat = CWD + "/images/interface/local_chat.png"
_store_button = CWD + "/images/interface/store_button.png"
_store_button_alt = CWD + "/images/interface/store_button_alt.png"
_game_window: Box = Box(0, 0, 0, 0)
_game_window_center: Box = Box(0, 0, 0, 0)


def getGameWindow() -> Box:
    global _game_window
    return _game_window


def getGameWindowCenter() -> Box:
    global _game_window_center
    return _game_window_center


def locateGameWindow():
    global _game_window
    global _game_window_center
    try:
        _box1 = ImageLocator.get_pos(_local_chat)
        _box2 = ImageLocator.get_pos(_store_button)
        if not type(_box2) == Box:
            _box2 = ImageLocator.get_pos(_store_button_alt)
        if type(_box1) == Box and type(_box2) == Box:
            _box1 = Box(_box1.left - 13, _box1.top - 84, 50, 50)
            _box2 = Box(_box2.left - 13, _box2.top + 23, 50, 50)
            width = _box2.left - _box1.left
            height = _box1.top - _box2.top
            setScreenCenter(_box1.left + (width // 2), _box2.top + (height // 2))
            setSqmSize(width // 15)
            _game_window = Box(_box1.left, _box2.top, width, height)
            _game_window_center = Box(
                getScreenCenterX() - (getSqmSize() // 2),
                getScreenCenterY() - (getSqmSize() // 2),
                getSqmSize(),
                getSqmSize(),
            )
            pyautogui.screenshot(f"{SESSION_DIR}/game_window.png", region=_game_window)
            pyautogui.screenshot(
                f"{SESSION_DIR}/game_window_center.png", region=_game_window_center
            )
        else:
            Console.log("Cannot find screen center", color=Colors.red)
            Status.exit()
    except:
        Console.log("Cannot find screen center", color=Colors.red)
        Status.exit()


# CONTAINERS
_containers_dir = CWD + "/images/containers"
_container_window_footer = CWD + "/images/interface/window_footer.png"
_container_window_list: Optional[List[Box]] = []
_selected_container: str = ""


def getContainerList() -> list:
    list = [f[:-4] for f in listdir(CONTAINERS_DIR) if isfile(join(CONTAINERS_DIR, f))]
    list.insert(0, "")
    return list


def getSelectedContainer():
    global _selected_container
    return _selected_container


def setContainer(value: str):
    global _selected_container
    _selected_container = value


def getContainerWindows() -> Optional[List[Box]]:
    global _container_window_list
    return _container_window_list


def locateDropContainer():
    global _container_window_list
    try:
        _boxes = ImageLocator.locate_all_windows(
            f"{_containers_dir}/{getSelectedContainer()}.png",
            _container_window_footer,
            save_as="container",
        )
        _container_window_list = _boxes
    except:
        Console.log("Cannot find any container", color=Colors.red)
        Status.exit()


# HEALTH BAR
_health_bar_dir = CWD + "/images/heal/"
_health_bar_list = [
    _health_bar_dir + f
    for f in listdir(_health_bar_dir)
    if isfile(join(_health_bar_dir, f))
]
_health_bar: Box = Box(0, 0, 0, 0)


def getHealthBar():
    global _health_bar
    return _health_bar


def locateHealthBar():
    global _health_bar
    try:
        _box: Optional[Box] = None
        for i in _health_bar_list:
            _box = ImageLocator.get_pos(i)
            if type(_box) == Box:
                break
        if type(_box) == Box:
            _health_bar = Box(_box.left, _box.top, 269, 16)
            screenshot_path = f"{SESSION_DIR}/health.png"
            pyautogui.screenshot(screenshot_path, region=_health_bar)
        else:
            Console.log("Cannot find health bar", color=Colors.red)
            Status.exit()
    except:
        Console.log("Cannot find health bar", color=Colors.red)
        Status.exit()


# MAP
_map_controls = CWD + "/images/interface/map_controls.png"
_map: Box = Box(0, 0, 0, 0)


def getMap():
    global _map
    return _map


def locateMap():
    global _map
    try:
        _box = ImageLocator.get_pos(_map_controls)
        if type(_box) == Box:
            _map = Box(_box.left - 117, _box.top - 50, 106, 109)
            pyautogui.screenshot(f"{SESSION_DIR}/map.png", region=_map)
            pyautogui.screenshot(f"{TEMP_DIR}/last_map_view.png", region=_map)
        else:
            Console.log("Cannot find map", color=Colors.red)
            Status.exit()
    except:
        Console.log("Cannot find map", color=Colors.red)
        Status.exit()
