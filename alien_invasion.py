import pygame
import sys
from ship import Ship
from alien import Alien
from powerup import Powerup
from bullet import Bullet
from fleet import Fleet
from bullets_manager import BulletsManager
from powerups_manager import PowerupManager
from collisions_manager import CollisionsManager
from game_stats import GameStats
from menu import Menu
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    BgColour = (230, 230, 230)

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()

        # Game status
        self.game_active = False
        self.difficulty_selected = False

        self.game_stats = GameStats()

        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        # Related classes
        self.ship = Ship(self.screen, self.screen_rect) 
        self.fleet = Fleet(self.screen, self.screen_rect)

        self.menu = Menu(self.screen, self.screen_rect)

        self.scoreboard = Scoreboard(
            self.screen, 
            self.screen_rect, 
            self.game_stats,
            AlienInvasion.BgColour
        )

        self.powerups_manager = PowerupManager(
            self.screen, 
            self.screen_rect
        )
        self.bullets_manager = BulletsManager(
            self.screen, 
            self.ship, 
            self.powerups_manager
        )

        self.bullets = self.bullets_manager.bullets
        self.powerups = self.powerups_manager.powerups
        self.aliens = self.fleet.aliens

        # Clocks
        self.clock = pygame.time.Clock()
        self.dt = None

        self.fleet.generate()
        self.ship.center_ship()

        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

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
            self._call_bullet_trigger()
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

    def _update_screen(self):
        """Executes all the changes in a frame."""
        self.screen.fill(AlienInvasion.BgColour)
        self.dt = self.clock.tick()

        if self.game_active:
            self._update_gameplay()
            self._check_collisions()

        self._draw_gameplay()
        self._draw_menu()
        self.scoreboard.draw()

        pygame.display.flip()

    def _start_game(self):
        """Start a new game."""
        self.game_active = True

        self.stats.reset_stats()
        self._reposition_elements()        

        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
        
        pygame.mouse.set_visible(False)

    def _new_level(self):
        """Increases the difficulty and level of the game."""
        self.stats.level += 1

        self._reposition()
        self.scoreboard.prep_level()

        Ship.increase_speed()
        Alien.increase_difficulty()
        Bullet.increase_speed()

        pygame.time.delay(1000)

    def _lose_life(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self._reposition_elements()
        else:
            self.game_active = False
            self.difficulty_selected = False
        
        self.scoreboard.prep_ships()
        pygame.time.delay(1000)

    def _call_bullets_collision(self):
        """Updates the game score with any bullet collision."""
        collisions = CollisionsManager.check_bullets_collision(
            self.bullets, 
            self.aliens
        )

        for alien in collisions.values():
            self.game_stats.score += len(alien) * 10

    def _update_gameplay(self):
        """Updates the gameplay elements."""
        self.ship.update()
        self.fleet.update()
        self.bullets_manager.update()
        self.powerups_manager.update()

        self._call_bullets_collision()
        self._call_aliens_collision()
        self._call_powerups_collision()

        self.fleet.check_bottom_reached()

        if fleet.is_empty():
            self._new_level()

    def _call_alien_collision(self):
        """Lose a life with any alien collision."""
        alien_collided = CollisionsManager.check_alien_collision(
            self.ship,
            self.aliens
        )

        if alien_collided:
            self._lose_life()


    def _call_powerups_collision(self):
        """Activate a powerup with its collision."""
        powerup_collided = CollisionsManager.check_powerups_collision(
            self.ship,
            self.powerups
        )

        if powerup_collided:
            powerup_collided.active = True

    def _call_bullets_trigger(self):
        """Calls the bullet trigger with powerups."""
        powerups = self.powerups_manager.get_active_powerups()
        if self.bullets_manager.check_cooldown(self.dt):
            if powerups:
                for powerup in powerups:
                    self.bullets_manager.powered_fire()
                    powerup.progress_state()
            else:
                self.bullets_manager.fire()


    def _reposition(self):
        """Repositions elements for a new round."""
        self.bullets.clear()
        self.aliens.clear()
        self.powerups.clear()

        self.fleet.create_fleet()
        self.ship.center_ship()

    def _draw_gameplay(self):
        """Draws the gameplay elements."""
        self.ship.draw()
        self.aliens.draw(self.screen)
        self.bullets.draw(self.screen)
        self.powerups.draw(self.screen)

    def _draw_menu(self):
        """Draws menu according to status."""
        if not self.difficulty_selected:
            self.menu.draw_difficulty_menu()
        elif not self.game_active:
            self.menu.draw_play_button()
        else:
            pygame.mouse.set_visible(True)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
