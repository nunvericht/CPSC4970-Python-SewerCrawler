import pygame

from ..game_elements import settings


class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = settings.NPC_LAYER
        super().__init__(self.game.npc_group)
        self.game.all_sprites.add(self.game.npc_group)

        tile_size = settings.TILE_SIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.npc_image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
