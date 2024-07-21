from ctypes import WinDLL
import ctypes
from time import sleep
import psutil
import win32gui
import win32process


# Define necessary structures and constants
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class CURSORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("flags", ctypes.c_uint),
        ("hCursor", ctypes.c_void_p),
        ("ptScreenPos", POINT),
    ]


user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

# Define GetCursorInfo function
GetCursorInfo = user32.GetCursorInfo
GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
GetCursorInfo.restype = ctypes.c_bool

# Constants
CURSOR_SHOWING = 0x00000001


def get_active_window():
    try:
        # Get the handle of the foreground window
        hwnd = win32gui.GetForegroundWindow()

        # Get the process ID of the foreground window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        # Ensure the pid is a positive integer
        if pid < 0:
            return None

        # Get the process name using psutil
        process_name = psutil.Process(pid).name()
        return process_name

    except Exception:
        return None


WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


def calculate_grab_zone(pixel_fov):
    ZONE = max(1, min(5, pixel_fov))
    return (
        int(WIDTH / 2 - ZONE),
        int(HEIGHT / 2 - ZONE),
        int(WIDTH / 2 + ZONE),
        int(HEIGHT / 2 + ZONE),
    )


def isCapslock():
    return ctypes.windll.user32.GetKeyState(0x14) != 0


def is_cursor_show():
    # Initialize CURSORINFO structure
    pci = CURSORINFO()
    pci.cbSize = ctypes.sizeof(CURSORINFO)

    # Call GetCursorInfo function
    if GetCursorInfo(ctypes.byref(pci)):
        return pci.flags == CURSOR_SHOWING
    else:
        return False


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
