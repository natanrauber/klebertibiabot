
from lib.utils.colors import Colors
from lib.utils.console import Console
from lib.utils.keyboard import Key

SESSION_DIR = 'C:/dev/kleber/images/session'
TEMP_DIR = 'C:/dev/kleber/images/temp'


# ACTIONS --------------------------------------------------
HEAL = True
ATTACK = True
LOOT = True
DROP = True
WALK = True

# HEAL --------------------------------------------------
HEAL_KEY = Key.f9
HEAL_ON_YELLOW = True  # if False will heal on red


# ATTACK --------------------------------------------------
ATTACK_KEY = Key.space
ATTACK_TIMEOUT = 0  # 0 to disable


# LOOT --------------------------------------------------
SCREEN_CENTER_X = 530
SCREEN_CENTER_Y = 285
SQM_SIZE = 40


# DROP --------------------------------------------------
DROP_CONTAINER = 'shopping_bag'
MAX_CLEANER_AMOUNT = 3  # each cleaner runs in a CPU thread


# WALK --------------------------------------------------
HUNT_NAME = 'secret_spider_lair'
ROPE_KEY = Key.f5
STOP_ALL_ACTIONS_KEY = Key.pause


def _status(on: bool) -> str:
    """
    Returns a string representation of a boolean value, indicating if a feature is enabled or not.

    Args:
        on (bool): A boolean value indicating if a feature is enabled.

    Returns:
        str: A string representation of the boolean value.
    """
    return "on" if on else "off"


def _colorize(value: bool) -> str:
    """
    Returns a string representation of a color, based on a boolean value.

    Args:
        value (bool): A boolean value indicating if a color should be green or red.

    Returns:
        str: A string representation of a color.
    """
    return Colors.green if value else Colors.red


def printConfigs() -> None:
    Console.log(f"HEAL: {_status(HEAL)}", color=_colorize(HEAL))
    if HEAL:
        Console.log(f"\thealth: {'yellow' if HEAL_ON_YELLOW else 'red'}",
                    color=Colors.yellow)
        Console.log(f"\tkey: {HEAL_KEY}", color=Colors.yellow)

    Console.log(f"ATTACK: {_status(ATTACK)}", color=_colorize(ATTACK))
    if ATTACK:
        Console.log(f"\tkey: {ATTACK_KEY}", color=Colors.yellow)

    Console.log(f"LOOT: {_status(LOOT)}", color=_colorize(LOOT))

    Console.log(f"DROP: {_status(DROP)}", color=_colorize(DROP))
    if DROP:
        Console.log(f"\tthreads: {MAX_CLEANER_AMOUNT}", color=Colors.yellow)
        Console.log(f"\tcontainer: {DROP_CONTAINER}", color=Colors.yellow)

    Console.log(f"WALK: {_status(WALK)}", color=_colorize(WALK))
    if WALK:
        Console.log(f"\thunt: {HUNT_NAME}", color=Colors.yellow)
