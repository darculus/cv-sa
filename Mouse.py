import win32api
import win32con
from time import sleep
from threading import Thread

class Button:
    Left = 0
    Right = 1

    LeftDown = win32con.MOUSEEVENTF_LEFTDOWN
    RightDown = win32con.MOUSEEVENTF_RIGHTDOWN
    LeftUp = win32con.MOUSEEVENTF_LEFTUP
    RightUp = win32con.MOUSEEVENTF_RIGHTUP

def Move(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)

def Click(button:Button=Button.Left):
    Thread(target=Click_sync, args=(button,)).start()

def Click_sync(button:Button=Button.Left, delay=0.025):
    Down(button)
    sleep(delay)
    Up(button)
    sleep(0.01)

def Down(button:Button=Button.Left):
    if button == Button.Left:
        button = Button.LeftDown
    else:
        button = Button.RightDown
    win32api.mouse_event(button, 0,0, 0, 0)


def Up(button:Button=Button.Left):    
    if button == Button.Left:
        button = Button.LeftUp
    else:
        button = Button.RightUp
    win32api.mouse_event(button, 0,0, 0, 0)
    