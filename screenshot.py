import pyautogui


dir = "C:/dev/kleber/images/"

slot = (1753, 454, 32, 22)
sqm = (1296, 59, 49, 49)
other = (1765, 406, 136, 9)


name = input("name: ")
folder = input("folder: ")
im1 = pyautogui.screenshot(
    "{}{}/{}.png".format(dir, folder, name), region=slot)
