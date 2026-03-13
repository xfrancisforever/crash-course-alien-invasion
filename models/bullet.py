import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
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

    def draw(self):
        """Draw the bullet to the screen."""
        pg.draw.rect(self.screen, Bullet.Colour, self.rect)

