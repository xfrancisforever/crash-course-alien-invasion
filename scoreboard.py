class Scoreboard:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """Turn the score into a rendered image."""
            
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'
        self.score_image = self.settings.score_font.render(
            score_str,
            True,
            self.settings.score_text_colour,
            self.settings.bg_colour
        )

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - \
            self.settings.score_gap
        self.score_rect.top = self.settings.score_gap

    def prep_high_score(self):
        """Turn the high score into a rendered image."""

        high_score = round(self.stats.high_score, -1)
        high_score_str = f'{high_score:,}'

        self.high_score_image = self.settings.score_font.render(
            high_score_str,
            True,
            self.settings.score_text_colour,
            self.settings.bg_colour
        )

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.settings.score_gap

    def prep_level(self):
        """Turn the level into a rendered image."""

        level_str = str(self.stats.level)
        self.level_image = self.settings.score_font.render(
            level_str,
            True,
            self.settings.score_text_colour,
            self.settings.bg_colour
        )

        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.settings.score_gap
        self.level_rect.top = self.settings.score_gap

    def draw(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def check_high_score(self):
        """Check to see if there's a new high score."""

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
