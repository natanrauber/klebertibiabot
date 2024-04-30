import ctypes
import sys

from lib.setup import setup
from lib.utils.folder_manager import FolderManager
from lib.utils.gui_manager import GUIManager

gui_manager: GUIManager


def is_admin() -> bool:
    """
    Determines if the current user has administrative privileges.

    Returns:
        bool: True if the user has administrative privileges, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if is_admin():
    FolderManager.delete_file("./dist/compiler.exe")
    setup()
    gui_manager = GUIManager()
    gui_manager.start()
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
