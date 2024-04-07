import os
import shutil
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
            print(f"{folder_path} does not exist or is not a directory")
            return

        for item in folder.glob('*'):
            if item.is_file():
                try:
                    item.unlink()
                except Exception as e:
                    print(f"Failed to remove {item}: {e}")
            if item.is_dir():
                try:
                    shutil.rmtree(str(item))
                except Exception as e:
                    print(f"Failed to remove {item}: {e}")

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

    @staticmethod
    def delete_file(file_path: str) -> None:
        """
        Delete all files in a folder.

        Args:
            folder_path (str): The path to the folder to be cleared.

        Returns:
            None

        Raises:
            ValueError: If the specified folder does not exist or is not a directory.
        """
        file = Path(file_path)
        if not file.is_file():
            print(f"{file_path} does not exist or is not a file")
            return

        if file.is_file():
            try:
                file.unlink()
            except Exception as e:
                print(f"Failed to remove {file}: {e}")
