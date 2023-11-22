from src.settings import BACKGROUND_COLOR, GFX, SCREEN_RECT, font_xizor
from src.state_machine import _State
import pygame as pg


class Splash(_State):
    def __init__(self):
        super().__init__()
        self.next = "MENU"
        self.timeout = 1
        self.alpha = 150
        self.alpha_speed = 0

        self.image = GFX["misc"]['splash'].copy().convert()
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=SCREEN_RECT.center)

    def update(self, keys, now):
        self.now = now
        self.alpha = min(self.alpha + self.alpha_speed, 255)
        if self.now - self.start_time > 1000.0 * self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        surface.fill(BACKGROUND_COLOR)
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        pass