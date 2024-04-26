import pygame


class Button:
    def __init__(self, x, y, width, height, fg_color, bg_color, content, font_size):
        self.font = pygame.font.Font("../main_game/fonts/DinoJumps.otf", font_size)
        self.content = content
        self.rect = pygame.Rect(x, y, width, height)
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.image = pygame.Surface(self.rect.size)
        self._render_text()

    def _render_text(self):
        self.text = self.font.render(self.content, True, self.fg_color)
        self.text_rect = self.text.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.fill(self.bg_color)
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, position, pressed):
        return self.rect.collidepoint(position) and pressed[0]
