class Settings:
    def __init__(self):
        """Class to store all settings from the Alien Invasion game."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)

        # Alien settings
        self.fleet_drop_speed = 10
        self.alien_size = (40, 39)
        self.fleet_direction = 1

        # Button settings
        self.button_size = (200, 50)

        # Speed
        self.speedup_scale = 1.15
        self.bullet_cooldown_drop = 20

    def set_difficulty(self, difficulty):
        """Initialise settings that change throughout the game."""

        match difficulty:
            case 'easy':
                self.ship_speed = 2.5
                self.bullet_speed = 2.5
                self.alien_speed = 0.7
                self.bullet_cooldown = 300

            case 'normal':
                self.ship_speed = 1.8
                self.bullet_speed = 2.5
                self.alien_speed = 0.7
                self.bullet_cooldown = 500

            case 'hard':
                self.ship_speed = 1.3
                self.bullet_speed = 1.5
                self.alien_speed = 1.5
                self.bullet_cooldown = 700

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        if self.bullet_cooldown >= 100:
            self.bullet_cooldown -= self.bullet_cooldown_drop
