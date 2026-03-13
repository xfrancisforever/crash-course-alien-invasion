from models.button import Button

class MenuManager:
    """Manage game menus and UI"""

    ButtonSize = (200, 50)

    def __init__(self, screen, screen_rect):
        """Initialise the game menu."""

        self.screen = screen
        self.screen_rect = screen_rect

        self._create_play_button()
        self._create_difficulty_buttons()

    def _create_play_button(self):
        """Creates the play button object."""

        self.play_button = Button(
            self.screen, 
            MenuManager.ButtonSize,
            self.screen_rect.center, 
            "Play"
        )

    def _create_difficulty_buttons(self):
        """Creates the difficulty button objects."""

        screen_center = self.screen_rect.center
        space_between = MenuManager.ButtonSize[0] * 1.25
            
        self.difficulty_buttons = {
            'easy': Button(
                self.screen, 
                MenuManager.ButtonSize, 
                (screen_center[0] - space_between, 
                screen_center[1]), 
                'Easy'
            ),
            'normal': Button(
                self.screen, 
                MenuManager.ButtonSize,
                (screen_center[0], 
                screen_center[1]),
                'Normal'
            ),
            'hard': Button(
                self.screen, 
                MenuManager.ButtonSize,
                (screen_center[0] + space_between,
                screen_center[1]), 
                'Hard'
            )
        }

    def draw_difficulty_menu(self):
        """Draws the difficulty buttons on the screen."""

        for button in self.difficulty_buttons.values():
            button.draw_button()

    def draw_play_button(self):
        """Draws the play button on the game screen."""
        self.play_button.draw_button()

    def check_difficulty_buttons(self, mouse_pos):
        """Checks if any difficulty button was pressed."""

        for difficulty, button in self.difficulty_buttons.items():
            collided = button.rect.collidepoint(mouse_pos)

            if collided:
                return difficulty

        return None

    def check_play_button(self, mouse_pos):
        """Checks if the play button was pressed."""

        collided = self.play_button.rect.collidepoint(mouse_pos)
        return collided
