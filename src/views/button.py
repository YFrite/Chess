from pygame import Surface


class Button:
    def __init__(self, position: tuple[int, int],
                 next_state: str, image, image_hovered):
        self.next_state = next_state

        self.image = image
        self.image_hovered = image_hovered
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, surface: Surface, position: tuple[int, int]):
        if self.is_hovered(position):
            surface.blit(self.image_hovered, self.rect)
        else:
            surface.blit(self.image, self.rect)

    def is_hovered(self, position: tuple[int, int]):
        return (position[0] in range(self.rect.left, self.rect.right) and
                position[1] in range(self.rect.top, self.rect.bottom))
