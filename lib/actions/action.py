from config import *
from lib.actions.attack.attack import attack, hasTarget, isAttacking
from lib.actions.attack_timeout import *
from lib.actions.clean.clean import Cleaner, cleanerAmount
from lib.actions.heal.heal import Healer, healing
from lib.actions.loot.loot import loot
from lib.actions.walk.walk import walk, walkOnCooldown
from lib.shared import hasLoot
from lib.utils.gui import checkActiveWindows


def executeAction():
    checkActiveWindows()

    _healing = healing()

    if HEAL:
        if not _healing:
            healer = Healer()
            healer.daemon = True
            return healer.start()

    if DROP:
        while cleanerAmount() < MAX_CLEANER_AMOUNT:
            cleaner = Cleaner()
            cleaner.daemon = True
            cleaner.start()

    _has_loot = hasLoot()
    _is_attacking = isAttacking()

    if LOOT:
        if _has_loot and not _is_attacking:
            return loot()

    _has_target = isAttackEnabled() and hasTarget()

    if ATTACK and isAttackEnabled():
        if _has_target:
            if ATTACK_TIMEOUT == 0:
                if not _is_attacking and not _has_loot:
                    return attack()

    if WALK:
        if not walkOnCooldown():
            if not _has_target and not _has_loot:
                return walk()
