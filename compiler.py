import random
import string
import subprocess

from lib.utils.folder_manager import FolderManager

# generate random uid
uid = "".join(random.choice(string.ascii_letters + string.digits) for i in range(10))

# overwrite uid.py
with open("./lib/uid.py", "w") as item:
    item.write(f"uid = '{uid}'")

# clear old build output
FolderManager.clear_folder("./dist")

# build .exe
buildCmd = f"pyinstaller ./main.py --name {uid} --onefile --noconsole"
subprocess.run(["powershell", "-Command", buildCmd])

# clear build files
FolderManager.clear_folder("./build")
FolderManager.delete_file(f"./{uid}.spec")

# run new .exe
runCmd = f"./dist/{uid}.exe"
subprocess.run(["powershell", "-Command", runCmd])
