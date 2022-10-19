import pyautogui


dir = "C:/dev/kleber/"

slot = (1753, 454, 32, 22)
sqm = (1296, 59, 49, 49)
other = (1741, 378, 176, 15)


name = input("name: ")
folder = input("folder: ")
im1 = pyautogui.screenshot(
    "{}{}/{}.png".format(dir, folder, name), region=slot)
