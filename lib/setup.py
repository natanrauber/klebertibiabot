import pyautogui

from lib.config import *
from lib.uid import uid
from lib.utils.console import Console
from lib.utils.folder_manager import FolderManager
from lib.utils.keyboard import Keyboard
from lib.utils.window_manager import WindowManager


def setup() -> None:
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    pyautogui.hotkey("winleft", "m")

    FolderManager.clear_folder(SESSION_DIR)
    FolderManager.open_folder(SESSION_DIR)
    WindowManager.activate("Tibia -")
    if not getOTServer():
        WindowManager.activate("Projector")
    WindowManager.activate("session")
    WindowManager.activate(uid)
