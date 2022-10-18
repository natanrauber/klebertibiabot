import os
from config import *
from lib.utils.datetime import dateTime
from lib.utils.status import pause
from lib.utils.window import activateAllWindows
from lib.utils.log import *
from lib.utils.character import *


def _clear(): return os.system('cls')


def _status(on: bool):
    return "on" if on else "off"


def _getColor(value: bool):
    return Colors.GREEN if value else Colors.RED


def setup():
    getCharacterName()
    activateAllWindows()
    _clear()

    log(f"CHARACTER: {charName()}", color=Colors.YELLOW)

    log(f"HEAL: {_status(HEAL)}", color=_getColor(HEAL))
    if HEAL:
        log(f'\thealth: {"yellow" if HEAL_ON_YELLOW else "red"}',
            color=_getColor(HEAL))
        log(f'\tkey: "{HEAL_KEY}"', color=_getColor(HEAL))

    log(f"ATTACK: {_status(ATTACK)}", color=_getColor(ATTACK))
    if ATTACK:
        log(f'\tkey: "{ATTACK_KEY}"', color=_getColor(ATTACK))

    log(f"LOOT: {_status(LOOT)}", color=_getColor(LOOT))

    log(f"DROP: {_status(DROP)}", color=_getColor(DROP))
    log(f"\tthreads: {MAX_CLEANER_AMOUNT}", color=_getColor(DROP))

    log(f"WALK: {_status(WALK)}", color=_getColor(WALK))

    pause(True)
