import pygame

class Settings:
    """Class to store all settings from the Alien Invasion game."""

    def __init__(self):
        """Initialise settings attributes."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

        # Menu settings
        self.score_gap = 20

        # Button settings
        self.button_size = (200, 50)
