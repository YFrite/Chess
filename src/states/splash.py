from src.settings import BACKGROUND_COLOR, RESOURCES, SCREEN_RECT, SCREEN_SIZE
from src.state_machine import _State


class Splash(_State):
    def __init__(self):
        super().__init__()
        self.next = "MENU"
        self.timeout = 1
        self.alpha = 50
        self.alpha_speed = 0
        self.text = RESOURCES["fonts"]["oswald"].render("Project by Python for hour", True, "black")
        # self.image = RESOURCES["misc"]['splash']
        # self.image.set_alpha(self.alpha)
        self.rect = self.text.get_rect(center=SCREEN_RECT.center)

    def update(self, keys, now):
        self.now = now
        self.alpha = min(self.alpha + self.alpha_speed, 255)
        if self.now - self.start_time > 1000.0 * self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        surface.fill(BACKGROUND_COLOR)
        surface.blit(self.text,
                     self.rect)

    def get_event(self, event):
        pass
