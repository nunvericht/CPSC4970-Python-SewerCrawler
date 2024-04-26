import math
import random

import pygame
from settings import *


class BadGuy(pygame.sprite.Sprite):
    """
    Represents an enemy character in the game in bad_guy group.
    Attributes:
        game (Game): Main game instance.
        _layer (int): Layer index for sprite rendering.
        x (int): x-coordinate of enemy position.
        y (int): y-coordinate of enemy position.
        width (int): Width of sprite.
        height (int): Height of sprite.
        dx (int): Horizontal movement speed.
        dy (int): Vertical movement speed.
        facing (str): The direction enemy is facing
        animation_loop (int): Loop counter for animations.
        movement_loop (int): Loop counter for movement.
        max_travel (int): Maximum travel distance for enemy.
        image (pygame.Surface): The current sprite image.
        rect (pygame.Rect): The rectangle representing enemy's position.
        """
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BAD_GUY_LAYER
        super().__init__(self.game.bad_guys)
        self.game.all_sprites.add(self.game.bad_guys)

        tile_size = TILE_SIZE
        self.x = x * tile_size
        self.y = y * tile_size
        self.width, self.height = tile_size, tile_size

        self.dx, self.dy = 0, 0
        self.facing = random.choice(["up", "down"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(32, 64)

        self.image = self.game.bad_guys_sprite_sheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [
            self.game.bad_guys_sprite_sheet.get_sprite(3, 98, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(35, 98, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(68, 98, self.width, self.height)
            ]

        self.right_animations = [
            self.game.bad_guys_sprite_sheet.get_sprite(3, 66, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(35, 66, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(68, 66, self.width, self.height)
            ]

        self.up_animations = [
            self.game.bad_guys_sprite_sheet.get_sprite(3, 34, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(35, 34, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(68, 34, self.width, self.height)
            ]

        self.down_animations = [
            self.game.bad_guys_sprite_sheet.get_sprite(3, 2, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(35, 2, self.width, self.height),
            self.game.bad_guys_sprite_sheet.get_sprite(68, 2, self.width, self.height)
            ]

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.dx
        self.rect.y += self.dy

        self.dx, self.dy = 0, 0

    def movement(self):
        if self.facing == "left":
            self.dx -= BAD_GUY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.dx += BAD_GUY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"
        if self.facing == "up":
            self.dy -= BAD_GUY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "down"
        if self.facing == "down":
            self.dy += BAD_GUY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "up"

    def animate(self):
        if self.facing == "left":
            if self.dx == 0:
                self.image = self.game.bad_guys_sprite_sheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.dx == 0:
                self.image = self.game.bad_guys_sprite_sheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.dy == 0:
                self.image = self.game.bad_guys_sprite_sheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "down":
            if self.dy == 0:
                self.image = self.game.bad_guys_sprite_sheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1