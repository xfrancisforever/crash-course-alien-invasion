import random
import pygame as pg
from pygame.sprite import Sprite

class Powerup(Sprite):
    """Class to represent a powerup for Alien Invasion."""

    Cooldown = 10000
    Limit = 15

    def __init__(self, screen, screen_rect):
        """Initialise the attributes of a powerup."""

        super().__init__()

        self.screen = screen
        self.screen_rect = screen_rect

        self.y = 0
        self.x = 0
        self.sprite_count = 0
        self.rect = None
        self.active = False
        self.bullet_count = 1

        self._load_images() 
        self.reset_rect()

    def draw(self):
        current_sprite = self.images[self.sprite_count // 6]
        self.screen.blit(current_sprite, self.rect)

        if self.sprite_count < 59:
            self.sprite_count += 1
        else:
            self.sprite_count = 0

    def update(self):
        self.y = float(self.y + 1.5)
        self.rect.y = self.y
            
    def reset_rect(self):
        self.x = random.randint(10, self.screen_rect.right - 10)
        self.y = 0

        self.rect = pg.Rect((self.x, self.y), (20, 20))

    def _load_images(self):
        self.images = []

        for i in range(1, 11):
            self.images.append(pg.image.load(f'images/orbs/orb{i}.png'))
