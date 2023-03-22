import os
from typing import List, Optional

import cv2
import numpy as np
import pyautogui
from pyscreeze import Box
from screeninfo import get_monitors
from win32gui import GetForegroundWindow, GetWindowText

from config import SESSION_DIR
from lib.utils.wsh import wsh

_interface_dir: str = 'C:/dev/kleber/images/interface'
_window_footer: str = f'{_interface_dir}/window_footer.png'


def check_active_windows(charName: str = '') -> None:
    """
    Checks if the Tibia window is currently active. If not, activates all Tibia windows with the given character name.

    Args:
        charName (str, optional): The character name used to filter the Tibia windows to be activated. Defaults to ''.
    """
    if is_tibia_active():
        return
    activate_all_windows(charName=charName)


def get_window_name() -> str:
    """
    Returns the title of the active window.

    Returns:
        str: The title of the active window.
    """
    return GetWindowText(GetForegroundWindow())


def is_tibia_active() -> bool:
    """
    Checks if the Tibia window is currently active.

    Returns:
        bool: True if the Tibia window is active, False otherwise.
    """
    if 'Tibia' in get_window_name():
        return True
    return False


def activate_all_windows(charName: str = '') -> None:
    """
    Activates all Tibia windows with the given character name.

    Args:
        charName (str, optional): The character name used to filter the Tibia windows to be activated. Defaults to ''.
    """
    wsh.AppActivate('session')
    wsh.AppActivate('Projetor em janela (prévia)')
    wsh.AppActivate('Kleber')
    wsh.AppActivate(f'Tibia - {charName}')


def get_pos(image: str, grayscale: bool = False, confidence: float = 0.9) -> Optional[Box]:
    """
    Returns the coordinates of the first match of the given image in the current screen.

    Args:
        image (str): The path of the image to search for.
        grayscale (bool, optional): Whether to search for the image in grayscale. Defaults to False.
        confidence (float, optional): The confidence level of the match. Defaults to 0.9.

    Returns:
        Optional[Box]: The coordinates of the first match of the given image in the current screen, or None if no match is found.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(
        image, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= np.full(res.shape, confidence))
    if len(loc[0]) > 0:
        left = loc[1][0]
        top = loc[0][0]
        right = left + template.shape[1]
        bottom = top + template.shape[0]
        return Box(left, top, right, bottom)
    else:
        return None


def get_all_pos(image: str, grayscale: bool = False, confidence: float = 0.9) -> List[Box]:
    """
    Get a list of all positions where the given image appears in the current screen.

    Args:
        image (str): The path to the image file to search for.
        grayscale (bool, optional): Whether to use grayscale image matching. Defaults to False.
        confidence (float, optional): The minimum confidence level required to match the image. Defaults to 0.9.

    Returns:
        List[Box]: A list of Box objects representing the positions where the image was found.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(
        image, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= np.full(res.shape, confidence))
    boxes = []
    for pt in zip(*loc[::-1]):
        left = pt[0]
        top = pt[1]  # type: ignore
        right = left + template.shape[1]
        bottom = top + template.shape[0]
        boxes.append(Box(left, top, right, bottom))
    return boxes


def get_pos_on_region(image: str, region: Optional[Box] = None, grayscale: bool = False, confidence: float = 0.9) -> Optional[Box]:
    """
    Get the position of the given image on the screen within the specified region.

    Args:
        image (str): The path to the image file to search for.
        region (Box, optional): The region of the screen to search in. Defaults to None (the entire screen).
        grayscale (bool, optional): Whether to use grayscale image matching. Defaults to False.
        confidence (float, optional): The minimum confidence level required to match the image. Defaults to 0.9.

    Returns:
        Box: A Box object representing the position of the image, or None if the image was not found in the specified region.
    """
    _box = pyautogui.locateOnScreen(
        image, region=region, grayscale=grayscale, confidence=confidence)
    return _box


def locate_window(image: str, save_as: Optional[str] = None) -> Optional[Box]:
    """
    Attempt to locate the window containing the given image and return its position as a Box object.

    Args:
        image (str): The path to the image file to search for.
        save_as (str, optional): If provided, save a screenshot of the window as the specified filename. Defaults to None.

    Returns:
        Optional[Box]: If the window is found, return a Box object representing its position. Otherwise, return None.
    """
    header = get_pos(image)
    if header is None:
        return None
    try:
        footer = None
        for i in range(int((get_monitors()[0].height - header.top) / 100)):
            region = Box(header.left, header.top, header.width, (i + 1) * 100)
            footer = get_pos_on_region(_window_footer, region)
            if footer is not None:
                break
        if footer is None:
            region = Box(header.left, header.top, header.width,
                         get_monitors()[0].height - header.top)
            footer = get_pos_on_region(_window_footer, region)
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


def locate_all_windows(image: str, save_as: Optional[str] = None) -> Optional[List[Box]]:
    """
    Locate all windows that match the given image and return their positions as a list of Box objects.

    Args:
        image (str): The path to the image file to search for.
        save_as (str, optional): If provided, save screenshots of each window to files with this base filename.
                                 Defaults to None.

    Returns:
        Optional[List[Box]]: A list of Box objects representing the positions of each matched window, or None if an
                              error occurs.
    """
    windows: List[Box] = []
    try:
        for header in get_all_pos(image):
            footer: Optional[Box] = None
            for i in range(int(get_monitors()[0].height - header.top) // 100):
                region = Box(header.left, header.top,
                             header.width, (i + 1) * 100)
                footer = get_pos_on_region(_window_footer, region)
                if footer is not None:
                    break
            if footer is None:
                region = Box(header.left, header.top, header.width,
                             get_monitors()[0].height - header.top)
                footer = get_pos_on_region(_window_footer, region)
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
