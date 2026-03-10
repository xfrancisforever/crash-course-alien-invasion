import pygame
from buttonStyles import ButtonStyles

pygame.init()

class Button:
    "A class to build buttons for the game."""

    def __init__(self, screen, position, message, style=ButtonStyle()):
        """Initialise the button attributes."""

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.style = style

        self.rect = pygame.Rect(0, 0, style.size[0], style.size[1])
        self.rect.center = position

        self.message_image = None
        self.message_rect = None

        self._prep_message(message)

    def _prep_message(self, message):
        """Turn message into a rendered image and center text on the
           button.
        """

        self.message_image = self.font.render(
            message, 
            True, 
            self.style.font_colour, 
            self.style.colour
        )

        self.message_rect = self.message_image.get_rect()
        self.message_rect.center = self.rect.center

    def draw_button(self):
        """Draw a blank button and then draw message."""

        self.screen.fill(self.style.colour, self.rect)
        self.screen.blit(self.message_image, self.message_rect)
