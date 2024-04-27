import settings


class Camera:
    def __init__(self, screen_width, screen_height):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = settings.MAP_WIDTH
        self.map_height = settings.MAP_HEIGHT

    def update(self, player_rect):
        """Centers the camera on the player"""
        self.x = player_rect.centerx - self.screen_width // 2
        self.y = player_rect.centery - self.screen_height // 2

        self.x = max(0, min(self.x, self.map_width - self.screen_width))
        self.y = max(0, min(self.y, self.map_height- self.screen_height))

    def apply(self, rect):
        return rect.move(-self.x, -self.y)
