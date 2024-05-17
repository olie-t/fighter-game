import pygame
from pygame.sprite import Sprite
import random

class PowerUp(Sprite):
    """A class to represent a power-up."""

    def __init__(self, fg_game, powerup_type):
        """Initialize the power-up."""
        super().__init__()
        self.screen = fg_game.screen
        self.settings = fg_game.settings
        self.powerup_type = powerup_type

        # Font settings for power-up
        self.font = pygame.font.SysFont(None, 48)
        self.color = (255, 0, 0)
        self.text = 'L'

        # Create a rect for the power-up
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        # Start each new power-up at a random position near the enemy's position
        self.rect.x = random.randint(fg_game.screen_rect.left + self.rect.width, fg_game.screen_rect.right - self.rect.width)
        self.rect.y = random.randint(fg_game.screen_rect.top + self.rect.height, fg_game.screen_rect.bottom - self.rect.height)

        # Store the power-up's exact position
        self.x = float(self.rect.x)

    def update(self):
        """Move the power-up to the left."""
        self.x -= self.settings.powerup_speed
        self.rect.x = self.x

    def draw_powerup(self):
        """Draw the power-up at its current location."""
        self.image = self.font.render(self.text, True, self.color)
        self.screen.blit(self.image, self.rect)
