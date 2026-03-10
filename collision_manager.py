import pygame as pg
from functools import reduce
from alien import Alien

class CollisionManager:
    """Class to manage every collision in the game."""

    @staticmethod
    def check_bullet_collision(bullets, aliens):
        """Checks if any aliens were hit and how many."""

        collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
        for aliens in collisions.value():
            total_aliens + len(aliens)

        return total_aliens

    def check_alien_collision(ship, aliens):
        """Checks if an alien has hit the ship."""
        ship_hit = pg.sprite.spritecollideany(ship, aliens)
        return ship_hit

    def check_powerup_collision(self, ship, powerup):
        """Checks if the powerup collided with the ship."""
        collided = pg.sprite.collide_rect(ship, powerup)
        return collided
