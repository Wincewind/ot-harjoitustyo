from config import CARD_WIDTH, CARD_HEIGHT
from entities.card import Card
import os
import sys
import pygame
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "..", ".."))


class CardSprite(pygame.sprite.Sprite):
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
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets",
                         self.card.set, self.__img_name)
        )
        self.image = pygame.transform.scale(
            self.image, CardSprite.CARD_DIMENSIONS)

    def set_overlay(self, overlay_color=None):
        self.load_img()
        if overlay_color is not None:
            overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            overlay.fill(overlay_color)
            self.image.blit(overlay, (0, 0))


# if __name__ == '__main__':
#     crd = Card('minime453', 'Hearts', '13', True)
#     crd_sprite = CardSprite(crd)
#     pygame.init()
#     screen_width = 800
#     screen_height = 600
#     screen = pygame.display.set_mode(crd_sprite.image.get_size())
#     screen.blit(crd_sprite.image, crd_sprite.rect)
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     crd_sprite.set_overlay(CardSprite.OVERLAY_GREEN)
#                 if event.key == pygame.K_DOWN:
#                     crd_sprite.set_overlay(CardSprite.OVERLAY_RED)
#                 if event.key == pygame.K_LEFT:
#                     crd_sprite.set_overlay(CardSprite.OVERLAY_YELLOW)
#                 if event.key == pygame.K_RIGHT:
#                     crd_sprite.set_overlay()
#                 screen.blit(crd_sprite.image, crd_sprite.rect)

#         pygame.display.update()

#     pygame.quit()
