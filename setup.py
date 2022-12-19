import os
import pyautogui
from config import *
from lib.actions.attack.attack import setupAttack
from lib.actions.clean.clean import setupDrop
from lib.actions.heal.heal import setupHeal
from lib.actions.walk.walk import setupWalk
from lib.utils.clear_folder import clearFolder
from lib.utils.status import pause
from lib.utils.gui import activateAllWindows, openFolder
from lib.utils.log import *
from lib.utils.character import *


def _clear(): return os.system('cls')


def _status(on: bool):
    return 'on' if on else 'off'


def _getColor(value: bool):
    return Colors.green if value else Colors.red


def setup():
    _clear()
    getCharacterName()
    _clear()
    activateAllWindows()
    clearFolder('C:/dev/kleber/images/session')

    log(f'CHARACTER: {charName()}', color=Colors.yellow)

    log(f'HEAL: {_status(HEAL)}', color=_getColor(HEAL))
    if HEAL:
        log(f'\thealth: {"yellow" if HEAL_ON_YELLOW else "red"}',
            color=Colors.yellow)
        log(f'\tkey: {HEAL_KEY}', color=Colors.yellow)
        setupHeal()

    log(f'ATTACK: {_status(ATTACK)}', color=_getColor(ATTACK))
    if ATTACK:
        log(f'\tkey: {ATTACK_KEY}', color=Colors.yellow)
        setupAttack()

    log(f'LOOT: {_status(LOOT)}', color=_getColor(LOOT))

    log(f'DROP: {_status(DROP)}', color=_getColor(DROP))
    if DROP:
        log(f'\tthreads: {MAX_CLEANER_AMOUNT}', color=Colors.yellow)
        log(f'\tcontainer: {DROP_CONTAINER}', color=Colors.yellow)
        setupDrop()

    log(f'WALK: {_status(WALK)}', color=_getColor(WALK))
    if WALK:
        log(f'\thunt: {HUNT_NAME}', color=Colors.yellow)
        setupWalk()

    pyautogui.screenshot(f'{SESSION_DIR}/start.png')

    pause(True)
    openFolder(SESSION_DIR)
