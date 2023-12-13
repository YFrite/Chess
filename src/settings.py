import os.path

import pygame as pg

from src.files import resources_from_dir, load_yaml

pg.init()
SCREEN_SIZE: tuple[int, int] = (1200, 700)
BACKGROUND_COLOR = (255, 255, 255)
COLORS = load_yaml("data.yaml")

STATUSES = {0: 'White: Select a Piece to Move!', 1: 'White: Select a Destination!',
            2: 'Black: Select a Piece to Move!', 3: 'Black: Select a Destination!'}

SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
_screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)

TIME_PER_UPDATE = 16  # ms

CAPTURE = "AICar"

_SUB_DIRECTORIES = ["misc", "fonts", "figures"]
RESOURCES = resources_from_dir(_SUB_DIRECTORIES)
