import pygame as pg
from alien import Alien

class Fleet:
    """Manages the alien fleet."""
    DropSpeed = 10
    Direction = 1

    def __init__(self, screen, screen_rect):
        """Initialises attributes of the manager."""
        self.screen = screen_rect
        self.screen_rect = screen_rect

        self.aliens = pg.sprite.Group()

    def generate(self):
        """Create a fleet of aliens."""
        alien = Alien(self.screen, self.screen_rect)
        x, y = Alien.Size

        while y < (self.screen_rect.bottom - (5 * Alien.Size[0])):
            while x < (self.screen_rect.right - (3 * Alien.Size[1])):
                self.create_alien(x, y)
                x += 3 * Alien.Size[0]

            x = Alien.Size[0]
            y += 2 * Alien.Size[1]

    def create_alien(self, x, y):
        """Creates a new alien in the specified position."""
        alien = Alien(self.screen, self.screen_rect)
        alien.x = x

        alien.rect.x = x
        alien.rect.y = y

        self.aliens.add(alien)

    def update(self):
        """Update alien positions."""
        self._check_fleet_edges()
        self.aliens.update(Fleet.Direction)

    def is_empty(self):
        """Returns a boolean telling if there are aliens remaining."""
        return bool(self.aliens)

    def check_bottom_reached(self):
        """Checks if any alien has reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.reached_bottom():
                return True

        return False

    def _check_fleet_edges(self):
        """Checks if the fleet has reached the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Changes the direction the fleet is going."""
        for alien in self.aliens.sprites():
            alien.rect.y += Fleet.DropSpeed

        Flet.Direction *= -1

