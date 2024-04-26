import sys

import pygame
from attack import Attack
from bad_guys import BadGuy
from block import Block
from button import Button
from camera import Camera
from flame_skeletons import FlameSkeleton
from ground import Ground
from npc import NPC
from player import Player
from settings import *
from skeletons import Skeleton
from sprite_sheet import SpriteSheet


class Game:
    """Game environment, including initialization.
        Attributes:
            screen: Pygame display surface for rendering game.
            screen_width (int): Width of game screen.
            screen_height (int): Height of game screen.
            clock: Pygame clock for managing frame rate.
            font: Pygame font for text rendering.
            running (bool): Flag indicating if game loop is running.
            playing (bool): Flag indicating if game is currently being played.
            all_sprites: Pygame sprite group containing all game sprites.
            blocks: Pygame sprite group for block objects.
            bad_guys: Pygame sprite group for enemy characters.
            attacks: Pygame sprite group for attack animations.
            npc_group: Pygame sprite group for non-player characters.
            player_sprite_sheet: Sprite sheet for character animations.
            dino_sprite: Sprite image for dinosaur animations.
            terrain_sprite_sheet: Sprite sheet for terrain graphics.
            terrain2_sprite_sheet: Additional sprite sheet for terrain variations.
            bad_guys_sprite_sheet: Sprite sheet for enemy character animations (BoundWorlds project/opengameart.org)
            skeletons_sprite_sheet: Sprite sheet for skeleton animations (BoundWorlds project/opengameart.org).
            npc_image: Scaled image of a friendly dinosaur NPC (create.microsoft.com).
            attack_sprite_sheet: Sprite sheet for attack animations.
            start_background: Image for game start screen background.
            game_over_background: Image for game over screen background.
            player: Player character instance.
            camera: Camera object for managing view.
            current_level (int): Current level of the game.
        """

    def __init__(self):
        """Game init"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("fonts/DinoJumps.otf", 48)
        self.running = True
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.bad_guys = pygame.sprite.LayeredUpdates()
        self.flame_skeletons = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npc_group = pygame.sprite.LayeredUpdates()
        self.player_sprite_sheet = SpriteSheet("images/the_knight.png")
        self.dino_sprite = SpriteSheet("images/dino.png")
        self.terrain_sprite_sheet = SpriteSheet("images/terrain.png")
        self.terrain2_sprite_sheet = SpriteSheet("images/terrain2.png ")
        self.bad_guys_sprite_sheet = SpriteSheet("images/bad_guys.png")
        self.skeletons_sprite_sheet = SpriteSheet("images/skeleton.png")
        dino_npc_image = pygame.image.load("images/friendly_dino.png")
        self.npc_image = pygame.transform.scale(dino_npc_image, (128, 128))
        self.attack_sprite_sheet = SpriteSheet("images/attack.png")
        self.start_background = pygame.image.load("images/start_background.png")
        self.game_over_background = pygame.image.load("images/game_over.png")
        self.player = Player(self, 5, 5)
        self.camera = Camera(self.screen_width, self.screen_height)
        self.current_level = 0

    def create_tile_map(self, current_level):
        if current_level == 0:
            tile_map = tile_map1
        else:
            tile_map = tile_map2
        for i, row in enumerate(tile_map):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "G":
                    Block(self, j, i)
                if column == "W":
                    wall = Block(self, j, i)
                    wall.change_image(image_number=3)
                elif column == "S":
                    stairs = Block(self, j, i)
                    stairs.change_image(image_number=2)
                elif column == "E":
                    Skeleton(self, j, i)
                elif column == "F":
                    FlameSkeleton(self, j, i)
                elif column == "B":
                    BadGuy(self, j, i)
                elif column == "D":
                    NPC(self, j, i)

    def events(self):
        """Game loop events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y-TILE_SIZE)
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TILE_SIZE, self.player.rect.y)

    def update(self):
        """
        Game Loop updates
        """
        self.player.movement()
        self.camera.update(self.player.rect)
        self.all_sprites.update()
        if self.player.collide_with_stairs:
            self.level_change()
        elif self.player.finished_quest:
            self.handle_game_over("Quest Complete", self.start_background)

    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def new(self):
        """
        Calls __init__ method to reset game state
        """
        self.__init__()
        self.load_level(self.current_level)

    def level_change(self):
        """
        Calls __init__ method to reset game state before loading next level
        """
        self.__init__()
        self.current_level += 1
        self.load_level(self.current_level)

    def load_level(self, level_number):
        """Call create tile_map method with the corresponding level number"""
        self.create_tile_map(level_number)

    def handle_game_over(self, title_text, background_image):
        """
        Handles game over scenario.
        """
        game_over = True
        title = self.font.render(title_text, True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        restart_button = Button(WINDOW_WIDTH // 2 - 125, WINDOW_HEIGHT // 2 + 30, 250, 50, GREEN,
                                BLACK, "Play Again", 36)
        for sprite in self.all_sprites:
            sprite.kill()
        while game_over and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    self.running = False
            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if restart_button.is_pressed(mouse_position, mouse_pressed):
                game_over = False
                self.new()
                self.main()
            self.screen.blit(background_image, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def start_menu(self):
        intro = True
        title = self.font.render("Sewer Crawler", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        subtitle = self.font.render("Defeat baddies and find dino", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        play_button = Button(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 30, 100, 50, GREEN,
                             BLACK, "Play", 36)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_position, mouse_pressed):
                intro = False
            self.screen.blit(self.start_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.start_menu()
    game.load_level(game.current_level)
    while game.running:
        game.main()
        game.handle_game_over("Game Over", game.game_over_background)
    pygame.quit()
    sys.exit()
