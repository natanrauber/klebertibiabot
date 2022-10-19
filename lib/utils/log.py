

from lib.utils.datetime import dateTime


class Colors:
    default = '\033[0m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'


def log(value, color=Colors.default):
    return print(f"[{dateTime()}] {color}{value}{Colors.default}")
