import pygame as pg
from alien import Alien

class CollisionManager:
    """Class to manage every collision in the game."""

    def __init__(self, game):
        """Initialises all attributes of the class."""

        self.game = game
        self.stats = game.stats
        self.scoreboard = game.scoreboard

        self.aliens = game.fleet.aliens
        self.ship = game.ship
        self.bullets_manager = game.bullets_manager
        self.powerup_manager = game.powerup_manager

    def check_bullet_collision(self):
        """Checks if a bullet collided with an alien."""

        collisions = pg.sprite.groupcollide(
            self.bullets_manager.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += len(aliens) * Alien.Points

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

    def check_alien_collision(self):
        """Checks if an alien has hit the ship."""

        ship_hit = pg.sprite.spritecollideany(self.ship, self.aliens)
        if ship_hit: 
            self.game.lose_life()

    def check_powerup_collision(self):
        collided = pg.sprite.collide_rect(
            self.ship, self.powerup_manager.powerup
        )
                 
        if collided:
            self.powerup_manager.active = True
            self.powerup_manager.on_screen = False
