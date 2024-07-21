import cv2
import win32api
import Windows
import bettercam
from time import sleep

sct = bettercam.create(output_color="BGR", output_idx=0)

index = 0

while True:
    if not Windows.isCapslock() or Windows.is_cursor_show():
        continue
    isKey = win32api.GetAsyncKeyState(0x01) < 0
    if isKey:
        img = sct.grab()
        if img is None:
            sleep(0.01)
            continue
        cv2.imwrite(f"dataset/{index}.png", img)
        print(f"dataset/{index}.png")
        index+=1
        sleep(0.1)
    else:
        sleep(0.01)