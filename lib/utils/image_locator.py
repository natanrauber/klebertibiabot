from typing import List, Optional

import cv2
import numpy as np
import pyautogui
from pyscreeze import Box
from screeninfo import get_monitors

from lib.utils.dir import Dir


class ImageLocator:

    @staticmethod
    def get_pos(
        image: str, grayscale: bool = False, confidence: float = 0.9
    ) -> Optional[Box]:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(
            image, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
        )
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
    def get_all_pos(
        image: str, grayscale: bool = False, confidence: float = 0.9
    ) -> List[Box]:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(
            image, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
        )
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
    def get_pos_on_region(
        image: str,
        region: Optional[Box] = None,
        grayscale: bool = False,
        confidence: float = 0.9,
    ) -> Optional[Box]:
        _box = pyautogui.locateOnScreen(
            image, region=region, grayscale=grayscale, confidence=confidence
        )
        return _box

    @staticmethod
    def locate_window(
        header_image: str, footer_image: str, save_as: Optional[str] = None
    ) -> Optional[Box]:
        header = ImageLocator.get_pos(header_image)
        if header is None:
            return None
        try:
            footer = None
            for i in range(int((get_monitors()[0].height - header.top) // 100)):
                region = Box(header.left, header.top, header.width, (i + 1) * 100)
                footer = ImageLocator.get_pos_on_region(footer_image, region)
                if footer is not None:
                    break
            if footer is None:
                region = Box(
                    header.left,
                    header.top,
                    header.width,
                    get_monitors()[0].height - header.top,
                )
                footer = ImageLocator.get_pos_on_region(footer_image, region)
            if footer is None:
                return None
            window = Box(
                header.left,
                header.top,
                footer.left + footer.width - header.left,
                footer.top + footer.height - header.top,
            )
            if save_as is not None and isinstance(window, Box):
                screenshot_path = f"{Dir.SESSION}/{save_as}.png"
                pyautogui.screenshot(screenshot_path, region=window)
            return window
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def locate_all_windows(
        header_image: str, footer_image: str, save_as: Optional[str] = None
    ) -> Optional[List[Box]]:
        windows: List[Box] = []
        try:
            for header in ImageLocator.get_all_pos(header_image):
                footer: Optional[Box] = None
                for i in range(int(get_monitors()[0].height - header.top) // 100):
                    region = Box(header.left, header.top, header.width, (i + 1) * 100)
                    footer = ImageLocator.get_pos_on_region(footer_image, region)
                    if footer is not None:
                        break
                if footer is None:
                    region = Box(
                        header.left,
                        header.top,
                        header.width,
                        get_monitors()[0].height - header.top,
                    )
                    footer = ImageLocator.get_pos_on_region(footer_image, region)
                if isinstance(footer, Box):
                    window = Box(
                        header.left,
                        header.top,
                        footer.left + footer.width - header.left,
                        footer.top + footer.height - header.top,
                    )
                    if isinstance(window, Box):
                        if save_as is not None:
                            screenshot_path = (
                                f"{Dir.SESSION}/{save_as}{len(windows)}.png"
                            )
                            pyautogui.screenshot(screenshot_path, region=window)
                        windows.append(window)
            return windows
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
