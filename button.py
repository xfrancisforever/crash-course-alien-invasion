import pygame
from button_styles import ButtonStyles

class Button:
    "A class to build buttons for the game."""

    def __init__(
            self, 
            screen, 
            screen_rect, 
            position, 
            message, 
            styles=ButtonStyles()
    ):
        """Initialise the button attributes."""

        self.screen = screen
        self.screen_rect = screen_rect

        self.styles = styles

        self.rect = pygame.Rect(0, 0, styles.size[0], styles.size[1])
        self.rect.center = position

        self.message_image = None
        self.message_rect = None

        self._prep_message(message)

    def _prep_message(self, message):
        """Turn message into a rendered image and center text on the
           button.
        """

        self.message_image = self.styles.font.render(
            message, 
            True, 
            self.styles.font_colour, 
            self.styles.colour
        )

        self.message_rect = self.message_image.get_rect()
        self.message_rect.center = self.rect.center

    def draw_button(self):
        """Draw a blank button and then draw message."""

        self.screen.fill(self.styles.colour, self.rect)
        self.screen.blit(self.message_image, self.message_rect)
