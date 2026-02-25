import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""

        super().__init__()
        
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.colour = self.settings.bullet_colour

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    # Only used by Group.update()
    def update(self):
        """Move the bullet up the screen."""
        if self.rect.bottom < 0:
            self.kill()
            return

        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)
