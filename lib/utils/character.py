from lib.utils.console import Console
from lib.utils.window_manager import check_active_windows, is_tibia_active


class Character:
    """
    A class representing a Tibia character.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    _name: str = ''

    @staticmethod
    def name() -> str:
        """
        Returns the name of the character as a string.

        Returns:
            str: The name of the character.
        """
        return Character._name

    @staticmethod
    def prompt_for_name() -> None:
        """
        Prompts the user to enter a character name and stores it in a static variable.
        """
        Character._name = input('Enter character name: ')

    @staticmethod
    def get_character_name() -> str:
        """
        Prompts the user to enter a character name and keeps prompting until the Tibia window is found for the given character name.
        Returns the character name as a string.

        Returns:
            str: The character name.
        """
        Character.prompt_for_name()
        check_active_windows()
        while not is_tibia_active():
            Console.log(
                'Cannot find Tibia window with the given character name.')
            Character.prompt_for_name()
            check_active_windows()
        return Character.name()
