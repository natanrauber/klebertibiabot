from os.path import isfile, join
from os import listdir

foodDir = "C:/dev/kleber/images/food/"
blacklistDir = "C:/dev/kleber/images/blacklist/"

foodList = [foodDir + f for f in listdir(foodDir) if isfile(join(foodDir, f))]
blackList = foodList + [blacklistDir +
                        f for f in listdir(blacklistDir) if isfile(join(blacklistDir, f))]
