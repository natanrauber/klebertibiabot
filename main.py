import ctypes
import sys

from lib.utils.gui_manager import GUIManager
from setup import setup

gui_manager: GUIManager


def is_admin() -> bool:
    """
    Determines if the current user has administrative privileges.

    Returns:
        bool: True if the user has administrative privileges, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    setup()
    gui_manager = GUIManager()
    gui_manager.start()
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
