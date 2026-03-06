import pygame as pg

class CollisionManager:
    """Class to manage collisions in the Alien Invasion game."""

    def __init__(self, game):
        """Initialise attributes of the manager."""

        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        self.scoreboard = game.scoreboard

        self.bullets = game.bullets_manager.bullets
        self.aliens = game.fleet.aliens
        self.ship = game.ship

    def check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""

        collisions = pg.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for alien in collisions.values():
                self.stats.score += (self.settings.alien_points * \
                    len(alien))

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

    def check_alien_collision(self):
        """Check if any aliens have reached the bottom."""

        ship_hit = pg.sprite.spritecollideany(self.ship, self.aliens)
        if ship_hit or self.alien_reached_bottom():
            self.game.lose_life()

    def alien_reached_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.settings.screen_height:
                return True

        return False
