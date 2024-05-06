import random
import string

# generate random uid
uid: str = "".join(
    random.choice(string.ascii_letters + string.digits) for _ in range(10)
)

# Write uid to a file
with open("./uid.txt", "w") as uid_file:
    uid_file.write(uid)
