import random
import pygame as pg
from powerup import Powerup

class PowerupManager:
    """Class to manage the powerups."""

    def __init__(self, game):
        """Initialises the attributes of the class."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.powerup = Powerup(game)

        self.on_screen = False
        self.active = False

        self.cooldown_clock = pg.time.Clock()
        self.cooldown_count = 0
        self.limit_count = 1

    def generate_powerup(self):
        tick = self.cooldown_clock.tick()

        if self.on_screen or self.active:
            return

        if (self.cooldown_count + tick) > Powerup.Cooldown:
            generate = random.choices([True, False], weights=(2, 98), k=2)
            if generate:
                self.powerup.reset_rect()

                self.on_screen = True
                self.cooldown_count = 0
        else:
            self.cooldown_count += tick
    
    def update(self):
        """Updates the powerup and clears it if not caught."""
        self.powerup.update()

        if self.powerup.rect.top > self.screen_rect.bottom:
            self.on_screen = False
            self.cooldown_count = 0

    def draw(self):
        """Draws the powerup on the screen."""
        self.powerup.draw()

    def turn_off(self):
        self.cooldown_count = 0
        self.on_screen = False
        self.active = False
