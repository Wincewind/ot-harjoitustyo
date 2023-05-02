import os
import sys
import pygame
from config import CARD_WIDTH, CARD_HEIGHT
from entities.card import Card
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "..", ".."))


class CardSprite(pygame.sprite.Sprite):
    """Class representing a card sprite.

    Args:
        pygame (sprite.Sprite): Inherits the pygame Sprite class.

    Attributes:
        card: Card object that will determine what the image loaded to the sprite will be.
        rect: pygame.Rect object generated from the card image's surface.
        __img_name: filename of the image.

    """
    CARD_DIMENSIONS = (CARD_WIDTH, CARD_HEIGHT)
    OVERLAY_GREEN = (50, 168, 82, 128)
    OVERLAY_RED = (196, 65, 93, 128)
    OVERLAY_YELLOW = (255, 226, 99, 128)

    def __init__(self, card: Card, x=0, y=0, use_front_img=True):
        super().__init__()
        self.card = card
        if use_front_img:
            self.__img_name = f"{card.set}_{card.suit[0].lower()}{card.value}.png"
        else:
            self.__img_name = f"{self.card.set}_back.png"
        self.load_img()
        self.image = pygame.transform.scale(
            self.image, CardSprite.CARD_DIMENSIONS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_img(self):
        """Load the card's image from assets-directory. 
        """
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets",
                         self.card.set, self.__img_name)
        )
        self.image = pygame.transform.scale(
            self.image, CardSprite.CARD_DIMENSIONS)

    def set_overlay(self, overlay_color=None):
        """Set a overlay to the card sprite.

        Args:
            overlay_color (tuple(int,int,int,int), optional): The RGBA value of the overlay. 
            Defaults to None and no color overlay is set.
        """
        self.load_img()
        if overlay_color is not None:
            overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            overlay.fill(overlay_color)
            self.image.blit(overlay, (0, 0))
