from Windows import *
from Config import *
import Mouse, win32api

def trigger(img, weapon, RButton_timer):
    (b, g, r) = img[Region.center_y, Region.center_x] 
    # print(r)
    if r >= 253 and r <= 255:
        if weapon == 1 and RButton_timer >= 27:
                Mouse.Click(Mouse.Button.Right)
                RButton_timer = 0
        elif weapon == 4:
            Mouse.Up()
        else:
            Mouse.Click()