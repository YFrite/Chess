import os.path

import pygame as pg

from src.files import resources_from_dir, load_yaml

pg.init()
SCREEN_SIZE: tuple[int, int] = (1200, 805)
BACKGROUND_COLOR = (255, 255, 255)
COLORS = load_yaml("data.yaml")

STATUSES = {0: "Ход белых: выберите фигуру!", 1: "Ход белых: выберите клетку!",
            2: "Ход черных: выберите фигуру!", 3: "Ход черных: выберите клетку!"}

_screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
SCREEN_RECT = _screen.get_rect()

TIME_PER_UPDATE = 16  # ms

CAPTURE = "Chess"

_SUB_DIRECTORIES = ["misc", "fonts", "figures"]
RESOURCES = resources_from_dir(_SUB_DIRECTORIES)
MUSIC = {"finish_him": pg.mixer.Sound(os.path.join("resources", "sounds", "finish_him.mp3")), }
