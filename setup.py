import pyautogui

from config import *
from lib.actions.attack.attack import setupAttack
from lib.actions.clean.clean import setupDrop
from lib.actions.heal.heal import setupHeal
from lib.actions.walk.walk import setupWalk
from lib.utils.character import Character
from lib.utils.colors import Colors
from lib.utils.console import Console
from lib.utils.folder_manager import FolderManager
from lib.utils.status import Status
from lib.utils.window_manager import WindowManager

SESSION_DIR: str = "C:/dev/kleber/images/session"
START_SCREENSHOT: str = SESSION_DIR + "/start.png"


def setup() -> None:
    """
    Configures the player's character behavior, based on global settings.
    Prints logs indicating the enabled features and their specific settings.

    Returns:
        None
    """
    Console.clear()
    Character.get_character_name()
    Console.clear()
    WindowManager.activate_all_windows(Character.name())
    FolderManager.clear_folder(SESSION_DIR)

    Console.log(f"CHARACTER: {Character.name()}", color=Colors.yellow)
    printConfigs()

    if HEAL:
        setupHeal()
    if ATTACK:
        setupAttack()
    if DROP:
        setupDrop()
    if WALK:
        setupWalk()

    pyautogui.screenshot(START_SCREENSHOT)

    Status.pause()
    FolderManager.open_folder(SESSION_DIR)
