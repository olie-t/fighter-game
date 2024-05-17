import random
import os

import pygame
from pygame.sprite import Sprite

class Tree(Sprite):
    """A class to represent a rudimentary tree"""

    def __init__(self, fg_game, initial=False):
        super().__init__()
        self.screen = fg_game.screen
        self.settings = fg_game.settings
        self.images_folder = 'images/trees/'
        self.images = [os.path.join(self.images_folder, f) for f in os.listdir(self.images_folder)]

        self.image_path = random.choice(self.images)
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect()
        if initial:
            self.rect.x = random.randint(0, self.settings.screen_width)
        else:
            self.rect.x = self.settings.screen_width
        self.rect.y = random.randint(0, self.settings.screen_height)
        self.x = float(self.rect.x)
        self.speed = 1.2

    def update(self):
        """Move the tree left across the screen."""
        self.x -= self.speed
        self.rect.x = self.x

    def draw_tree(self):
        """Draw the tree to the screen."""
        self.screen.blit(self.image, self.rect)