import threading
import time

from lib.config import Config
from lib.modules.food import Food
from lib.modules.haste import Haste
from lib.modules.ring import Ring
from lib.modules.utura import Utura
from lib.utils.console import Console
from lib.utils.status import Status

_active = False


class StatsWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global _active
        _active = True
        Console.log("Stats worker started...")
        while not Status.is_paused() and Config.anyStat():
            if Config.getEat() and Food.status() is False:
                Food.use()
                Console.log("Eating food...")
            if Config.getRing() and Ring.status() is False:
                Ring.use()
                Console.log("Equipping ring...")
            if Config.getUtura() and Utura.status() is False:
                Utura.use()
                Console.log("Casting utura...")
            if Config.getHaste() and Haste.status() is False:
                Haste.use()
                Console.log("Casting haste...")
            time.sleep(0.1)
        _active = False
        Console.log("Stats worker stopped...")
        time.sleep(0.1)
        if Config.getRing() and Ring.status():
            Ring.use()
            time.sleep(0.1)

    @staticmethod
    def active():
        global _active
        return _active
