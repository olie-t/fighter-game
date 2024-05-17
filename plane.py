import pygame


class Plane:
    """A class to manage to player sprite"""

    def __init__(self, fg_game):
        self.screen = fg_game.screen
        self.screen_rect = fg_game.screen.get_rect()
        self.settings = fg_game.settings

        # Load the plane image and set its rectangle
        self.image = pygame.image.load('images/fighter.bmp')
        self.rect = self.image.get_rect()

        # Start the plane at the center left of the screen
        self.rect.midleft = self.screen_rect.midleft

        # Store a float of the planes exact position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags, start with a plane that's not moving
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.plane_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.plane_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.plane_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.plane_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
