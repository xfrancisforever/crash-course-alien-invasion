import random
import pygame as pg
from powerup import Powerup

class PowerupManager:
    """Class to manage the powerups."""
    def __init__(self, screen, screen_rect):
        """Initialises the attributes of the class."""
        self.screen = screen
        self.screen_rect = screen_rect

        self.cooldown = 100
        self.cooldown_count = 0

        self.powerups = pg.sprite.Group()

    def generate_powerup(self):
        """Randomly draws the powerup if the cooldown is over."""
#        if random.random() < 0.1:
        self.powerups.add(Powerup(self.screen, self.screen_rect))
        self.cooldown_count = 0

    def get_active_powerups(self):
        """Returns all active powerups."""
        active_powerups = []

        for powerup in self.powerups:
            if powerup.active:
                active_powerups.append(powerup)

        return active_powerups
    
    def update(self):
        """Updates the powerup and clears it if not caught."""
        self.powerups.update()

        for powerup in self.powerups.copy():
            if powerup.rect.top > self.screen_rect.bottom:
                self.powerups.remove(powerup)
                self.cooldown_count = 0

    def draw(self):
        """Draws every powerup."""
        for powerup in self.powerups:
            powerup.draw()

    def update_cooldown(self, dt):
        """Updates the cooldown of the powerups."""
        if not self.powerups:
            self.cooldown_count += dt

    def check_cooldown(self):
        """Checks if the cooldown is over."""
        return self.cooldown_count > self.cooldown
