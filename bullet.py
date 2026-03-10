import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
    Speed = 2.0
    Cooldown = 500
    Width = 5
    Height = 15
    Colour = (60, 60, 60)

    def __init__(self, screen, initial_pos):
        """Create a bullet object at the ship's current position."""

        super().__init__()
        
        self.screen = screen

        self.rect = pg.Rect(0, 0, Bullet.Width, Bullet.Height)
        self.rect.midtop = initial_pos

        self.y = float(self.rect.y)

    # Only used by Group.update()
    def update(self):
        """Move the bullet up the screen."""

        self.y -= Bullet.Speed
        self.rect.y = self.y

    def draw(self):
        """Draw the bullet to the screen."""
        pg.draw.rect(self.screen, Bullet.Colour, self.rect)

    @staticmethod
    def increase_speed():
        Bullet.Speed *= 1.5

        if Bullet.Cooldown >= 100:
            Bullet.Cooldown -= 25
