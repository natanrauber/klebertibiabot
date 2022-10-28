from datetime import datetime
from lib.utils.mouse import Mouse
from pyscreeze import Box

from os.path import isfile, join
from os import listdir

foodDir = 'C:/dev/kleber/images/food/'
foodList = [foodDir + f for f in listdir(foodDir) if isfile(join(foodDir, f))]

_lastEat = datetime.now()


def canEat() -> bool:
    return (datetime.now() - _lastEat).seconds > 30


def isFood(image) -> bool:
    return image in foodList


def eat(box: Box):
    Mouse.lock(True)
    _initPos = Mouse.getPos()
    Mouse.clickLeft((box.left-944, box.top+16))
    Mouse.setPos(_initPos)
    Mouse.lock(False)
    global _lastEat
    _lastEat = datetime.now()
