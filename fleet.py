import pygame as pg
from alien import Alien

class Fleet:
    """Manages the alien fleet."""
    def __init__(self, screen, screen_rect):
        """Initialises attributes of the manager."""
        self.screen = screen
        self.screen_rect = screen_rect

        self.direction = 1
        self.drop_speed = 10
        self.speed = None

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

    def update(self):
        """Update alien positions."""
        self._check_fleet_edges()

        for alien in self.aliens:
            alien.x += self.speed * self.direction
            alien.rect.x = alien.x

    def draw(self):
        """Draws the aliens in the fleet."""
        for alien in self.aliens:
            alien.draw()

    def create_alien(self, x, y):
        """Creates a new alien in the specified position."""
        alien = Alien(self.screen, self.screen_rect)
        alien.x = x

        alien.rect.x = x
        alien.rect.y = y

        self.aliens.add(alien)

    def set_difficulty(self, difficulty):
        """Change the fleet stats according to difficulty."""

        match difficulty:
            case 'easy':
                self.speed = 0.3
                Alien.Points = 8
            case 'normal':
                self.speed = 0.4
                Alien.Points = 10
            case 'hard':
                self.speed = 0.5
                Alien.Points = 12

    def is_empty(self):
        """Returns a boolean telling if there are aliens remaining."""
        return bool(self.aliens)

    def check_bottom_reached(self):
        """Checks if any alien has reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.reached_bottom():
                return True

        return False

    def increase_speed(self):
        """Increases the fleet stats."""
        self.speed *= 1.2

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

        self.direction *= -1
