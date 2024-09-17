from functools import partial
from typing import List, Optional

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from pyscreeze import Box

from lib.config import Config
from lib.utils.dir import Dir

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


class ImageLocator:

    @staticmethod
    def screenshot(
        imageFilename: str | None = None,
        region: Optional[Box] = None,
    ):
        if region is None:
            region = Box(
                0,
                0,
                Config.getMonitorWidth(),
                Config.getMonitorHeight(),
            )
        return pyautogui.screenshot(
            imageFilename,
            region=(
                int(region.left),
                int(region.top),
                int(region.width),
                int(region.height),
            ),
        )

    @staticmethod
    def get_pos(
        image: str, grayscale: bool = False, confidence: float = 0.9
    ) -> Optional[Box]:
        screenshot = ImageLocator.screenshot()
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
        screenshot = ImageLocator.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(
            image, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
        )
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= np.full(res.shape, confidence))
        boxes: list[Box] = []
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
        region: Box,
        grayscale: bool = False,
        confidence: float = 0.9,
    ) -> Optional[Box]:
        try:
            _box = pyautogui.locateOnScreen(
                image,
                region=(
                    int(region.left),
                    int(region.top),
                    int(region.width),
                    int(region.height),
                ),
                grayscale=grayscale,
                confidence=confidence,
            )
            return _box
        except Exception:
            return None

    @staticmethod
    def locate_window(
        header_image: str, footer_image: str, save_as: Optional[str] = None
    ) -> Optional[Box]:
        header = ImageLocator.get_pos(header_image)
        if header is None:
            return None
        try:
            footer = None
            for i in range(int(Config.getMonitorHeight() - header.top) // 100):
                region = Box(
                    header.left,
                    header.top,
                    header.width,
                    (i + 1) * 100,
                )
                footer = ImageLocator.get_pos_on_region(footer_image, region)
                if footer is not None:
                    break
            if footer is None:
                region = Box(
                    header.left,
                    header.top,
                    header.width,
                    Config.getMonitorHeight() - header.top,
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
            if save_as is not None:
                screenshot_path = f"{Dir.SESSION}/{save_as}.png"
                ImageLocator.screenshot(screenshot_path, region=window)
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
                for i in range(
                    int(Config.getMonitorHeight() - header.top) // 100,
                ):
                    region = Box(
                        header.left,
                        header.top,
                        header.width,
                        (i + 1) * 100,
                    )
                    footer = ImageLocator.get_pos_on_region(
                        footer_image,
                        region,
                    )
                    if footer is not None:
                        break
                if footer is None:
                    region = Box(
                        header.left,
                        header.top,
                        header.width,
                        Config.getMonitorHeight() - header.top,
                    )
                    footer = ImageLocator.get_pos_on_region(
                        footer_image,
                        region,
                    )
                if isinstance(footer, Box):
                    window = Box(
                        header.left,
                        header.top,
                        footer.left + footer.width - header.left,
                        footer.top + footer.height - header.top,
                    )
                    if save_as is not None:
                        screenshot_path = f"{Dir.SESSION}/{save_as}{len(windows)}.png"
                        ImageLocator.screenshot(screenshot_path, region=window)
                    windows.append(window)
            return windows
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
