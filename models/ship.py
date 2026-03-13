import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    Speed = 1.5
    Image = pygame.image.load('images/ship.bmp')

    def __init__(self, screen, screen_rect):
        """Initialise the ship and set its starting position."""

        super().__init__()

        self.screen = screen
        self.screen_rect = screen_rect

        # Image
        self.rect = Ship.Image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def draw(self):
        """Draw the ship at its current location."""
        self.screen.blit(Ship.Image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag."""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += Ship.Speed
        if self.moving_left and self.rect.left > 0:
            self.x -= Ship.Speed

        self.rect.x = self.x
        
    def center_ship(self):
        """Center the ship on the screen."""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def set_difficulty(self, difficulty):
        """Change the ship stats according to difficulty."""
        match difficulty:
            case 'easy':
                Ship.Speed = 2.0
            case 'normal':
                Ship.Speed = 1.8
            case 'hard':
                Ship.Speed = 1.5

    @staticmethod
    def increase_speed():
        Ship.Speed *= 1.2
