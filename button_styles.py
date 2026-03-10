import pygame as pg
from dataclasses import dataclass

pg.font.init()

@dataclass
class ButtonStyles:
    """Class to store a set of styles for a button."""
    size = (200, 50)
    colour = (0, 135, 0)
    font_colour = (255, 255, 255)
    font = pg.font.SysFont(None, 48)

