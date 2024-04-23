import pygame
from sprites import *
from settings import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.character_sprite_images = SpriteImage("images/character.png")
        self.terrain_sprite_images = SpriteImage("images/terrain2.png")
        self.create_tile_map()

    def create_tile_map(self):
        for i, row in enumerate(tile_map):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "G":
                    Block(self, j, i)
                elif column == "P":
                    Player(self, j, i)

    def new(self):
        """ 
        Calls __init__ method to reset game state
        """
        self.__init__()
        """self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.create_tile_map()"""

    def events(self):
        """Game loop events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        """
        Game Loop updates
        """
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.intro_screen()
    while game.running:
        game.main()
        game.game_over()
    pygame.quit()
    sys.exit()
