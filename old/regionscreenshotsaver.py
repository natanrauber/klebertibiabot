#This script saves the image of the region 660,350,600,400 as savedimage.png in the path "C:\Users\Antec\Desktop\Tutorial\savedimage.png"

import pyautogui

im1 = pyautogui.screenshot(region=(1415,115,55,55))
im1.save(r"C:/dev/kleber/savedimage.png")
