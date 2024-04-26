import math

import pygame
from settings import *


class FlameSkeleton(pygame.sprite.Sprite):
    """
    Represents an enemy character in bad_guys group that moves in clockwise patter.
    Attributes:
        game (Game): Main game instance.
        _layer (int): Layer index for sprite rendering.
        x (int): x-coordinate of enemy position.
        y (int): y-coordinate of enemy position.
        width (int): Width of sprite.
        height (int): Height of sprite.
        dx (int): Horizontal movement speed.
        dy (int): Vertical movement speed.
        facing (str): Direction enemy is facing
        animation_loop (int): Loop counter for animations.
        movement_loop (int): Loop counter for movement.
        max_travel (int): Maximum travel distance for enemy.
        image (pygame.Surface): Current sprite image.
        rect (pygame.Rect): Rectangle representing enemy's position.
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
        self.facing = "up"
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 32

        self.x_offset = 0
        self.y_offset = 4
        flame_skeleton_image = self.game.skeletons_sprite_sheet.get_sprite(0 + self.x_offset, 32 + self.y_offset,
                                                                           self.width, self.height)
        self.image = pygame.transform.scale(flame_skeleton_image, (48, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        left_frames = [(0 + self.x_offset, 288 + self.y_offset), (32 + self.x_offset, 288 + self.y_offset),
                       (64 + self.x_offset, 288 + self.y_offset)]
        self.left_animations = [
            pygame.transform.scale(self.game.skeletons_sprite_sheet.get_sprite(*frame, self.width, self.height),
                                   (48, 48))
            for frame in left_frames
        ]

        right_frames = [
            (0 + self.x_offset, 320 + self.y_offset), (32 + self.x_offset, 320 + self.y_offset),
            (64 + self.x_offset, 320 + self.y_offset)
        ]
        self.right_animations = [
            pygame.transform.scale(self.game.skeletons_sprite_sheet.get_sprite(*frame, self.width, self.height),
                                   (48, 48))
            for frame in right_frames
            ]

        up_frames = [
            (0 + self.x_offset, 352 + self.y_offset), (32 + self.x_offset, 352 + self.y_offset),
            (64 + self.x_offset, 352 + self.y_offset)
            ]
        self.up_animations = [
            pygame.transform.scale(self.game.skeletons_sprite_sheet.get_sprite(*frame, self.width, self.height),
                                   (48, 48))
            for frame in up_frames
            ]

        down_frames = [(0 + self.x_offset, 256 + self.y_offset), (32 + self.x_offset, 256 + self.y_offset),
                       (64 + self.x_offset, 256 + self.y_offset)]
        self.down_animations = [
            pygame.transform.scale(self.game.skeletons_sprite_sheet.get_sprite(*frame, self.width, self.height),
                                   (48, 48))
            for frame in down_frames
            ]

    def movement(self):
        if self.facing == "left":
            self.dx -= BAD_GUY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "up"
        if self.facing == "up":
            self.dy -= BAD_GUY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.dx += BAD_GUY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "down"
        if self.facing == "down":
            self.dy += BAD_GUY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"

    def animate(self):
        if self.facing == "left":
            if self.dx == 0:
                self.image = self.game.skeletons_sprite_sheet.get_sprite(0 + self.x_offset, 352 + self.y_offset,
                                                                         self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.dx == 0:
                self.image = self.game.skeletons_sprite_sheet.get_sprite(0 + self.x_offset, 320 + self.y_offset,
                                                                         self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.dy == 0:
                self.image = self.game.skeletons_sprite_sheet.get_sprite(0 + self.x_offset, 288 + self.y_offset,
                                                                         self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "down":
            if self.dy == 0:
                self.image = self.game.skeletons_sprite_sheet.get_sprite(0 + self.x_offset, 256 + self.y_offset,
                                                                         self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dx, self.dy = 0, 0
