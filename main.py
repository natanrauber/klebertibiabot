import ctypes
import sys

from main_loop import loop_thread
from setup import setup
from window import callPauseButton, rootWindow


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    setup()
    callPauseButton()
    rootWindow.mainloop()
    callPauseButton()
    loop_thread.join()
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
