import pygame as pg
from bullet import Bullet

class BulletsManager:
    """Class to manage bullets in an alien invasion game."""

    def __init__(self, game):
        """Initialise the attributes of the bullet manager."""
        
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.bullets = pg.sprite.Group()

        self.cooldown_clock = pg.time.Clock()
        self.cooldown_count = -1

    def fire(self):
        """Create a new bullet and add it to the bullets group."""

        tick = self.cooldown_clock.tick()

        if tick + self.cooldown_count >= \
                self.settings.bullet_cooldown or \
                self.cooldown_count == -1:
            self.bullets.add(Bullet(self.game))
            self.cooldown_count = 0
        else:
            self.cooldown_count += tick

    def update(self):
        """Update bullet positions."""
        
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def draw(self):
        for b in self.bullets.sprites():
            b.draw_bullet()

    def empty(self):
        """Clears all bullets."""
        self.bullets.empty()
