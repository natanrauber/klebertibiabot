import time

from lib.config import DESTROY, MAX_CLEANER_AMOUNT, Config
from lib.modules.attack import attack, hasTarget, isAttackEnabled, isAttacking
from lib.modules.clean import Cleaner, cleanerAmount
from lib.modules.destroy import Destroyer, destroying
from lib.modules.heal import Healer
from lib.modules.loot import hasLoot, loot
from lib.modules.walk import walk, walkOnCooldown
from lib.utils.status import Status
from lib.utils.window_manager import WindowManager


def executeAction() -> None:
    if not WindowManager.isActive("Tibia"):
        WindowManager.activate("Tibia -")
    if not Config.getOTServer() and not WindowManager.isActive("Projector"):
        WindowManager.activate("Projector")

    if Status.is_sleeping():
        time.sleep(1)
        return executeAction()

    if Config.getHeal() and not Healer.active():
        healer = Healer()
        healer.daemon = True
        return healer.start()

    if DESTROY:
        if not destroying():
            destroyer = Destroyer()
            destroyer.daemon = True
            return destroyer.start()

    if Config.getEat() or Config.getDrop():
        for _ in range(MAX_CLEANER_AMOUNT - cleanerAmount()):
            cleaner = Cleaner()
            cleaner.daemon = True
            cleaner.start()

    if Config.getLoot() and hasLoot() and not isAttacking():
        return loot()

    if Config.getAttack() and isAttackEnabled() and hasTarget():
        if not isAttacking() and not hasLoot():
            return attack()

    if Config.getWalk() and not walkOnCooldown():
        if Config.getAttack() and hasTarget():
            return
        if Config.getLoot() and hasLoot():
            return
        return walk()
