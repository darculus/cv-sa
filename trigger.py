from Windows import *
from Config import *
from HIDMouse import HIDMouse

def trigger(img, weapon, RButton_timer):
    (b, g, r) = img[Region.center_y, Region.center_x] 
    # print(r)
    if r >= 253:
        if weapon == 1 and RButton_timer >= 27:
                HIDMouse.Click(HIDMouse.Button.Right)
                RButton_timer = 0
        elif weapon == 4:
            HIDMouse.Up()
        else:
            HIDMouse.Click()