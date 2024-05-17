import pygame
from pygame.sprite import Sprite

class EnemyPlane(Sprite):
    """A Class to represent enemies planes"""

    def __init__(self, fg_game):

        super().__init__()
        self.screen = fg_game.screen
        self.settings = fg_game.settings

        # Load the image to be used for the plane
        self.image = pygame.image.load('images/enemy1.bmp')
        self.rect = self.image.get_rect()

        #start each new enemy near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the exact postion
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the plane"""
        self.y -= self.settings.enemy_speed
        self.rect.y = self.y

    def check_edges(self):
        """Return true if an alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.top > 0) or (self.rect.bottom >= screen_rect.bottom)