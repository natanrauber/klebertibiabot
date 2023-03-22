from win32gui import GetForegroundWindow, GetWindowText

from lib.utils.wsh import wsh


class WindowManager:
    """
    A class that provides methods for managing windows.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    @staticmethod
    def check_active_windows(charName: str = '') -> None:
        """
        Checks if the Tibia window is currently active. If not, activates all Tibia windows with the given character name.

        Args:
            charName (str, optional): The character name used to filter the Tibia windows to be activated. Defaults to ''.
        """
        if WindowManager.is_tibia_active():
            return
        WindowManager.activate_all_windows(charName=charName)

    @staticmethod
    def get_window_name() -> str:
        """
        Returns the title of the active window.

        Returns:
            str: The title of the active window.
        """
        return GetWindowText(GetForegroundWindow())

    @staticmethod
    def is_tibia_active() -> bool:
        """
        Checks if the Tibia window is currently active.

        Returns:
            bool: True if the Tibia window is active, False otherwise.
        """
        if 'Tibia' in WindowManager.get_window_name():
            return True
        return False

    @staticmethod
    def activate_all_windows(charName: str = '') -> None:
        """
        Activates all Tibia windows with the given character name.

        Args:
            charName (str, optional): The character name used to filter the Tibia windows to be activated. Defaults to ''.
        """
        wsh.AppActivate('session')
        wsh.AppActivate('Projetor em janela (prévia)')
        wsh.AppActivate('Kleber')
        wsh.AppActivate(f'Tibia - {charName}')
