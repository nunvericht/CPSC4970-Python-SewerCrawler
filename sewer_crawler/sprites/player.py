import math

import pygame

from ..game_elements import settings


class Player(pygame.sprite.Sprite):
    """
    Represents main player in game.
    Attributes:
        game (Game): Main game instance.
        _layer (int): Layer index for sprite rendering.
        x (int): x-coordinate of position.
        y (int): y-coordinate of position.
        width (int): Width of sprite.
        height (int): Height of sprite.
        dx (int): Horizontal movement speed.
        dy (int): Vertical movement speed.
        facing (str): Direction player is facing
        animation_loop (int): Loop counter for animations.
        image (pygame.Surface): Current sprite image.
        rect (pygame.Rect): Rectangle representing player's position.
        """
    def __init__(self, game, x, y):
        self.game = game
        self._layer = settings.PLAYER_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.tile_size = settings.TILE_SIZE
        self.x = x * self.tile_size
        self.y = y * self.tile_size
        self.width, self.height = self.tile_size, self.tile_size

        self.dx, self.dy = 0, 0

        # tracks game objective
        self.finished_quest = False

        self.facing = "down"
        self.animation_loop = 1
        self.x_offset = 0
        self.y_offset = 0
        self.image = self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 0 + self.y_offset,
                                                              self.width, self.height)

        self.left_animations = [
            pygame.transform.flip(
                self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 32 + self.y_offset, self.width,
                                                         self.height), True, False),
            pygame.transform.flip(
                self.game.player_sprite_sheet.get_sprite(32 + self.x_offset, 32 + self.y_offset, self.width,
                                                         self.height), True, False),
            pygame.transform.flip(
                self.game.player_sprite_sheet.get_sprite(64 + self.x_offset, 32 + self.y_offset, self.width,
                                                         self.height), True, False)
        ]

        self.right_animations = [
            self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 32 + self.y_offset, self.width, self.height),
            self.game.player_sprite_sheet.get_sprite(32 + self.x_offset, 32 + self.y_offset, self.width, self.height),
            self.game.player_sprite_sheet.get_sprite(64 + self.x_offset, 32 + self.y_offset, self.width, self.height)
            ]

        self.up_animations = [
            self.game.player_sprite_sheet.get_sprite(64 + self.x_offset, 0 + self.y_offset, self.width, self.height),
            self.game.player_sprite_sheet.get_sprite(96 + self.x_offset, 0 + self.y_offset, self.width, self.height),
            ]

        self.down_animations = [
            self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 0 + self.y_offset, self.width, self.height),
            self.game.player_sprite_sheet.get_sprite(32 + self.x_offset, 0 + self.y_offset, self.width, self.height),
            ]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = settings.PLAYER_SPEED
        self.collide_with_stairs = False

    def update(self):
        self.movement()
        self.animate()
        self.collide_bad_guys()
        self.collide_npc()

        self.rect.x += self.dx
        self.collide_block("x")
        self.rect.y += self.dy
        self.collide_block("y")

        self.dx, self.dy = 0, 0

    def movement(self):
        """Keys pressed"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx -= self.speed
            self.facing = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx += self.speed
            self.facing = "right"
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.dy -= self.speed
            self.facing = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.dy += self.speed
            self.facing = "down"

    def collide_block(self, direction):
        """Collisions with blocks including stairs"""
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            for block in hits:
                if block.is_stairs:
                    self.collide_with_stairs = True
                else:
                    if direction == "x":
                        if self.dx > 0:
                            self.rect.x = block.rect.left - self.rect.width
                        elif self.dx < 0:
                            self.rect.x = block.rect.right
                    elif direction == "y":
                        if self.dy > 0:
                            self.rect.y = block.rect.top - self.rect.height
                        elif self.dy < 0:
                            self.rect.y = block.rect.bottom

    def collide_bad_guys(self):
        hits = pygame.sprite.spritecollide(self, self.game.bad_guys, False)
        if hits:
            self.kill()
            self.finished_quest = False
            self.game.playing = False

    def collide_npc(self):
        hits = pygame.sprite.spritecollide(self, self.game.npc_group, False)
        if hits:
            self.finished_quest = True
            self.game.playing = False

    def animate(self):
        if self.facing == "left":
            if self.dx == 0:
                self.image = pygame.transform.flip(
                    self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 32 + self.y_offset, self.width,
                                                             self.height), True, False)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.dx == 0:
                self.image = self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 32 + self.y_offset,
                                                                      self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 1

        if self.facing == "down":
            if self.dy == 0:
                self.image = self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 0 + self.y_offset,
                                                                      self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.dy == 0:
                self.image = self.game.player_sprite_sheet.get_sprite(0 + self.x_offset, 0 + self.y_offset,
                                                                      self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 1
