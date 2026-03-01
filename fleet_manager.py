import pygame
from alien import Alien

class FleetManager:
    """Manages the alien fleet."""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.aliens = pygame.sprite.Group()

    def create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self.game)
        alien_width, alien_height = alien.rect.size

        x, y = alien_width, alien_height

        while y < (self.settings.screen_height - (5 * alien_height)):
            while x < (self.settings.screen_width - (3 * alien_width)):
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

    def check_bottom_reached(self):
        """Check if any aliens have reached the bottom."""

        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.settings.screen_height:
                return True

        return False

    def update(self):
        """Update alien positions."""
        self._check_fleet_edges()
        self.aliens.update()

    def draw(self):
        """Draw the fleet."""
        self.aliens.draw(self.screen)

    def empty(self):
        """Clear group of aliens."""
        self.aliens.empty()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

