import pygame

from ..game_elements import settings


class SpriteSheet:

    def __init__(self, file):
        self.images = pygame.image.load(file).convert()
        self.black = settings.BLACK

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.images, (0, 0), (x, y, width, height))
        sprite.set_colorkey(self.black)
        return sprite
