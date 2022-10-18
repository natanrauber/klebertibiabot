from config import *
from lib.actions.attack.attack import attack, hasTarget, isAttacking
from lib.actions.attack_timeout import *
from lib.actions.clean import Cleaner, cleanerAmount
from lib.actions.heal import Healer, healing, isWounded
from lib.actions.loot import loot
from lib.actions.walk import walk
from lib.shared import hasLoot
from lib.utils.window import checkActiveWindows

def executeAction():
    checkActiveWindows()

    if HEAL:
        if not healing():
            healer = Healer()
            healer.daemon = True
            healer.start()

    if DROP:
        if cleanerAmount() < MAX_CLEANER_AMOUNT:
            cleaner = Cleaner()
            cleaner.daemon = True
            cleaner.start()

    if LOOT:
        if hasLoot() and not isAttacking():
            return loot()

    if ATTACK:
        if hasTarget():
            if ATTACK_TIMEOUT == 0:
                if not isAttacking() and not hasLoot():
                    return attack()
            else:
                if not checkingTimeout():
                    attackTimeoutChecker = AttackTimeoutChecker()
                    attackTimeoutChecker.daemon = True
                    attackTimeoutChecker.start()
                if not isAttacking() and not hasLoot():
                    return attack()
                if timeout() and not attackOnCooldown():
                    setTimeout(False)
                    setLoot(False)
                    if WALK:
                        return walk()
                    return attack()

    if WALK:
        if not isWounded() and not hasTarget() and not hasLoot():
            return walk()
