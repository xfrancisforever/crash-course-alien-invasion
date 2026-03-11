import pygame as pg
from bullet import Bullet
from powerup import Powerup

class BulletsManager:
    """Class to manage bullets in an alien invasion game."""
    def __init__(self, screen, ship, powerup):
        """Initialise the attributes of the bullet manager."""
        # Dependencies
        self.screen = screen
        self.ship = ship

        self.cooldown = None
        self.speed = None

        # Bullets
        self.bullets = pg.sprite.Group()

        # Settings
        self.cooldown_clock = pg.time.Clock()
        self.cooldown_count = -1

    def trigger(self, powerups=None):
        """Create a new bullet and add it to the bullets group."""
        if self._check_cooldown():
            if powerups:
                self._powered_fire()
            else:
                self._fire()

    def update(self):
        """Update bullet positions."""
        for bullet in self.bullets:
            bullet.y -= self.speed
            bullet.rect.y -= self.speed

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def draw(self):
        """Draws all bullets."""
        for bullet in self.bullets:
            bullet.draw()

    def fire(self):
        """Shoots a single bullet from the game's ship."""
        self.bullets.add(
            Bullet(
                self.screen, 
                self.ship.rect.midtop
            )
        )

    def powered_fire(self):
        """Shoots triple bullets."""
        for n in range(-1, 2):
            ship_top = self.ship.rect.midtop
            offset = ship_top[0] + ((Bullet.Width + 10) * n)

            self.bullets.add(
                Bullet(
                    self.screen, 
                    (offset, ship_top[1])
                )
            )

    def check_cooldown(self, dt):
        """Returns a boolean telling if  the cooldown is over."""
        cooldown_over = self.cooldown_count >= self.cooldown
        initial_fire = self.cooldown_count == -1

        if cooldown_over or initial_fire:
            self.cooldown_count = 0
            return True
        else:
            self.cooldown_count += dt
            return False

    def increase_speed(self):
        """Increases the bullets speed."""
        self.speed *= 1.2
        
        if self.cooldown > 100:
            self.cooldown -= 25

    def update_cooldown(self, dt):
        """Updates the bullets cooldown."""
        self.cooldown_count += dt

    def set_difficulty(self, difficulty):
        """Set the bullets attributes according to difficulty."""
        match difficulty:
            case 'easy':
                self.cooldown = 300
                self.speed = 2.0
            case 'normal':
                self.cooldown = 400
                self.speed = 1.7
            case 'hard':
                self.cooldown = 500
                self.speed = 1.4
