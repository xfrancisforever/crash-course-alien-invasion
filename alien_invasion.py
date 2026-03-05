import pygame
import sys
from ship import Ship
from alien import Alien
from bullet import Bullet
from fleet_manager import FleetManager
from settings import Settings
from game_stats import GameStats
from menu import Menu
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()

        # Game stats
        self.bullet_cooldown_count = -1
        self.game_active = False
        self.difficulty_selected = False

        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Settings
        self.settings = Settings()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Related classes
        self.ship = Ship(self) 
        self.fleet = FleetManager(self)
        self.menu = Menu(self)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Sprite groups
        self.bullets = pygame.sprite.Group()

        # Clocks
        self.fps_clock = pygame.time.Clock()
        self.bullet_clock = pygame.time.Clock()
        self.fleet.create_fleet()
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_fleet()
                self._update_bullets()

            self._update_screen()
            self.fps_clock.tick(60)

    def _update_screen(self):
        """Repopulate the screen with updated elements."""

        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        self.fleet.draw()
        self.scoreboard.draw()
        
        for b in self.bullets.sprites():
            b.draw_bullet()

        if not self.difficulty_selected:
            self.menu.draw_difficulty_menu()
        elif not self.game_active:
            self.menu.draw_play_button()
        else:
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        """Handle all events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

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
        elif event.key == pygame.K_p and self.difficulty_selected and \
                not self.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _handle_mouse_click(self):
        """Handle mouse clicks."""

        mouse_pos = pygame.mouse.get_pos()

        if not self.difficulty_selected:
            difficulty = self.menu.check_difficulty_buttons(mouse_pos)

            if difficulty:
                self.settings.set_difficulty(difficulty)
                self.difficulty_selected = True

        elif not self.game_active:
            pressed = self.menu.check_play_button(mouse_pos)
            if pressed:
                self._start_game()

    def _start_game(self):
        """Start a new game."""

        self.game_active = True
        self.stats.reset_stats()

        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        
        self.bullets.empty()
        self.fleet.empty()

        self.fleet.create_fleet()
        self.ship.center_ship()
        
        pygame.mouse.set_visible(False)

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
        """Update bullet positions and check for collisions."""

        self.bullets.update()
        self._check_bullet_alien_collisions()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.fleet.aliens, True, True
        )

        if collisions:
            for alien in collisions.values():
                self.stats.score += (self.settings.alien_points * \
                    len(alien))

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.fleet.aliens:
            self.bullets.empty()
            self.fleet.create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.scoreboard.prep_level()

            pygame.time.delay(1000)

    def _update_fleet(self):
        """Updates the fleet and checks if it killed the player."""

        self.fleet.update()

        bottom_reached = self.fleet.check_bottom_reached()
        ship_hit = pygame.sprite.spritecollideany(
                self.ship, self.fleet.aliens
        )

        if bottom_reached or ship_hit:
            self._lose_life()


    def _lose_life(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.fleet.empty()

            self.fleet.create_fleet()
            self.ship.center_ship()

            pygame.time.delay(1000)
        else:
            self.game_active = False
            self.difficulty_selected = False

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
