import pygame as pg
from bullet import Bullet
from powerup import Powerup

class BulletsManager:
    """Class to manage bullets in an alien invasion game."""

    def __init__(self, game, powerup_manager):
        """Initialise the attributes of the bullet manager."""
        
        self.game = game
        self.screen = game.screen
        self.ship = game.ship
        self.settings = game.settings
        self.scoreboard = game.scoreboard
        self.stats = game.stats
        self.powerup_manager = powerup_manager

        self.aliens = game.fleet.aliens
        self.bullets = pg.sprite.Group()

        self.cooldown_clock = pg.time.Clock()
        self.cooldown_count = -1
        self.powerup_count = 0

    def trigger(self):
        """Create a new bullet and add it to the bullets group."""
        
        if self._check_cooldown():
            if self.powerup_manager.active:
                self.powered_fire()
            else:
                self.fire()

    def fire(self):
        """Shoots a single bullet from the game's ship."""
        self.bullets.add(Bullet(self.game))

    def powered_fire(self):
        """Shoots triple bullets."""

        for n in range(-1, 2):
            ship_midtop = self.ship.rect.midtop
            offset = ship_midtop[0] + ((Bullet.Width + 10) * n)
            midtop = (offset, ship_midtop[1])

            self.bullets.add(Bullet(self.game, initial_midtop=midtop))

        if self.powerup_manager.limit_count < Powerup.Limit:
            self.powerup_manager.limit_count += 1
        else:
            self.powerup_manager.active = False
            self.powerup_manager.limit_count = 1

    def update(self):
        """Update bullet positions."""
        
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def draw(self):
        for b in self.bullets.sprites():
            b.draw_bullet()

    def empty(self):
        """Clears all bullets."""
        self.bullets.empty()

    def _check_cooldown(self):
        tick = self.cooldown_clock.tick()

        cooldown_done = tick + self.cooldown_count >= Bullet.Cooldown
        initial_fire = self.cooldown_count == -1

        if cooldown_done or initial_fire:
            self.cooldown_count = 0
            return True
        else:
            self.cooldown_count += tick
            return False

