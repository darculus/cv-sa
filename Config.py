import json, os, sys
from pathlib import Path
from TTS import TTS
from Windows import WIDTH, HEIGHT

tts = TTS()


class Resolution:
    w = WIDTH
    h = HEIGHT
    if w > 1280:
        w = 1280
    if h > 1024:
        h = 1024
    print(f"Resolution: {w}x{h}")


class Region:
    fov_w = 250
    fov_h = 250
    left, top = (Resolution.w - fov_w) // 2, (Resolution.h - fov_h) // 2
    right, bottom = left + fov_w, top + fov_h
    region = (left, top, right, bottom)
    center_x = fov_w // 2
    center_y = fov_h // 2


class GlobalConfig:
    tolerance = 20
    offsetY = 0.9


class Config:
    isTriggerL = True
    sensX = 0.65
    sensY = 0.4
    sensXflick = 0.1
    sensYflick = 0.05
    sensXalt = 0.04
    sensYalt = 0.02
    flickRangeX = 3
    flickRangeY = 5
