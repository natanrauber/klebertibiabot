import time

from lib.config import Config
from lib.modules.attack import attack, hasTarget, isAttackEnabled, isAttacking
from lib.modules.heal import Healer
from lib.modules.loot import hasLoot, loot
from lib.modules.stats_worker import StatsWorker
from lib.modules.strike import Strike
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

    if Config.getHeal() is True and Healer.active() is False:
        healer = Healer()
        healer.daemon = True
        return healer.start()

    if Config.anyStat() is True and StatsWorker.active() is False:
        stats_worker = StatsWorker()
        stats_worker.daemon = True
        return stats_worker.start()

    # if DESTROY:
    #     if not destroying():
    #         destroyer = Destroyer()
    #         destroyer.daemon = True
    #         destroyer.start()

    # if Config.getDrop():
    #     for _ in range(MAX_CLEANER_AMOUNT - cleanerAmount()):
    #         cleaner = Cleaner()
    #         cleaner.daemon = True
    #         cleaner.start()

    if Config.getLoot() and hasLoot() and not isAttacking():
        return loot()

    if Config.getAttack() and isAttackEnabled() and hasTarget():
        if isAttacking():
            if Config.getStrike() and not Strike.onCooldown():
                return Strike.use()
        else:
            if not hasLoot():
                return attack()

    if Config.getWalk() and not walkOnCooldown():
        if Config.getAttack() and hasTarget():
            return
        if Config.getLoot() and hasLoot():
            return
        return walk()
