from datetime import datetime


def dateTime() -> str:
    return str(datetime.now())[11:19]
