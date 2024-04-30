import os

import pyautogui

from lib.config import Config
from lib.uid import uid
from lib.utils.dir import Dir
from lib.utils.folder_manager import FolderManager
from lib.utils.window_manager import WindowManager


def setup() -> None:
    if not os.path.exists(Dir.SESSION):
        os.makedirs(Dir.SESSION)

    if not os.path.exists(Dir.TEMP):
        os.makedirs(Dir.TEMP)

    pyautogui.hotkey("winleft", "m")

    FolderManager.clear_folder(Dir.SESSION)
    FolderManager.open_folder(Dir.SESSION)
    WindowManager.activate("Tibia -")
    if not Config.getOTServer():
        WindowManager.activate("Projector")
    WindowManager.activate("session")
    WindowManager.activate(uid)
