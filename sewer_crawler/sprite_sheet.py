import pygame
from settings import *


class SpriteSheet:

    def __init__(self, file):
        self.images = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.images, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

    """def __init__(self, image):
        self.sheet = image

    self.sheet = image
    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image"""
