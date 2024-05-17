import sys
import pygame
import random

from bullet import Bullet
from plane import Plane
from settings import Settings
from enemy import EnemyPlane
from background import Tree


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
        self.trees = pygame.sprite.Group()

        self.bg_colour = self.settings.bg_colour

        # time tracking for fleet spawning
        self.last_fleet_spawn_time = pygame.time.get_ticks()
        self.next_fleet_spawn_time = self._get_next_fleet_spawn_time()

        #score tracking
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)

        self._create_brown_tree()

    def run_game(self):
        """Start the main loop to run the game"""
        self._create_fleet()
        while True:
            self._check_events()
            self.plane.update()
            self._maybe_spawn_fleet()
            self._update_enemies()
            self._update_bullets()
            self._update_trees()
            self._update_screen()
            self.clock.tick(120)



    def _update_screen(self):
        """Handle updates to the screen"""
        self.screen.fill(self.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for tree in self.trees.sprites():
            tree.draw_tree()
        self.plane.blitme()
        self.enemies.draw(self.screen)
        self._draw_score()
        pygame.display.flip()

    def _draw_score(self):
        """Draw the score on the screen"""
        score_str = str(self.score)
        score_image = self.font.render(score_str, True, (30, 30, 30))
        self.screen.blit(score_image, (20, 20))

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

    def _create_brown_tree(self):
        """Create initial brown trees in the background"""
        for _ in range(20):  # Number of initial brown pixels
            new_tree = Tree(self, True)
            self.trees.add(new_tree)
            print("new tree")

    def _update_trees(self):
        self.trees.update()
        for tree in self.trees.copy():
            if tree.rect.right <= 0:
                self.trees.remove(tree)
                new_tree = Tree(self)
                self.trees.add(new_tree)
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

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

        if collisions:
            for enemies in collisions.values():
                self.score += 10 * len(enemies)

    def _create_enemy(self, position_x, position_y, direction):
        """Create an enemy ship"""

        new_enemy = EnemyPlane(self, direction)  # Pass direction to EnemyPlane
        new_enemy.x = position_x
        new_enemy.y = position_y
        new_enemy.rect.x = position_x
        new_enemy.rect.y = position_y
        self.enemies.add(new_enemy)


    def _create_fleet(self):
        """Create an enemy fleet"""
        num_enemies = random.randint(5, 12)  # Random number of enemies
        direction = random.choice([-1, 1])  # Randomize initial direction
        enemy_width, enemy_height = EnemyPlane(self, direction).rect.size  # Pass direction to EnemyPlane
        current_x = self.settings.screen_width - enemy_width
        current_y = enemy_height

        for _ in range(num_enemies):
            self._create_enemy(current_x, current_y, direction)
            current_y += 1.5 * enemy_height
            if current_y > self.settings.screen_height - enemy_height:
                break

    def _maybe_spawn_fleet(self):
        """Check the time and spawn a new fleet if needed"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fleet_spawn_time >= self.next_fleet_spawn_time:
            self._create_fleet()
            self.last_fleet_spawn_time = current_time
            self.next_fleet_spawn_time = self._get_next_fleet_spawn_time()

    def _get_next_fleet_spawn_time(self):
        return random.randint(1500, 5000)


    def _update_enemies(self):
        """ Update enemy positions"""
        self.enemies.update()

        """Check for enemies at the left of the screen and remove any that make it"""
        for enemy in self.enemies.copy():
            if enemy.rect.right <= 0:
                self.enemies.remove(enemy)


if __name__ == "__main__":
    fg = FighterGame()
    fg.run_game()
