from ship import Ship
from alien import Alien
from settings import Settings
from bullet import Bullet
from game_stats import GameStats
import pygame
import sys
from time import sleep

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()

        self.bullet_cooldown_count = -1
        self.game_active = True

        self.settings = Settings()

        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height), pygame.SHOWN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.fps_clock = pygame.time.Clock()
        self.bullet_clock = pygame.time.Clock()

        self.ship = Ship(self) 
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)

        self._create_fleet()

        pygame.display.set_caption("Alien Invasion")
        

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()

            self._update_screen()
            self.fps_clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        """Repopulate the screen with updated elements."""

        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        for b in self.bullets.sprites():
            b.draw_bullet()

        pygame.display.flip()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""

        new_tick = self.bullet_clock.tick()

        if new_tick + self.bullet_cooldown_count >= \
                self.settings.bullet_cooldown or \
                self.bullet_cooldown_count == -1: 
            self.bullets.add(Bullet(self))
            self.bullet_cooldown_count = 0
        else:
            self.bullet_cooldown_count += new_tick

    def _update_bullets(self):
        self.bullets.update()
        self._check_bullet_alien_collisions()

        for b in self.bullets:
            if b.rect.bottom <= 0:
                self.bullets.remove(b)

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
            True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _lose_life(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""

        for a in self.aliens.sprites():
            if a.rect.bottom >= self.settings.screen_height:
                self._lose_life()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 5  * 
            alien_height):
            while current_x < (self.settings.screen_width - 3 * 
                alien_width):
                self._create_alien(current_x, current_y)
                current_x += 3 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        
        for a in self.aliens.sprites():
            a.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""

        new_alien = Alien(self)

        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position

        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._lose_life()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached the edge."""

        for a in self.aliens.sprites():
            if a.check_edges():
                self._change_fleet_direction()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
