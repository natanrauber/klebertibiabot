import time

from config import SCREEN_CENTER_X, SCREEN_CENTER_Y, SQM_SIZE
from lib.shared import setLoot
from lib.utils.keyboard import Key, Keyboard
from lib.utils.log import log
from lib.utils.mouse import Mouse


def loot():
    if Mouse.isLocked():
        time.sleep(0.1)
        return loot()
    log('looting...')
    Mouse.lock(True)
    _initPos = Mouse.getPos()
    Keyboard.hold(Key.alt)
    Mouse.clickLeft((SCREEN_CENTER_X+SQM_SIZE, SCREEN_CENTER_Y-SQM_SIZE))
    Mouse.clickLeft((SCREEN_CENTER_X, SCREEN_CENTER_Y-SQM_SIZE))
    Mouse.clickLeft((SCREEN_CENTER_X-SQM_SIZE, SCREEN_CENTER_Y-SQM_SIZE))
    Mouse.clickLeft((SCREEN_CENTER_X-SQM_SIZE, SCREEN_CENTER_Y))
    Mouse.clickLeft((SCREEN_CENTER_X-SQM_SIZE, SCREEN_CENTER_Y+SQM_SIZE))
    Mouse.clickLeft((SCREEN_CENTER_X, SCREEN_CENTER_Y+SQM_SIZE))
    Mouse.clickLeft((SCREEN_CENTER_X+SQM_SIZE, SCREEN_CENTER_Y+SQM_SIZE))
    Mouse.clickLeft((SCREEN_CENTER_X+SQM_SIZE, SCREEN_CENTER_Y))
    Mouse.clickLeft((SCREEN_CENTER_X, SCREEN_CENTER_Y))
    Keyboard.release(Key.alt)
    Mouse.setPos(_initPos)
    Mouse.lock(False)
    setLoot(False)
