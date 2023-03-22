from typing import List, Optional

import cv2
import numpy as np
import pyautogui
from pyscreeze import Box
from screeninfo import get_monitors

from config import SESSION_DIR

_interface_dir: str = 'C:/dev/kleber/images/interface'
_window_footer: str = f'{_interface_dir}/window_footer.png'


class ImageLocator:
    """
    A class that provides various methods for locating images on the screen using OpenCV and PyAutoGUI libraries.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def locate_window(image: str, save_as: Optional[str] = None) -> Optional[Box]:
        """
        Attempt to locate the window containing the given image and return its position as a Box object.

        Args:
            image (str): The path to the image file to search for.
            save_as (str, optional): If provided, save a screenshot of the window as the specified filename. Defaults to None.

        Returns:
            Optional[Box]: If the window is found, return a Box object representing its position. Otherwise, return None.
        """
        header = ImageLocator.get_pos(image)
        if header is None:
            return None
        try:
            footer = None
            for i in range(int((get_monitors()[0].height - header.top) / 100)):
                region = Box(header.left, header.top,
                             header.width, (i + 1) * 100)
                footer = ImageLocator.get_pos_on_region(_window_footer, region)
                if footer is not None:
                    break
            if footer is None:
                region = Box(header.left, header.top, header.width,
                             get_monitors()[0].height - header.top)
                footer = ImageLocator.get_pos_on_region(_window_footer, region)
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

    @staticmethod
    def locate_all_windows(image: str, save_as: Optional[str] = None) -> Optional[List[Box]]:
        """
        Locate all windows that match the given image and return their positions as a list of Box objects.

        Args:
            image (str): The path to the image file to search for.
            save_as (str, optional): If provided, save screenshots of each window to files with this base filename.Defaults to None.

        Returns:
            Optional[List[Box]]: A list of Box objects representing the positions of each matched window, or None if an error occurs.
        """
        windows: List[Box] = []
        try:
            for header in ImageLocator.get_all_pos(image):
                footer: Optional[Box] = None
                for i in range(int(get_monitors()[0].height - header.top) // 100):
                    region = Box(header.left, header.top,
                                 header.width, (i + 1) * 100)
                    footer = ImageLocator.get_pos_on_region(
                        _window_footer, region)
                    if footer is not None:
                        break
                if footer is None:
                    region = Box(header.left, header.top, header.width,
                                 get_monitors()[0].height - header.top)
                    footer = ImageLocator.get_pos_on_region(
                        _window_footer, region)
                if isinstance(footer, Box):
                    window = Box(header.left, header.top, footer.left + footer.width -
                                 header.left, footer.top + footer.height - header.top)
                    if isinstance(window, Box):
                        if save_as is not None:
                            screenshot_path = f"{SESSION_DIR}/{save_as}{len(windows)}.png"
                            pyautogui.screenshot(
                                screenshot_path, region=window)
                        windows.append(window)
            return windows
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
