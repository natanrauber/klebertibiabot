import os
from os import listdir
from typing import Optional

from genericpath import isfile


class Dir:
    CWD = os.getcwd().replace("\\", "/")
    BLACKLIST = f"{CWD}/images/blacklist"
    CONTAINERS = f"{CWD}/images/containers"
    DESTROY: str = f"{CWD}/images/destroy"
    FOOD = f"{CWD}/images/food"
    HEALTH = f"{CWD}/images/heal"
    INTERFACE = f"{CWD}/images/interface"
    SESSION = f"{CWD}/images/session"
    TEMP = f"{CWD}/images/temp"
    WAYPOINTS = f"{CWD}/images/waypoints"

    @staticmethod
    def getFiles(
        dir: str,
        fullPath: bool = True,
        rstrip: Optional[int] = None,
    ) -> list[str]:
        return [
            (f"{dir}/{f}" if fullPath else f)[:rstrip]
            for f in listdir(dir)
            if isfile(f"{dir}/{f}")
        ]

    @staticmethod
    def getFolders(
        dir: str,
        fullPath: bool = True,
    ) -> list[str]:
        return [
            (f"{dir}/{d}" if fullPath else d)
            for d in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, d))
        ]
