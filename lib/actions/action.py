from config import *
from lib.actions.attack.attack import attack, hasTarget, isAttacking
from lib.actions.attack_timeout import *
from lib.actions.clean.clean import Cleaner, cleanerAmount
from lib.actions.heal.heal import Healer, healing
from lib.actions.loot.loot import hasLoot, loot
from lib.actions.walk.walk import walk, walkOnCooldown
from lib.utils.status import *
from lib.utils.window_manager import WindowManager


def executeAction():
    WindowManager.check_active_windows()

    if HEAL:
        if not healing():
            healer = Healer()
            healer.daemon = True
            return healer.start()

    if DROP:
        for i in range(MAX_CLEANER_AMOUNT - cleanerAmount()):
            cleaner = Cleaner()
            cleaner.daemon = True
            cleaner.start()

    if LOOT and hasLoot() and not isAttacking():
        return loot()

    if ATTACK and isAttackEnabled() and hasTarget():
        if ATTACK_TIMEOUT == 0 and not isAttacking() and not hasLoot():
            return attack()

    if WALK and not walkOnCooldown() and not hasTarget() and not hasLoot():
        return walk()
