from win32gui import GetForegroundWindow, GetWindowText

from lib.utils.wsh import wsh


class WindowManager:
    """
    A class that provides methods for managing windows.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    @staticmethod
    def check_active_windows() -> None:
        """
        Checks if the Tibia window is currently active. If not, activates all Tibia windows with the given character name.
        """
        if WindowManager.is_tibia_active():
            return
        WindowManager.activate_all_windows()

    @staticmethod
    def is_tibia_active() -> bool:
        """
        Checks if the Tibia window is currently active.

        Returns:
            bool: True if the Tibia window is active, False otherwise.
        """
        if 'Tibia' in GetWindowText(GetForegroundWindow()):
            return True
        return False

    @staticmethod
    def activate_all_windows() -> None:
        """
        Activates all Tibia windows with the given character name.
        """
        wsh.AppActivate('session')
        wsh.AppActivate('Kleber')
        wsh.AppActivate('Windowed Projector')
        wsh.AppActivate('Tibia -')
        
    @staticmethod
    def activate_projector_window() -> None:
        wsh.AppActivate('Windowed Projector')

