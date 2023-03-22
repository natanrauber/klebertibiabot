import os
from pathlib import Path


class FolderManager:
    """
    A class that provides static methods for working with folders.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """

    @staticmethod
    def clear_folder(folder_path: str) -> None:
        """
        Delete all files in a folder.

        Args:
            folder_path (str): The path to the folder to be cleared.

        Returns:
            None

        Raises:
            ValueError: If the specified folder does not exist or is not a directory.
        """
        folder = Path(folder_path)
        if not folder.is_dir():
            raise ValueError(
                f"{folder_path} does not exist or is not a directory")

        for file in folder.glob('*'):
            if file.is_file():
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Failed to remove {file}: {e}")

    @staticmethod
    def open_folder(folder_path: str) -> None:
        """
        Open a folder in the default file explorer.

        Args:
            folder_path (str): The path to the folder to be opened.

        Returns:
            None
        """
        os.startfile(folder_path)
