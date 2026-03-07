from button import Button

class Menu:
    """Manage game menus and UI"""

    def __init__(self, game):
        """Initialise the game menu."""

        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self._create_play_button()
        self._create_difficulty_buttons()

    def _create_play_button(self):
        """Creates the play button object."""

        self.play_button = Button(
            self, 
            self.settings.button_size, 
            self.screen_rect.center, 
            "Play"
        )

    def _create_difficulty_buttons(self):
        """Creates the difficulty button objects."""

        screen_center = self.screen_rect.center
        space_between = self.settings.button_size[0] * 1.25
            
        self.difficulty_buttons = {
            'easy': Button(self, self.settings.button_size, 
                          (screen_center[0] - space_between, 
                          screen_center[1]), 'Easy'),
            'normal': Button(self, self.settings.button_size,
                            (screen_center[0], screen_center[1]),
                            'Normal'),
            'hard': Button(self, self.settings.button_size,
                          (screen_center[0] + space_between,
                          screen_center[1]), 'Hard')
        }

    def draw_difficulty_menu(self):
        """Draws the difficulty buttons on the screen."""

        for button in self.difficulty_buttons.values():
            button.draw_button()

    def draw_play_button(self):
        """Draws the play button on the game screen."""

        self.play_button.draw_button()

    def check_difficulty_buttons(self, mouse_pos):
        for difficulty, button in self.difficulty_buttons.items():
            collided = button.rect.collidepoint(mouse_pos)

            if collided:
                self.game.difficulty_selected = True
                return

        return None

    def check_play_button(self, mouse_pos):
        collided = self.play_button.rect.collidepoint(mouse_pos)

        if collided:
            self.game.start_game()
        else:
            return None

