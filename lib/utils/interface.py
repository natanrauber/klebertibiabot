from typing import List, Optional

import pyautogui
from pyscreeze import Box

from lib.config import Config
from lib.utils.console import Console
from lib.utils.dir import Dir
from lib.utils.image_locator import ImageLocator
from lib.utils.status import Status

# battle
_battle_window_header = f"{Dir.INTERFACE}/battle_window_title.png"
_battle_window_footer = f"{Dir.INTERFACE}/window_footer.png"
battle_window: Box = Box(0, 0, 0, 0)

# stats
_stop_button = f"{Dir.INTERFACE}/stop_button.png"
stats_window: Box = Box(0, 0, 0, 0)

# screen center
_local_chat = f"{Dir.INTERFACE}/local_chat.png"
_store_button1 = f"{Dir.INTERFACE}/store_button1.png"
_store_button2 = f"{Dir.INTERFACE}/store_button2.png"
_store_button3 = f"{Dir.INTERFACE}/store_button3.png"
game_window: Box = Box(0, 0, 0, 0)
center_sqm: Box = Box(0, 0, 0, 0)

# containers
_container_window_footer = f"{Dir.INTERFACE}/window_footer.png"
container_window_list: List[Box] = []
selected_container: str = ""

# health bar
_health_bar_list = Dir.getFiles(Dir.HEALTH)
health_bar: Box = Box(0, 0, 0, 0)

# map
_map_controls = f"{Dir.INTERFACE}/map_controls.png"
map: Box = Box(0, 0, 0, 0)


class GameUI:
    # battle
    @staticmethod
    def getBattleWindow() -> Box:
        global battle_window
        return battle_window

    @staticmethod
    def locateBattleWindow():
        global battle_window
        try:
            _box = ImageLocator.locate_window(
                _battle_window_header, _battle_window_footer, save_as="battle"
            )
            if isinstance(_box, Box):
                battle_window = _box
            else:
                Console.log("cannot find battle window")
                Status.exit()
        except Exception:
            Console.log("cannot find battle window")
            Status.exit()

    # stats
    @staticmethod
    def getStatsWindow() -> Box:
        global stats_window
        return stats_window

    @staticmethod
    def locateStatsWindow():
        global stats_window
        try:
            _box = ImageLocator.get_pos(_stop_button)
            if isinstance(_box, Box):
                stats_window = Box(_box.left - 118, _box.top, 108, 13)
                screenshot_path = f"{Dir.SESSION}/stats_window.png"
                pyautogui.screenshot(screenshot_path, region=stats_window)
            else:
                Console.log("Cannot find stats window")
                Status.exit()
        except Exception:
            Console.log("Cannot find stats window")
            Status.exit()

    # screen center
    @staticmethod
    def getGameWindow() -> Box:
        global game_window
        return game_window

    @staticmethod
    def getGameWindowCenter() -> Box:
        global center_sqm
        return center_sqm

    @staticmethod
    def locateGameWindow():
        global game_window
        global center_sqm
        try:
            _box1 = ImageLocator.get_pos(_local_chat)
            _box2 = ImageLocator.get_pos(_store_button1)
            if not isinstance(_box2, Box):
                _box2 = ImageLocator.get_pos(_store_button2)
            if not isinstance(_box2, Box):
                _box2 = ImageLocator.get_pos(_store_button3)
            if isinstance(_box1, Box) and isinstance(_box2, Box):
                _box1 = Box(_box1.left - 13, _box1.top - 84, 50, 50)
                _box2 = Box(_box2.left - 13, _box2.top + 23, 50, 50)
                width = _box2.left - _box1.left
                height = _box1.top - _box2.top
                Config.setScreenCenter(
                    _box1.left + (width // 2),
                    _box2.top + (height // 2),
                )
                Config.setSqmSize(width // 15)
                game_window = Box(_box1.left, _box2.top, width, height)
                center_sqm = Box(
                    Config.getScreenCenterX() - (Config.getSqmSize() // 2),
                    Config.getScreenCenterY() - (Config.getSqmSize() // 2),
                    Config.getSqmSize(),
                    Config.getSqmSize(),
                )
                pyautogui.screenshot(
                    f"{Dir.SESSION}/game_window.png", region=game_window
                )
                pyautogui.screenshot(
                    f"{Dir.SESSION}/center_sqm.png",
                    region=center_sqm,
                )
            else:
                Console.log("Cannot find screen center")
                Status.exit()
        except Exception:
            Console.log("Cannot find screen center")
            Status.exit()

    # containers
    @staticmethod
    def getContainerList() -> list[str]:
        container_list: list[str] = Dir.getFiles(
            Dir.CONTAINERS,
            fullPath=False,
            rstrip=-4,
        )
        container_list.insert(0, "")
        return container_list

    @staticmethod
    def getSelectedContainer():
        global selected_container
        return selected_container

    @staticmethod
    def setContainer(value: str):
        global selected_container
        selected_container = value

    @staticmethod
    def getContainerWindows() -> List[Box]:
        global container_window_list
        return container_window_list

    @staticmethod
    def locateDropContainer():
        global container_window_list
        try:
            _boxes = ImageLocator.locate_all_windows(
                f"{Dir.CONTAINERS}/{GameUI.getSelectedContainer()}.png",
                _container_window_footer,
                save_as="container",
            )
            if _boxes is None:
                Console.log("Cannot find any container")
            else:
                container_window_list = _boxes
        except Exception:
            Console.log("Cannot find any container")
            Status.exit()

    # health bar
    @staticmethod
    def getHealthBar():
        global health_bar
        return health_bar

    @staticmethod
    def locateHealthBar():
        global health_bar
        try:
            _box: Optional[Box] = None
            for i in _health_bar_list:
                _box = ImageLocator.get_pos(i)
                if isinstance(_box, Box):
                    break
            if isinstance(_box, Box):
                health_bar = Box(_box.left, _box.top, 269, 16)
                screenshot_path = f"{Dir.SESSION}/health.png"
                pyautogui.screenshot(screenshot_path, region=health_bar)
            else:
                Console.log("Cannot find health bar")
                Status.exit()
        except Exception:
            Console.log("Cannot find health bar")
            Status.exit()

    # map
    @staticmethod
    def getMap():
        global map
        return map

    @staticmethod
    def locateMap():
        global map
        try:
            _box = ImageLocator.get_pos(_map_controls)
            if isinstance(_box, Box):
                map = Box(_box.left - 117, _box.top - 50, 106, 109)
                pyautogui.screenshot(f"{Dir.SESSION}/map.png", region=map)
                pyautogui.screenshot(
                    f"{Dir.TEMP}/last_map_view.png",
                    region=map,
                )
            else:
                Console.log("Cannot find map")
                Status.exit()
        except Exception:
            Console.log("Cannot find map")
            Status.exit()
