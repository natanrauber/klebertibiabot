import os
import glob


def clearFolder(folder):
    files = glob.glob(f'{folder}/*')
    for f in files:
        os.remove(f)
