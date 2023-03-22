from datetime import datetime
from os import listdir
from os.path import isfile, join

from pyscreeze import Box

from lib.utils.mouse import Mouse

foodDir = 'C:/dev/kleber/images/food/'
foodList = [foodDir + f for f in listdir(foodDir) if isfile(join(foodDir, f))]

_lastEat = datetime.now()


def canEat() -> bool:
    return (datetime.now() - _lastEat).seconds > 30


def isFood(image) -> bool:
    return image in foodList


def eat(box: Box):
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.click_left((box.left-884, box.top+16))
    Mouse.set_pos(_initPos)
    Mouse.lock(False)
    global _lastEat
    _lastEat = datetime.now()
