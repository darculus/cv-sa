import cv2
import bettercam
import numpy as np
import win32api
import ctypes
import os
from pynput import keyboard
from threading import Thread
from TTS import TTS
from Windows import *
from Config import *
import time
from HIDMouse import HIDMouse
from trigger import trigger

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, ' '.join(sys.argv), None, 1
    )
    os._exit(0)

tts = TTS()

weapon = 3

def quit():
    tts.Speak_sync("종료")
    os._exit(0)

def on_press_threaded(key):
    global weapon
    try:
        if key == keyboard.Key.f12:
            quit()
        if not isCapslock() or is_cursor_show():
            return
        elif isinstance(key, keyboard.KeyCode) and key.vk >= 0x31 and key.vk <= 0x34:
            if weapon == key.vk - 0x30:
                return
            weapon = key.vk - 0x30
    except Exception as e:
        print(f"Error: {e}")
def on_press(key):
    Thread(target=on_press_threaded, args=(key,)).start()

def key_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

keyboard_listner_thread = Thread(target=key_listener)
keyboard_listner_thread.daemon = True
keyboard_listner_thread.start()


sct = bettercam.create(output_color="BGR", output_idx=0)


outline_range = (0, 0, 150)

kernel = np.ones((2, 2), np.uint8)
RButton_timer = 0
HIDMouse.Init()

while True:
    if not isCapslock() or is_cursor_show():
        time.sleep(0.01)
        continue
    elif weapon == 3 or weapon >= 5:
        continue

    img = sct.grab(Region.region)
    if img is None:
        time.sleep(0.01)
        continue
    
    LButton = win32api.GetAsyncKeyState(0x01) < 0
    RButton = win32api.GetAsyncKeyState(0x02) < 0
    if RButton:
        RButton_timer += 1
    else:
        RButton_timer = 0
    
    if not LButton or weapon == 4:
        Thread(target=trigger, args=(img, weapon, RButton_timer)).start()
    
    mask = cv2.inRange(img, outline_range, outline_range)

    # 컨투어 검출
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    closest_contour = None
    closest_distance = float("inf")

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cX = x + w // 2
        cY = y + h // 2
        distance = ((cX - Region.center_x) ** 2 + (cY - Region.center_y) ** 2) ** 0.5
        if distance < closest_distance:
            closest_distance = distance
            closest_contour = contour

    if closest_contour is None:
        time.sleep(0.01)
        continue
    x, y, w, h = cv2.boundingRect(closest_contour)

    cX = x + w // 2
    cY = y + h // 2
    cY = cY * GlobalConfig.offsetY
    cX = cX - Region.center_x
    cY = cY - Region.center_y

    
    
    isFlickKey = win32api.GetAsyncKeyState(0x05) < 0

    sensX = Config.sensX
    sensY = Config.sensY
    if isFlickKey and (not Config.flickOnlyZoom or (Config.flickOnlyZoom and RButton)):
        sensX = Config.sensXflick
        sensY = Config.sensYflick
    elif LButton:
        sensX = Config.sensX
        sensY = Config.sensY
    elif RButton:
        sensX = Config.sensXalt
        sensY = Config.sensYalt

    dX = int(cX * sensX)
    dY = int(cY * sensY)

    if dY > -10:
        # if LButton or RButton or isFlickKey:
        HIDMouse.Move(dX, dY)
    # if isFlickKey:
    #     if abs(cX) <= Config.flickRangeX and cY <= Config.flickRangeY and cY >= -5:            
    #         button = Mouse.Button.Left if Config.isTriggerL else Mouse.Button.Right        
    #         Mouse.Click(button)
    #         isX1Pressed = False
    #         time.sleep(0.01)
    time.sleep(0.001)
