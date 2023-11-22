import os.path

import pygame as pg

from src.files import graphics_from_dir

pg.init()
SCREEN_SIZE: tuple[int, int] = (1200, 700)
BACKGROUND_COLOR = (255, 255, 255)
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
_screen = pg.display.set_mode(SCREEN_SIZE)

font_xizor = pg.font.Font(os.path.join("resources", "fonts", "Xizor.ttf"), 30)  # Temp

TIME_PER_UPDATE = 16  # ms

CAPTURE = "AICar"

_SUB_DIRECTORIES = ["misc"]
GFX = graphics_from_dir(_SUB_DIRECTORIES)
