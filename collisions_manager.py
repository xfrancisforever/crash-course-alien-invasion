import pygame as pg
from functools import reduce
from alien import Alien

class CollisionsManager:
    """Class to manage every collision in the game."""

    @staticmethod
    def check_bullets_collision(bullets, aliens):
        """Checks collisions between bulletsa and aliens."""
        collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
        return collisions

    @staticmethod
    def check_aliens_collision(ship, aliens):
        """Checks collisions between aliens and the ship."""
        collisions = pg.sprite.spritecollideany(ship, aliens)
        return collisions

    @staticmethod
    def check_powerups_collision(ship, powerups):
        """Checks collisions between powerups and the ship."""
        collisions = pg.sprite.spritecollideany(ship, powerups)
        return collisions
