import sys
import pygame

from bullet import Bullet
from plane import Plane
from settings import Settings
from enemy import EnemyPlane


class FighterGame:
    """Overall class for the game"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Fighter Game")

        # Game assets
        self.plane = Plane(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()


        self.bg_colour = self.settings.bg_colour

    def run_game(self):
        """Start the main loop to run the game"""

        while True:
            self._check_events()
            self.plane.update()
            self._update_enemies()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(120)

    def _update_screen(self):
        """Handle updates to the screen"""
        self.screen.fill(self.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.plane.blitme()
        pygame.display.flip()

    def _check_events(self):
        """Watch for keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_d:
            self.plane.moving_right = True
        elif event.key == pygame.K_a:
            self.plane.moving_left = True
        elif event.key == pygame.K_w:
            self.plane.moving_up = True
        elif event.key == pygame.K_s:
            self.plane.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()


    def _check_keyup_events(self, event):
        """ Respond to key releases  """
        if event.key == pygame.K_d:
            self.plane.moving_right = False
        elif event.key == pygame.K_a:
            self.plane.moving_left = False
        elif event.key == pygame.K_w:
            self.plane.moving_up = False
        elif event.key == pygame.K_s:
            self.plane.moving_down = False

    def _fire_bullets(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update the bullets """
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_rect.right:
                self.bullets.remove(bullet)

    def _create_enemy(self, position_x, position_y):
        """Create and enemy ship"""

        new_enemy = EnemyPlane(self)
        new_enemy.x = position_x
        new_enemy.y = position_y
        self.enemies.add(new_enemy)

    def _create_fleet(self):
        """ Create an enemy fleet """
        print("Spawning")
        enemy = EnemyPlane(self)
        enemy_width, enemy_height = enemy.rect.size
        current_x, current_y = enemy_width, enemy_height
        while current_y < (self.settings.screen_height * enemy_height):
            self._create_enemy(current_x,current_y)
            current_y += 1.5 * enemy_height

    def _update_enemies(self):
        """ Update enemy positions"""
        self.enemies.update()


if __name__ == "__main__":
    fg = FighterGame()
    fg.run_game()
