import pygame as pg
from models.ship import Ship

SCREEN_GAP = 20
PADDING = 10

class ScoreboardManager:
    """Class to display the player stats while the game is running."""

    TextColour = (30, 30, 30)
    Font = pg.font.SysFont(None, 48)

    def __init__(self, screen, screen_rect, game_stats, bg_colour):
        """Initialise scoreboard attributes."""

        self.screen = screen
        self.screen_rect = screen_rect
        self.bg_colour = bg_colour

        self.game_stats = game_stats

        self.score_image = None
        self.high_score_image = None
        self.level_image = None
        self.ships = []

        self.score_rect = None
        self.high_score_rect = None
        self.level_rect = None

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.game_stats.score, -1)
        score_str = f'{rounded_score:,}'

        self.score_image = ScoreboardManager.Font.render(
            score_str,
            True,
            ScoreboardManager.TextColour,
            self.bg_colour
        )

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - SCREEN_GAP
        self.score_rect.top = SCREEN_GAP

    def prep_high_score(self):
        """Turn the high score into a rendered image."""

        high_score = round(self.game_stats.high_score, -1)
        high_score_str = f'{high_score:,}'

        self.high_score_image = ScoreboardManager.Font.render(
            high_score_str,
            True,
            ScoreboardManager.TextColour,
            self.bg_colour
        )

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = SCREEN_GAP 

    def prep_level(self):
        """Turn the level into a rendered image."""

        level_str = str(self.game_stats.level)
        self.level_image = ScoreboardManager.Font.render(
            level_str,
            True,
            ScoreboardManager.TextColour,
            self.bg_colour
        )

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - SCREEN_GAP
        self.level_rect.top = self.score_rect.bottom + \
                PADDING

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = []

        for n in range(self.game_stats.ships_left):
            rect = Ship.Image.get_rect()
            rect.x = PADDING + (n * rect.width)
            rect.y = SCREEN_GAP
            
            self.ships.append(rect)

    def draw(self):
        """Draw stats to the screen."""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        for ship in self.ships:
            self.screen.blit(Ship.Image, ship)

    def check_high_score(self):
        """Check to see if there's a new high score."""

        if self.game_stats.score > self.game_stats.high_score:
            self.game_stats.high_score = self.game_stats.score
            self.prep_high_score()
