import os
from config import *
from lib.actions.attack.attack import setupAttack
from lib.actions.clean.clean import setupDrop
from lib.actions.heal.heal import setupHeal
from lib.utils.status import pause
from lib.utils.gui import activateAllWindows
from lib.utils.log import *
from lib.utils.character import *


def _clear(): return os.system('cls')


def _status(on: bool):
    return "on" if on else "off"


def _getColor(value: bool):
    return Colors.green if value else Colors.red


def setup():
    getCharacterName()
    activateAllWindows()
    _clear()

    log(f"CHARACTER: {charName()}", color=Colors.yellow)

    log(f"HEAL: {_status(HEAL)}", color=_getColor(HEAL))
    if HEAL:
        log(f'\thealth: {"yellow" if HEAL_ON_YELLOW else "red"}',
            color=_getColor(HEAL))
        log(f'\tkey: "{HEAL_KEY}"', color=_getColor(HEAL))
        setupHeal()

    log(f"ATTACK: {_status(ATTACK)}", color=_getColor(ATTACK))
    if ATTACK:
        log(f'\tkey: "{ATTACK_KEY}"', color=_getColor(ATTACK))
        setupAttack()

    log(f"LOOT: {_status(LOOT)}", color=_getColor(LOOT))

    log(f"DROP: {_status(DROP)}", color=_getColor(DROP))
    if DROP:
        log(f"\tthreads: {MAX_CLEANER_AMOUNT}", color=_getColor(DROP))
        setupDrop()

    log(f"WALK: {_status(WALK)}", color=_getColor(WALK))

    pause(True)
