import pygame
from pygame.sprite import Sprite

class EnemyPlane(Sprite):
    """A Class to represent enemies planes"""

    def __init__(self, fg_game, direction):

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

        #set the speed of the enemy
        self.speed = 1.0
        self.direction = direction

    def update(self):
        """Move the plane"""
        self.y -= self.direction * self.settings.enemy_speed
        self.x -= self.settings.enemy_speed
        self.rect.y = self.y
        self.rect.x = self.x

        # Check for edges and change direction if needed
        if self.check_edges():
            self.direction *= -1

    def check_edges(self):
        """Return true if an enemy is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom:
            return True
        if self.rect.left <= 0 or self.rect.right >= screen_rect.right:
            return True
        return False

    def blitme(self):
        """Draw the enemy plane at its current location."""
        self.screen.blit(self.image, self.rect)