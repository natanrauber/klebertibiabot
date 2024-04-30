import os

import pyautogui

import lib.config as cfg
from lib.uid import uid
from lib.utils.folder_manager import FolderManager
from lib.utils.window_manager import WindowManager


def setup() -> None:
    if not os.path.exists(cfg.SESSION_DIR):
        os.makedirs(cfg.SESSION_DIR)

    if not os.path.exists(cfg.TEMP_DIR):
        os.makedirs(cfg.TEMP_DIR)

    pyautogui.hotkey("winleft", "m")

    FolderManager.clear_folder(cfg.SESSION_DIR)
    FolderManager.open_folder(cfg.SESSION_DIR)
    WindowManager.activate("Tibia -")
    if not cfg.getOTServer():
        WindowManager.activate("Projector")
    WindowManager.activate("session")
    WindowManager.activate(uid)
