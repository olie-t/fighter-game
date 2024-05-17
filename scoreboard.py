import pygame

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, fg_game):
        """Initialize scorekeeping attributes."""
        self.fg_game = fg_game
        self.screen = fg_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = fg_game.settings
        self.stats = fg_game

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_lives()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_colour)

        # Display the score at the top left of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)

    def prep_lives(self):
        """Turn the lives into a rendered image."""
        lives_str = f"Lives: {self.stats.lives}"
        self.lives_image = self.font.render(lives_str, True, self.text_color, self.settings.bg_colour)

        # Display the lives at the top left of the screen below the score
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.screen_rect.left + 20
        self.lives_rect.top = self.score_rect.bottom + 10

    def show_lives(self):
        """Draw lives to the screen."""
        self.screen.blit(self.lives_image, self.lives_rect)

    def show_final_score(self):
        """Draw the final score to the center of the screen."""
        final_score_str = f"Final Score: {self.stats.score}"
        self.final_score_image = self.font.render(final_score_str, True, self.text_color, self.settings.bg_colour)

        # Center the final score on the screen
        self.final_score_rect = self.final_score_image.get_rect()
        self.final_score_rect.center = self.screen_rect.center
        self.screen.blit(self.final_score_image, self.final_score_rect)
