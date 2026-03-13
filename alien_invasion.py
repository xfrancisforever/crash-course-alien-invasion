import pygame
import sys
from game_stats import GameStats
from models.ship import Ship
from models.alien import Alien
from models.powerup import Powerup
from models.bullet import Bullet
from managers.fleet_manager import FleetManager
from managers.bullets_manager import BulletsManager
from managers.powerups_manager import PowerupManager
from managers.collisions_manager import CollisionsManager
from managers.menu_manager import MenuManager
from managers.scoreboard_manager import ScoreboardManager

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    BgColour = (230, 230, 230)

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()

        # Game attributes
        self.game_active = False
        self.difficulty = None
        self.game_stats = GameStats()

        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        # Gameplay objects
        self.ship = Ship(self.screen, self.screen_rect) 
        self.fleet = FleetManager(self.screen, self.screen_rect)

        self.powerups_manager = PowerupManager(
            self.screen, 
            self.screen_rect
        )

        self.bullets_manager = BulletsManager(
            self.screen, 
            self.ship
        )

        # Visual objects
        self.menu = MenuManager(self.screen, self.screen_rect)

        self.scoreboard = ScoreboardManager(
            self.screen, 
            self.screen_rect, 
            self.game_stats,
            AlienInvasion.BgColour
        )

        # Manager groups
        self.bullets = self.bullets_manager.bullets
        self.powerups = self.powerups_manager.powerups
        self.active_powerups = self.powerups_manager.active_powerups
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
            self._call_bullets_fire()
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

        if not self.difficulty:
            self.difficulty = self.menu.check_difficulty_buttons(mouse_pos)
            self._set_difficulty()

        elif not self.game_active:
            clicked = self.menu.check_play_button(mouse_pos)
            if clicked:
                self._start_game()

    def _update_screen(self):
        """Executes all the changes in a frame."""
        self.screen.fill(AlienInvasion.BgColour)
        self.dt = self.clock.tick(60)

        if self.game_active:
            self._update_cooldown()
            self._update_gameplay()

        self._draw_gameplay()
        self._draw_menu()
        self._draw_scoreboard()

        pygame.display.flip()

    def _start_game(self):
        """Start a new game."""
        self.game_active = True

        self.game_stats.reset_stats()
        self._reposition()        

        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
        
        pygame.mouse.set_visible(False)

    def _new_level(self):
        """Increases the difficulty and level of the game."""
        self.game_stats.level += 1

        self._reposition()
        self.scoreboard.prep_level()

        self.fleet.increase_speed()
        self.ship.increase_speed()
        self.bullets_manager.increase_speed()
        print(Alien.Points)

        pygame.time.delay(1000)

    def _lose_life(self):
        """Respond to the ship being hit by an alien."""
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reposition()
        else:
            self.game_active = False
            self.difficulty = None
        
        self.scoreboard.prep_ships()
        pygame.time.delay(1000)

    def _call_aliens_collision(self):
        """Lose a life with any alien collision."""
        alien_collided = CollisionsManager.check_aliens_collision(
            self.ship,
            self.aliens
        )

        if alien_collided:
            self._lose_life()

    def _call_bullets_collision(self):
        """Updates the game score with any bullet collision."""
        collisions = CollisionsManager.check_bullets_collision(
            self.bullets, 
            self.aliens
        )

        new_score = 0

        for alien in collisions.values():
            new_score += len(alien) * Alien.Points

        self.game_stats.update_scores(new_score)

    def _call_powerups_collision(self):
        """Activate a powerup with its collision."""
        collided_powerup = CollisionsManager.check_powerups_collision(
            self.ship,
            self.powerups
        )

        if collided_powerup:
            self.powerups.remove(collided_powerup)
            self.active_powerups.add(collided_powerup)

    def _call_bullets_fire(self):
        """Calls the bullet trigger with powerups."""
        if self.bullets_manager.check_cooldown(self.dt):
            if self.active_powerups:
                for powerup in self.active_powerups:
                    self.bullets_manager.powered_fire()
                    powerup.progress_state()
                    break
            else:
                self.bullets_manager.fire()

    def _call_generate_powerups(self):
        """Checks the cooldown before trying to generate a powerup."""
        if self.powerups_manager.check_cooldown():
            self.powerups_manager.generate_powerup()
                
    def _update_gameplay(self):
        """Updates the gameplay elements."""
        self.ship.update()
        self.fleet.update()
        self.bullets_manager.update()
        self.powerups_manager.update()
        self._call_generate_powerups()

        self._call_bullets_collision()
        self._call_aliens_collision()
        self._call_powerups_collision()

        self.fleet.check_bottom_reached()

        if not self.aliens:
            self._new_level()

    def _update_cooldown(self):
        """Updates the cooldown of the elements."""
        self.bullets_manager.update_cooldown(self.dt)
        self.powerups_manager.update_cooldown(self.dt)

    def _reposition(self):
        """Repositions elements for a new round."""
        self.bullets.empty()
        self.aliens.empty()
        self.powerups.empty()
        self.active_powerups.empty()

        self.fleet.generate()
        self.ship.center_ship()

    def _draw_gameplay(self):
        """Draws the gameplay elements."""
        self.ship.draw()
        self.fleet.draw()
        self.bullets_manager.draw()
        self.powerups_manager.draw()

    def _draw_menu(self):
        """Draws menu according to status."""
        if not self.difficulty:
            self.menu.draw_difficulty_menu()
        elif not self.game_active:
            self.menu.draw_play_button()
        else:
            pygame.mouse.set_visible(True)

    def _draw_scoreboard(self):
        """Updates scoreboard's contents and draws them."""
        self.scoreboard.prep_score()
        self.scoreboard.prep_high_score()
        self.scoreboard.prep_level()

        self.scoreboard.draw()

    def _set_difficulty(self):
        """Changes the game elements to adapt to the difficulty."""
        self.fleet.set_difficulty(self.difficulty)
        self.ship.set_difficulty(self.difficulty)
        self.bullets_manager.set_difficulty(self.difficulty)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
