import random
import pygame as pg
from models.powerup import Powerup

class PowerupManager:
    """Class to manage the powerups."""
    def __init__(self, screen, screen_rect):
        """Initialises the attributes of the class."""
        self.screen = screen
        self.screen_rect = screen_rect

        self.cooldown = 15000
        self.cooldown_count = 0

        self.powerups = pg.sprite.Group()
        self.active_powerups = pg.sprite.Group()

    def generate_powerup(self):
        """Randomly draws the powerup if the cooldown is over."""
        if random.random() < 0.05:
            self.powerups.add(Powerup(self.screen, self.screen_rect))
            self.cooldown_count = 0

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
        cooldown_over = self.cooldown_count > self.cooldown
        powerup_on_screen = bool(self.powerups)

        return cooldown_over and not powerup_on_screen
