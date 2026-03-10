import random
import pygame as pg
from powerup import Powerup

class PowerupManager:
    """Class to manage the powerups."""

    def __init__(self, screen, screen_rect):
        """Initialises the attributes of the class."""
        self.screen = screen
        self.screen_rect = screen_rect

        self.powerups = pg.sprite.Group()
        self.cooldown = 0

    def generate_powerup(self, dt):
        """Randomly draws the powerup if the cooldown is over."""

        if self.powerups:
            return

        if (self.cooldown + dt) > Powerup.Cooldown:
            if random.random() < 0.1:
                self.powerups.add(Powerup())
                self.cooldown = 0
        else:
            self.cooldown += dt

    def get_active_powerups(self):
        """Returns all active powerups."""
        active_powerups = []
        for powerup in self.powerups:
            active_powerups.append(powerup)

        return active_powerups
    
    def update(self):
        """Updates the powerup and clears it if not caught."""
        self.powerups.update()

        for powerup in self.powerups.copy():
            if powerup.rect.top > self.screen_rect.bottom:
                self.powerups.remove(powerup)
                self.cooldown = 0

    def draw(self):
        self.powerups.draw()

