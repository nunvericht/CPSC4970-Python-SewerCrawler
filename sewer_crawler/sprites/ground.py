import pygame

from sewer_crawler.game_elements import settings


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = settings.GROUND_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        tile_size = settings.TILE_SIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.terrain2_sprite_sheet.get_sprite(32, 64, self.width, self.height)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
