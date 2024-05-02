import subprocess

uid = "Kleber"

# overwrite uid.py
with open("./lib/uid.py", "w") as item:
    item.write(f"uid = '{uid}'")

# run
runCmd = "python ./main.py"
subprocess.run(["powershell", "-Command", runCmd])

# Write uid to a file
with open("./uid.txt", "w") as uid_file:
    uid_file.write(uid)
