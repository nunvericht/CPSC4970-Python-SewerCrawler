from settings import *


class Camera:
    def __init__(self, screen_width, screen_height):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, player_rect):
        """Centers the camera on the player"""
        self.x = player_rect.centerx - self.screen_width // 2
        self.y = player_rect.centery - self.screen_height // 2

        self.x = max(0, min(self.x, MAP_WIDTH - self.screen_width))
        self.y = max(0, min(self.y, MAP_HEIGHT - self.screen_height))

    def apply(self, rect):
        return rect.move(-self.x, -self.y)
