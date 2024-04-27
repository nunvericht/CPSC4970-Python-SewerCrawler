import pygame

from ..game_elements import settings


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = settings.BLOCK_LAYER
        super().__init__(self.game.all_sprites, self.game.blocks)

        tile_size = settings.TILE_SIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image1 = self.game.terrain2_sprite_sheet.get_sprite(32, 416, self.width, self.height)
        self.image2 = self.game.terrain_sprite_sheet.get_sprite(290, 640, self.width, self.height)
        self.image3 = self.game.terrain2_sprite_sheet.get_sprite(0, 448, self.width, self.height)

        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.is_stairs = False

    def change_image(self, image_number):
        if image_number == 1:
            self.image = self.image1
        elif image_number == 2:
            self.image = self.image2
            self.is_stairs = True
        elif image_number == 3:
            self.image = self.image3
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
