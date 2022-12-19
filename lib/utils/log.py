

from lib.utils.datetime import dateTime


class Colors:
    default = '\033[0m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'


_last_msg = ''


def log(msg, color=Colors.default):
    global _last_msg
    if msg == _last_msg:
        return
    _last_msg = msg
    return print(f'[{dateTime()}] {color}{msg}{Colors.default}')
