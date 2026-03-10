import pygame as pg
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    Points = 10
    Speed = 0.8
    Size = (40, 39)
    Image = pg.image.load('images/alien.bmp')

    def __init__(self, screen, screen_rect):
        """Initialise the alien and set its starting position."""

        super().__init__()

        self.screen = screen
        self.screen_rect = screen_rect

        self.image = pg.transform.scale(Alien.Image, Alien.Size)
        self.rect = Alien.Image.get_rect()
        self.rect.size = Alien.Size

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self, direction):
        """
        Move the alien sideways.
        
        Args: 
            direction: -1 or 1 to express left or right
        """

        self.x += Alien.Speed * direction 
        self.rect.x = self.x


    def check_edges(self):
        """Return boolean representing if the alien has hit the edge."""

        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or \
            (self.rect.left <= 0)

    def reached_bottom(self):
        """Checks if the alien has reached the bottom of the screen."""
        return self.rect.bottom > self.screen_rect.bottom

    @staticmethod
    def increase_difficulty():
        Alien.Speed *= 1.5
        Alien.Points += 1
