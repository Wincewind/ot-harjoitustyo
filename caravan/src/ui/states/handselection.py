import pygame
from sprites.card import CardSprite
from states.caravanplacement import CaravanPlacement

class HandSelection():
    def __init__(self,gameboard) -> None:
        self.board = gameboard
        self._player_selection = 0
        self._initialize_player_hand_sprites()
        self.player_hand_sprites.draw(self.board.display)
    
    def _initialize_player_hand_sprites(self):
        self.player_hand_sprites = pygame.sprite.Group()
        x = self.board.WIDTH // 3 - 50
        y = self.board.HEIGHT - CardSprite.CARD_DIMENSIONS[1] - 20
        for idx, crd in enumerate(self.board.player.hand):
            spr = CardSprite(crd,x,y)
            spr.set_overlay()
            if idx == self._player_selection:
                spr.set_overlay(CardSprite.OVERLAY_YELLOW)
            self.player_hand_sprites.add(spr)
            x += CardSprite.CARD_DIMENSIONS[0] + 10
        self.board.player_sprites.add(self.player_hand_sprites)

    @property
    def player_selection(self):
        return self._player_selection

    @player_selection.setter
    def player_selection(self, a):
        self._player_selection = a
        self._initialize_player_hand_sprites()

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        caravan_placement = CaravanPlacement(self.board,self.player_hand_sprites.sprites()[self.player_selection])
                        caravan_placement.main_loop()
                    if event.key == pygame.K_LEFT:
                        self.player_selection -= 1
                        self.player_hand_sprites.draw(self.board.display)
                    if event.key == pygame.K_RIGHT:
                        self.player_selection += 1
                        self.player_hand_sprites.draw(self.board.display)
        
            pygame.display.flip()
        return pygame.QUIT

    