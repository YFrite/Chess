from src.settings import BACKGROUND_COLOR, font_xizor
from src.state_machine import _State
import pygame as pg


class Menu(_State):
    def __init__(self):
        super().__init__()
        self.next = "GAME"
        self.timeout = 5
        self.alpha = 0
        self.alpha_speed = 2

    def update(self, keys, now):
        self.now = now
        self.alpha = min(self.alpha + self.alpha_speed, 255)

    def draw(self, surface, interpolate):
        surface.fill(BACKGROUND_COLOR)
        surface.blit(font_xizor.render("MENU", False, (0, 255, 0)), (0, 0))

    def get_event(self, event):
        self.done = event.type == pg.KEYDOWN
