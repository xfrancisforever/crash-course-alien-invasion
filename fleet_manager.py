import pygame as pg
from alien import Alien

class FleetManager:
    """Manages the alien fleet."""

    def __init__(self, game):
        """Initialises attributes of the manager."""

        self.drop_speed = 10
        self.fleet_direction = 1

        self.game = game
        self.stats = game.stats
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.ship = game.ship

        self.aliens = pg.sprite.Group()

    def create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self.game)
        alien_width, alien_height = alien.rect.size

        x, y = alien_width, alien_height

        while y < (self.screen_rect.bottom - (5 * alien_height)):
            while x < (self.screen_rect.right - (3 * alien_width)):
                self.create_alien(x, y)
                x += 3 * alien_width

            x = alien_width
            y += 2 * alien_height

    def create_alien(self, x, y):
        """Creates a new alien in the specified position."""

        alien = Alien(self.game)
        alien.x = x

        alien.rect.x = x
        alien.rect.y = y

        self.aliens.add(alien)

    def update(self):
        """Update alien positions."""
        self._check_fleet_edges()
        self.aliens.update(self.fleet_direction)

    def draw(self):
        """Draw the fleet."""
        self.aliens.draw(self.screen)

    def empty(self):
        """Clear group of aliens."""
        self.aliens.empty()

    def check_bottom_reached(self):
        """Checks if any alien has reached the bottom of the screen."""

        for alien in self.aliens.sprites():
            if alien.reached_bottom():
                self.game.lose_life()
                return

    def _check_fleet_edges(self):
        """Checks if the fleet has reached the edge of the screen."""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Changes the direction the fleet is going."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.drop_speed

        self.fleet_direction *= -1

