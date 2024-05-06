import subprocess

from lib.uid import uid
from lib.utils.folder_manager import FolderManager

# clear old build output
FolderManager.clear_folder("./dist")

# build .exe
buildCmd = f"pyinstaller ./main.py --name {uid} --onefile --noconsole"
subprocess.run(["powershell", "-Command", buildCmd])

# clear build files
FolderManager.clear_folder("./build")
FolderManager.delete_file(f"./{uid}.spec")
