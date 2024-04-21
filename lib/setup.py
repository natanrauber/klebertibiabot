import pyautogui

from lib.actions.attack.attack import setupAttack
from lib.actions.clean.clean import setupDrop
from lib.actions.destroy.destroy import setup_destroy
from lib.actions.heal.heal import setupHeal
from lib.actions.walk.walk import setupWalk
from lib.config import *
from lib.utils.console import Console
from lib.utils.folder_manager import FolderManager
from lib.utils.window_manager import WindowManager


def setup() -> None:
    """
    Configures the player's character behavior, based on global settings.
    Prints logs indicating the enabled features and their specific settings.

    Returns:
        None
    """
    Console.clear()
    WindowManager.activate_projector_window()

    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    FolderManager.clear_folder(SESSION_DIR)

    if HEAL:
        setupHeal()
    if DESTROY:
        setup_destroy()
    if ATTACK:
        setupAttack()
    if DROP:
        setupDrop()
    if WALK:
        setupWalk()

    WindowManager.activate_all_windows()
    FolderManager.open_folder(SESSION_DIR)
