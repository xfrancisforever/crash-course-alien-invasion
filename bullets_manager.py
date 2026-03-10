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
        self.powerup = powerup

        # Bullets
        self.bullets = pg.sprite.Group()

        # Settings
        self.cooldown_clock = pg.time.Clock()
        self.cooldown_count = -1

    def trigger(self):
        """Create a new bullet and add it to the bullets group."""
        
        if self._check_cooldown():
            if self.powerup.active:
                self.powered_fire()
            else:
                self.fire()

    def fire(self):
        """Shoots a single bullet from the game's ship."""
        self.bullets.add(
            Bullet(
                self.screen, 
                position=self.ship.rect.midtop
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
                    position=(offset, ship_top[1]
                )
            )

        if self.powerup.bullet_count < Powerup.Limit:
            self.powerup.bullet_count += 1
        else:
            self.powerup.active = False
            self.powerup.bullet_count = 1

    def update(self):
        """Update bullet positions."""
        
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def draw(self):
        """Draws all bullets."""

        for b in self.bullets.sprites():
            b.draw_bullet()

    def empty(self):
        """Clears all bullets."""
        self.bullets.empty()

    def _check_cooldown(self):
        """Returns a boolean telling if  the cooldown is over."""

        tick = self.cooldown_clock.tick()

        cooldown_done = tick + self.cooldown_count >= Bullet.Cooldown
        initial_fire = self.cooldown_count == -1

        if cooldown_done or initial_fire:
            self.cooldown_count = 0
            return True
        else:
            self.cooldown_count += tick
            return False

