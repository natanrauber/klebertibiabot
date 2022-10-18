

from lib.utils.datetime import dateTime


class Colors:
    DEFAULT = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


def log(value, color=Colors.DEFAULT):
    return print(f"[{dateTime()}] {color}{value}{Colors.DEFAULT}")
