import pygame

from settings import *


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = GROUND_LAYER
        super().__init__(self.groups)

        tile_size = TILE_SIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.terrain2_sprite_sheet.get_sprite(32, 64, self.width, self.height)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
