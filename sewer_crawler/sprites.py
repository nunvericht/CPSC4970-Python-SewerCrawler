import pygame

from settings import *
import math
import random


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        super().__init__(self.groups)
        # pygame.sprite.Sprite.__init__(self, self.groups)

        tile_size = TILESIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.terrain_sprite_images.get_sprite(448, 416, self.width, self.height)
        """self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)"""

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites
        self._layer = GROUND_LAYER
        super().__init__(self.groups)

        tile_size = TILESIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.terrain_sprite_images.get_sprite(32, 64, self.width, self.height)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class SpriteImage:
    def __init__(self, file):
        self.images = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.images, (0,  0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        # pygame.sprite.Sprite.__init__(self, self.groups)
        super().__init__(self.groups)

        tile_size = TILESIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width, self.height = tile_size, tile_size

        self.x_change, self.y_change = 0, 0

        self.facing = "down"
        self.animation_loop = 1

        self.image = self.game.character_sprite_images.get_sprite(3, 2, self.width, self.height)
        """image_file = pygame.image.load("images/single.png")
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey(BLACK)
        self.image.blit(image_file, (0, 0))"""

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = PLAYER_SPEED

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_block("x")
        self.rect.y += self.y_change
        self.collide_block("y")

        self.x_change, self.y_change = 0, 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= self.speed
            self.facing = "left"
        elif keys[pygame.K_LEFT]:
            self.x_change -= self.speed
            self.facing = "left"
        elif keys[pygame.K_d]:
            self.x_change += self.speed
            self.facing = "right"
        elif keys[pygame.K_RIGHT]:
            self.x_change += self.speed
            self.facing = "right"
        elif keys[pygame.K_w]:
            self.y_change -= self.speed
            self.facing = "up"
        elif keys[pygame.K_UP]:
            self.y_change -= self.speed
            self.facing = "up"
        elif keys[pygame.K_s]:
            self.y_change += self.speed
            self.facing = "down"
        elif keys[pygame.K_DOWN]:
            self.y_change += self.speed
            self.facing = "down"

    def collide_block(self, direction):
        if direction == "x":
            hit_block = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hit_block:
                if self.x_change > 0:
                    self.rect.x = hit_block[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hit_block[0].rect.right

        if direction == "y":
            hit_block = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hit_block:
                if self.y_change > 0:
                    self.rect.y = hit_block[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hit_block[0].rect.bottom

    def animate(self):
        down_animations = [self.game.character_sprite_images.get_sprite(3, 2, self.width, self.height),
                           self.game.character_sprite_images.get_sprite(35, 2, self.width, self.height),
                           self.game.character_sprite_images.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_sprite_images.get_sprite(3, 34, self.width, self.height),
                            self.game.character_sprite_images.get_sprite(35, 34, self.width, self.height),
                            self.game.character_sprite_images.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_sprite_images.get_sprite(3, 98, self.width, self.height),
                            self.game.character_sprite_images.get_sprite(35, 98, self.width, self.height),
                            self.game.character_sprite_images.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_sprite_images.get_sprite(3, 66, self.width, self.height),
                            self.game.character_sprite_images.get_sprite(35, 66, self.width, self.height),
                            self.game.character_sprite_images.get_sprite(68, 66, self.width, self.height)]

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_sprite_images.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_sprite_images.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_sprite_images.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_sprite_images.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

