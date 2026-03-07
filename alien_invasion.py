# TODO 2: Power-ups

import pygame
import sys
from ship import Ship
from alien import Alien
from powerup import Powerup
from bullet import Bullet
from fleet_manager import FleetManager
from bullets_manager import BulletsManager
from powerup_manager import PowerupManager
from collision_manager import CollisionManager
from settings import Settings
from game_stats import GameStats
from menu import Menu
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()

        # Game status
        self.game_active = False
        self.difficulty_selected = False

        self.stats = GameStats(self)

        # Clocks
        self.fps_clock = pygame.time.Clock()

        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Settings
        self.settings = Settings()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Related classes
        self.ship = Ship(self) 
        self.menu = Menu(self)
        self.scoreboard = Scoreboard(self)

        self.fleet = FleetManager(self)
        self.powerup_manager = PowerupManager(self)
        self.bullets_manager = BulletsManager(self, self.powerup_manager)
        self.collisions = CollisionManager(self)

        pygame.display.set_caption("Alien Invasion")

        self.fleet.create_fleet()
        self.ship.center_ship()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()
            self.fps_clock.tick(60)

    def start_game(self):
        """Start a new game."""

        self.game_active = True

        self.stats.reset_stats()
        self._reposition_elements()        

        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
        
        pygame.mouse.set_visible(False)

    def lose_life(self):
        """Respond to the ship being hit by an alien."""
        
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self._reposition_elements()
        else:
            self.game_active = False
            self.difficulty_selected = False
        
        self.scoreboard.prep_ships()
        pygame.time.delay(1000)

    def _update_screen(self):
        """Repopulate the screen with updated elements."""

        self.screen.fill(self.settings.bg_colour)

        if self.game_active:
            self._update_gameplay_elements()

        self._draw_initial_elements()

        
        self._draw_menu()
        self.scoreboard.draw()

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
            self.bullets_manager.trigger()
        elif event.key == pygame.K_q:
            sys.exit()

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
            self.menu.check_difficulty_buttons(mouse_pos)
        elif not self.game_active:
            self.menu.check_play_button(mouse_pos)

    def _draw_menu(self):
        if not self.difficulty_selected:
            self.menu.draw_difficulty_menu()
        elif not self.game_active:
            self.menu.draw_play_button()
        else:
            pygame.mouse.set_visible(True)

    def _update_gameplay_elements(self):
        """Updates the gameplay elements of the game."""
        self.ship.update()
        self.fleet.update()
        self.bullets_manager.update()

        self.collisions.check_alien_collision()
        self.fleet.check_bottom_reached()
        self.collisions.check_bullet_collision()

        self._execute_powerup_actions()

        if not self.fleet.aliens:
            self._new_level()

    def _draw_initial_elements(self):
        self.ship.draw()
        self.fleet.draw()
        self.bullets_manager.draw()

    def _execute_powerup_actions(self):
        self.powerup_manager.generate_powerup() 

        if self.powerup_manager.on_screen:
            self.powerup_manager.update()
            self.powerup_manager.draw()
            self.collisions.check_powerup_collision()

    def _reposition_elements(self):
        """Repositions elements for a new round."""

        self.bullets_manager.empty()
        self.fleet.empty()

        self.fleet.create_fleet()
        self.ship.center_ship()

    def _new_level(self):
        self.stats.level += 1

        self.bullets_manager.empty()
        self.fleet.create_fleet()
        self.powerup_manager.turn_off()

        Ship.increase_speed()
        Alien.increase_difficulty()
        Bullet.increase_speed()

        self.scoreboard.prep_level()

        pygame.time.delay(1000)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
