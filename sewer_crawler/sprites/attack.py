import math

import pygame

from ..game_elements import settings


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = settings.PLAYER_LAYER
        super().__init__(self.game.attacks)
        self.game.all_sprites.add(self.game.attacks)

        self.tile_size = settings.TILE_SIZE
        self.x = x
        self.y = y
        self.width, self.height = self.tile_size, self.tile_size

        self.animation_loop = 0
        self.image = self.game.attack_sprite_sheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [
            self.game.attack_sprite_sheet.get_sprite(3, 96, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(32, 96, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(64, 96, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(96, 96, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(128, 96, self.width, self.height)
        ]

        self.right_animations = [
            self.game.attack_sprite_sheet.get_sprite(3, 64, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(32, 64, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(64, 64, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(96, 64, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(128, 64, self.width, self.height)
        ]

        self.up_animations = [
            self.game.attack_sprite_sheet.get_sprite(3, 3, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(32, 3, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(64, 3, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(96, 3, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(128, 3, self.width, self.height)
            ]

        self.down_animations = [
            self.game.attack_sprite_sheet.get_sprite(3, 32, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(32, 32, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(64, 32, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(96, 32, self.width, self.height),
            self.game.attack_sprite_sheet.get_sprite(128, 32, self.width, self.height)
        ]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.bad_guys, True)
        return hits

    def animate(self):
        direction = self.game.player.facing
        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
