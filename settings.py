
class Settings:
    """A class to contain settings for the  game"""

    def __init__(self):
        self.screen_width = 1400
        self.screen_height = 1000
        self.bg_colour = (0, 150, 50)

        self.plane_speed = 5.0

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 6
        self.bullet_colour = (60, 60, 60)
        self.bullet_speed = 15
        self.bullets_allowed = 10

        #Enemy settings
        self.enemy_speed = 2.0

