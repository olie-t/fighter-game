import sys
import pygame
import random

from bullet import Bullet
from plane import Plane
from settings import Settings
from enemy import EnemyPlane
from background import Tree
from scoreboard import Scoreboard
from button import Button
from powerup import PowerUp

class FighterGame:
    """Overall class for the game"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Fighter Game")

        # Game states
        self.game_active = True
        self.game_over = False

        # Game assets
        self.plane = Plane(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.bg_colour = self.settings.bg_colour

        # Time tracking for fleet spawning
        self.last_fleet_spawn_time = pygame.time.get_ticks()
        self.next_fleet_spawn_time = self._get_next_fleet_spawn_time()

        # Score and lives tracking
        self.score = 0
        self.lives = 3

        # Initialize scoreboard
        self.sb = Scoreboard(self)
        # Initialize play again button
        self.play_button = Button(self, "Play Again")

        # Create initial trees
        self._create_initial_trees()

    def run_game(self):
        """Start the main loop to run the game"""
        self._create_fleet()
        while True:
            self._check_events()
            if self.game_active:
                self.plane.update()
                self._maybe_spawn_fleet()
                self._update_enemies()
                self._update_bullets()
                self._update_powerups()  # Update power-ups
                self._update_trees()  # Update trees
                self._check_collisions()  # Check for collisions
            self._update_screen()
            self.clock.tick(120)

    def _update_screen(self):
        """Handle updates to the screen"""
        self.screen.fill(self.bg_colour)
        for tree in self.trees.sprites():
            tree.draw_tree()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for powerup in self.powerups.sprites():
            powerup.draw_powerup()
        self.plane.blitme()
        self.enemies.draw(self.screen)
        self.sb.show_score()
        self.sb.show_lives()
        if not self.game_active and self.game_over:
            self.sb.show_final_score()
            self.play_button.draw_button()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self._check_play_button(mouse_x, mouse_y)

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
        """Respond to key releases"""
        if event.key == pygame.K_d:
            self.plane.moving_right = False
        elif event.key == pygame.K_a:
            self.plane.moving_left = False
        elif event.key == pygame.K_w:
            self.plane.moving_up = False
        elif event.key == pygame.K_s:
            self.plane.moving_down = False

    def _check_play_button(self, mouse_x, mouse_y):
        """Start a new game when the player clicks Play Again"""
        if self.play_button.rect.collidepoint(mouse_x, mouse_y):
            self._restart_game()

    def _create_initial_trees(self):
        """Create initial brown trees in the background at random positions"""
        for _ in range(20):  # Number of initial trees
            new_tree = Tree(self, initial=True)
            self.trees.add(new_tree)

    def _update_trees(self):
        """Update positions of trees and create new ones if necessary"""
        self.trees.update()
        for tree in self.trees.copy():
            if tree.rect.right <= 0:
                self.trees.remove(tree)
                new_tree = Tree(self, initial=False)
                self.trees.add(new_tree)

    def _fire_bullets(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the bullets and check for collisions with enemies"""
        self.bullets.update()

        # Remove bullets that have moved off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_rect.right:
                self.bullets.remove(bullet)

        # Check for collisions between bullets and enemies
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

        if collisions:
            for enemies in collisions.values():
                self.score += 10 * len(enemies)
                self.sb.prep_score()  # Update the score display
                self._maybe_drop_powerup(enemies[0])  # Drop a power-up

    def _maybe_drop_powerup(self, enemy):
        """Randomly drop a power-up from the destroyed enemy"""
        if random.random() < self.settings.powerup_drop_chance:
            powerup = PowerUp(self, 'extra_life')
            powerup.rect.center = enemy.rect.center
            self.powerups.add(powerup)

    def _update_powerups(self):
        """Update power-ups and check for collisions with the plane"""
        self.powerups.update()

        # Remove power-ups that have moved off the screen
        for powerup in self.powerups.copy():
            if powerup.rect.left <= 0:
                self.powerups.remove(powerup)

        # Check for collisions between the plane and power-ups
        collisions = pygame.sprite.spritecollide(self.plane, self.powerups, True)
        if collisions:
            for powerup in collisions:
                if powerup.powerup_type == 'extra_life':
                    self.lives += 1
                    self.sb.prep_lives()  # Update the lives display

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
        """Generate a random time between 1.5 and 5 seconds for the next fleet spawn"""
        return random.randint(1500, 5000)

    def _update_enemies(self):
        """Update enemy positions"""
        self.enemies.update()

        # Check for enemies at the left of the screen and remove any that make it
        for enemy in self.enemies.copy():
            if enemy.rect.right <= 0:
                self.enemies.remove(enemy)

    def _check_collisions(self):
        """Check for collisions between the player's plane and enemies"""
        if pygame.sprite.spritecollideany(self.plane, self.enemies):
            self._plane_hit()

    def _plane_hit(self):
        """Respond to the player being hit by an enemy"""
        if self.lives > 0:
            self.lives -= 1
            self.sb.prep_lives()  # Update the lives display
            self._reset_game()
        else:
            self._game_over()

    def _reset_game(self):
        """Reset the game state after the player loses a life"""
        self.enemies.empty()
        self.bullets.empty()
        self.powerups.empty()
        self.plane.center_plane()
        self._create_fleet()

    def _game_over(self):
        """Handle the game over state"""
        self.game_active = False
        self.game_over = True
        self.sb.show_final_score()
        self.play_button.draw_button()

    def _restart_game(self):
        """Restart the game"""
        self.score = 0
        self.lives = 3
        self.game_active = True
        self.game_over = False
        self.sb.prep_score()
        self.sb.prep_lives()
        self._reset_game()

if __name__ == "__main__":
    fg = FighterGame()
    fg.run_game()
