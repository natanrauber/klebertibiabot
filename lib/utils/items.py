from os.path import isfile, join
from os import listdir

foodDir = "C:/dev/kleber/images/food/"
foodList = [foodDir + f for f in listdir(foodDir) if isfile(join(foodDir, f))]
