import pygame
from sprites.card import CardSprite
from states.caravanplacement import CaravanPlacement
import config

class HandSelection():
    def __init__(self,gameboard,acting_player=None) -> None:
        self.board = gameboard
        self._player_selection = 0
        self.acting_player = acting_player
        self.initialize_hand_sprites()
        self.board.all_sprites.draw(self.board.display)

    def clear_player_area(self):
        if self.acting_player == self.board.player:
            self.board.display.fill(config.BOARD_COLOR,config.PLAYER_AREA_RECT)
        else:
            self.board.display.fill(config.BOARD_COLOR,config.OPPONENT_AREA_RECT)
    
    def initialize_hand_sprites(self):
        self.player_hand_sprites = pygame.sprite.Group()
        if self.acting_player is None:
            cards_to_show = (False,False)
        elif self.acting_player == self.board.player:
            cards_to_show = (True,False)
        else:
            cards_to_show = (False,True)

        # Update player hand sprites
        if cards_to_show == (False, False) or cards_to_show[0]:
            self.board.player_sprites = pygame.sprite.Group()
            x = config.BOARD_WIDTH / 3 - 50
            y = config.BOARD_HEIGHT - config.CARD_HEIGHT - 20
            for idx, crd in enumerate(self.board.player.hand):
                spr = CardSprite(crd,x,y,cards_to_show[0])
                spr.set_overlay()
                if cards_to_show[0] and idx == self._player_selection:
                    spr.set_overlay(CardSprite.OVERLAY_YELLOW)
                self.player_hand_sprites.add(spr)
                x += CardSprite.CARD_DIMENSIONS[0] + 10
            x = config.BOARD_WIDTH - config.CARD_WIDTH - 10
            y = config.BOARD_HEIGHT - config.CARD_HEIGHT - 20
            self.player_hand_sprites.add(CardSprite(self.board.player.deck.cards[-1],x,y,False))
            self.board.player_sprites.add(self.player_hand_sprites)

        # Update opponent hand sprites
        if cards_to_show == (False, False) or cards_to_show[1]:
            self.board.opponent_sprites = pygame.sprite.Group()
            x = config.BOARD_WIDTH / 3 - 50
            y = 20
            for idx, crd in enumerate(self.board.opponent.hand):
                spr = CardSprite(crd,x,y,cards_to_show[1])
                spr.set_overlay()
                if cards_to_show[1] and idx == self._player_selection:
                    spr.set_overlay(CardSprite.OVERLAY_YELLOW)
                self.player_hand_sprites.add(spr)
                x += CardSprite.CARD_DIMENSIONS[0] + 10
            x = config.BOARD_WIDTH - config.CARD_WIDTH - 10
            self.player_hand_sprites.add(CardSprite(self.board.opponent.deck.cards[-1],x,y,False))
            self.board.opponent_sprites.add(self.player_hand_sprites)
            #self.board.all_sprites.draw(self.board.display)

    @property
    def player_selection(self):
        return self._player_selection

    @player_selection.setter
    def player_selection(self, a):
        self._player_selection = a
        self.initialize_hand_sprites()

    def main_loop(self,acting_player):
        self.acting_player = acting_player
        self.player_selection = 0
        self.clear_player_area()
        self.player_hand_sprites.draw(self.board.display)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        selected_card = self.player_hand_sprites.sprites()[self.player_selection]
                        caravan_placement = CaravanPlacement(self.board,self.acting_player,selected_card)
                        if caravan_placement.main_loop():
                            self.initialize_hand_sprites()
                            self.board.all_sprites.draw(self.board.display)
                            return True
                    if event.key == pygame.K_LEFT:
                        self.player_selection -= 1
                        self.player_hand_sprites.draw(self.board.display)
                    if event.key == pygame.K_RIGHT:
                        self.player_selection += 1
                        self.player_hand_sprites.draw(self.board.display)
                    if event.key == pygame.K_ESCAPE:
                        running = False
        
            pygame.display.flip()
        return pygame.QUIT

    