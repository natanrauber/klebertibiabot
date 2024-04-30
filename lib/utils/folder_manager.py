import os
import shutil
from pathlib import Path


class FolderManager:

    @staticmethod
    def clear_folder(folder_path: str) -> None:
        folder = Path(folder_path)
        if not folder.is_dir():
            print(f"{folder_path} does not exist or is not a directory")
            return

        for item in folder.glob("*"):
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
        os.startfile(folder_path)

    @staticmethod
    def delete_file(file_path: str) -> None:
        file = Path(file_path)
        if not file.is_file():
            print(f"{file_path} does not exist or is not a file")
            return

        if file.is_file():
            try:
                file.unlink()
            except Exception as e:
                print(f"Failed to remove {file}: {e}")
