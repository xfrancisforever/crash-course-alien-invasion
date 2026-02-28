import pygame

pygame.init()

class Button:
    "A class to build buttons for the game."""

    def __init__(self, ai_game, size, position, message):
        """Initialise the button attributes."""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.button_colour = (0, 135, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = position

        self._prep_message(message)

    def _prep_message(self, message):
        """Turn message into a rendered image and center text on the
           button.
        """

        self.message_image = self.font.render(message, True, 
            self.text_colour, self.button_colour)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw a blank button and then draw message."""

        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
