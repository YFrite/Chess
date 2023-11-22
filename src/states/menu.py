import sys

import pygame as pg
from pygame import Surface
from pygame.event import Event

from src.settings import SCREEN_SIZE, BACKGROUND_COLOR, GFX
from src.state_machine import _State

from src.views.button import Button


class Menu(_State):
    def __init__(self):
        super().__init__()
        self.next = "GAME"
        self.timeout = 5
        self.alpha = 0
        self.alpha_speed = 2
        self.mouse_position = pg.mouse.get_pos()

        self.buttons = [Button(position=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 100),
                               image=GFX["misc"]["play_button"],
                               image_hovered=GFX["misc"]["play_button_hovered"],
                               next_state="GAME"),
                        Button(position=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 50),
                               image=GFX["misc"]["quit_button"],
                               image_hovered=GFX["misc"]["quit_button_hovered"],
                               next_state="EXIT"),
                        ]

    def update(self, keys, now):
        pass

    def draw(self, surface: Surface, interpolate):
        surface.fill((0, 122, 122))
        self.mouse_position = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(surface, self.mouse_position)

    def get_event(self, event: Event):
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_hovered(self.mouse_position):
                        self.next = button.next_state
                        self.done = True
                        if button.next_state == "EXIT":
                            pg.quit()
                            sys.exit()
