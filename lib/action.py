from lib.config import *
from lib.modules.attack import attack, hasTarget, isAttackEnabled, isAttacking
from lib.modules.clean import Cleaner, cleanerAmount
from lib.modules.destroy import Destroyer, destroying
from lib.modules.heal import Healer, healing
from lib.modules.loot import hasLoot, loot
from lib.modules.walk import walk, walkOnCooldown
from lib.utils.status import *
from lib.utils.window_manager import WindowManager


def executeAction():
    if not WindowManager.isActive("Tibia"):
        WindowManager.activate("Tibia -")
    if getProjector() and not WindowManager.isActive("Projector"):
        WindowManager.activate("Projector")

    if Status.is_sleeping():
        time.sleep(1)
        return executeAction()

    if getHeal():
        if not healing():
            healer = Healer()
            healer.daemon = True
            return healer.start()

    if DESTROY:
        if not destroying():
            destroyer = Destroyer()
            destroyer.daemon = True
            return destroyer.start()

    if getEat() or getDrop():
        for i in range(MAX_CLEANER_AMOUNT - cleanerAmount()):
            cleaner = Cleaner()
            cleaner.daemon = True
            cleaner.start()

    if getLoot() and hasLoot() and not isAttacking():
        return loot()

    if getAttack() and isAttackEnabled() and hasTarget():
        if ATTACK_TIMEOUT == 0 and not isAttacking() and not hasLoot():
            return attack()

    if getWalk() and not walkOnCooldown():
        if getAttack() and hasTarget():
            return
        if getLoot() and hasLoot():
            return
        return walk()
