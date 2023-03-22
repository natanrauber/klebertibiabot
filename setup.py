from pathlib import Path

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
from lib.utils.window_manager import activate_all_windows

SESSION_DIR: str = "C:/dev/kleber/images/session"
START_SCREENSHOT: str = SESSION_DIR + "/start.png"


def _status(on: bool) -> str:
    """
    Returns a string representation of a boolean value, indicating if a feature is enabled or not.

    Args:
        on (bool): A boolean value indicating if a feature is enabled.

    Returns:
        str: A string representation of the boolean value.
    """
    return "on" if on else "off"


def colorize(value: bool) -> str:
    """
    Returns a string representation of a color, based on a boolean value.

    Args:
        value (bool): A boolean value indicating if a color should be green or red.

    Returns:
        str: A string representation of a color.
    """
    return Colors.green if value else Colors.red


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
    activate_all_windows(Character.name())
    FolderManager.clear_folder(SESSION_DIR)

    Console.log(f"CHARACTER: {Character.name()}", color=Colors.yellow)

    Console.log(f"HEAL: {_status(HEAL)}", color=colorize(HEAL))
    if HEAL:
        Console.log(f"\thealth: {'yellow' if HEAL_ON_YELLOW else 'red'}",
                    color=Colors.yellow)
        Console.log(f"\tkey: {HEAL_KEY}", color=Colors.yellow)
        setupHeal()

    Console.log(f"ATTACK: {_status(ATTACK)}", color=colorize(ATTACK))
    if ATTACK:
        Console.log(f"\tkey: {ATTACK_KEY}", color=Colors.yellow)
        setupAttack()

    Console.log(f"LOOT: {_status(LOOT)}", color=colorize(LOOT))

    Console.log(f"DROP: {_status(DROP)}", color=colorize(DROP))
    if DROP:
        Console.log(f"\tthreads: {MAX_CLEANER_AMOUNT}", color=Colors.yellow)
        Console.log(f"\tcontainer: {DROP_CONTAINER}", color=Colors.yellow)
        setupDrop()

    Console.log(f"WALK: {_status(WALK)}", color=colorize(WALK))
    if WALK:
        Console.log(f"\thunt: {HUNT_NAME}", color=Colors.yellow)
        setupWalk()

    pyautogui.screenshot(START_SCREENSHOT)

    Status.pause()
    FolderManager.open_folder(SESSION_DIR)
