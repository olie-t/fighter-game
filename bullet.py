import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ A class to manage bullets fired from the plane"""

    def __init__(self, fg_game):
        """ Create a bullet at the present plane location """
        super().__init__()
        self.screen = fg_game.screen
        self.settings = fg_game.settings
        self.colour = self.settings.bullet_colour

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midleft = fg_game.plane.rect.midright

        self.x = float(self.rect.x)

    def update(self):
        """ Move the bullet """
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """ Draw the bullet """
        pygame.draw.rect(self.screen, self.colour, self.rect)
