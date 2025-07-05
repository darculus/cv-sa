import hid, random
from time import sleep
from threading import Thread

class Button:
    Left = 1
    Right = 2
    Middle = 4
    Button4 = 8
    Button5 = 16

class HIDMouse:
    _buttons_mask = 0
    _dev = None

    @classmethod
    def _init(cls, dev):
        cls._dev = dev
        cls._buttons_mask = 0
        cls.Move(5, 5)

    @classmethod
    def Init(cls, vid=0x046D, pid=0xC547, ping_code=0x7C):
        dev = find_mouse_device(vid, pid, ping_code)
        if not dev:
            vid_str = hex(vid) if vid else "Unspecified"
            pid_str = hex(pid) if pid else "Unspecified"
            ping_code_str = hex(ping_code) if pid else "Unspecified"
            error_msg = ("[-] Device "
                         f"Vendor ID: {vid_str}, Product ID: {pid_str} "
                         f"Pingcode: {ping_code_str} not found!")
            raise DeviceNotFoundError(error_msg)
        cls._init(dev)

    @classmethod
    def _buttons(cls, buttons):
        if buttons != cls._buttons_mask:
            cls._buttons_mask = buttons
            cls.Move(0, 0)

    @classmethod
    def Click_async(cls, button=Button.Left, delay=0.25):
        # cls._buttons_mask = button
        # cls.Move(0, 0)
        cls.Down(button)
        if delay >= 0.05:
            delay = random.uniform(delay - 0.05, delay + 0.05)
        sleep(delay)
        cls.Up(button)
        # cls._buttons_mask = 0
        # cls.Move(0, 0)
    @staticmethod
    def Click(button=Button.Left, delay=0.25):
        Thread(target=HIDMouse.Click_async, args=(button, delay)).start()

    @classmethod
    def Down(cls, button=Button.Left):
        cls._buttons(cls._buttons_mask | button)
        cls.Move(0, 0)

    @classmethod
    def Up(cls, button=Button.Left):
        cls._buttons(cls._buttons_mask & ~button)
        cls.Move(0, 0)

    @classmethod
    def is_pressed(cls, button=Button.Left):
        return bool(button & cls._buttons_mask)

    @classmethod
    def Move(cls, x, y, z=0):
        limited_x = limit_xy(x)
        limited_y = limit_xy(y)
        cls._sendRawReport(cls._makeReport(limited_x, limited_y, z))

    @classmethod
    def _makeReport(cls, x, y, z):
        report_data = [
            0x01,   # Report ID: 0
            cls._buttons_mask,
            low_byte(x), high_byte(x),
            low_byte(y), high_byte(y),
            z
        ]
        return report_data

    @classmethod
    def _sendRawReport(cls, report_data):
        cls._dev.write(report_data)


class DeviceNotFoundError(Exception):
    pass


def check_ping(dev, ping_code):
    dev.write([0, ping_code])
    try:
        resp = dev.read(max_length=1, timeout_ms=10)
    except OSError as e:
        return False
    else:
        return resp and resp[0] == ping_code


def find_mouse_device(vid, pid, ping_code):
    dev = hid.device()
    for dev_info in hid.enumerate(vid, pid):
        dev.open_path(dev_info['path'])
        found = check_ping(dev, ping_code)
        if found:
            return dev
        else:
            dev.close()
    return None


def limit_xy(xy):
    if xy < -32767:
        return -32767
    elif xy > 32767:
        return 32767
    else:
        return int(xy)


def low_byte(x):
    return x & 0xFF


def high_byte(x):
    return (x >> 8) & 0xFF


if __name__ == "__main__":
    HIDMouse.Init()
    HIDMouse.Move(100, 100)