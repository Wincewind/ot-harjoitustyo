import os
import sys
import pygame
from ui.states.handselection import HandSelection
from ui.states.caravanplacement import CaravanPlacement
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "..",".."))
import config
from entities.card import Card
from entities.cardset import CardSet
from entities.deck import Deck
from entities.player import Player
#from sprites.card import CardSprite


class Gameboard:
    def __init__(self, player: Player, opponent: Player):
        self.display = pygame.display.set_mode((config.BOARD_WIDTH, config.BOARD_HEIGHT))
        pygame.display.set_caption("Caravan")
        self.player = player
        self.opponent = opponent
        self.player_sprites = pygame.sprite.Group()
        self.opponent_sprites = pygame.sprite.Group()
        self.caravan_sprites = pygame.sprite.Group()
        self._all_sprites = pygame.sprite.Group()
        
        self._initialize_display()

        self._initialize_sprites()
    
    def clear_card_sprites(self):
        self.display.fill(config.BOARD_COLOR)
        for i in range(3):
            pygame.draw.rect(self.display,
                             config.CARAVAN_BASE_COLOR,
                             config.PLAYER_CARAVAN_BASE_RECTS[i],
                             width=5, border_radius=3)
            pygame.draw.rect(self.display,
                             config.CARAVAN_BASE_COLOR,
                             config.OPPONENT_CARAVAN_BASE_RECTS[i],
                             width=5, border_radius=3)

    def _initialize_display(self):
        self.display.fill(config.BOARD_COLOR)
        CaravanPlacement(self).clear_caravan_area()

    def _initialize_sprites(self):
        HandSelection(self).update_hand_sprites()
        
        self._all_sprites.add(
            self.player_sprites,
            self.opponent_sprites,
            self.caravan_sprites
        )
    @property
    def all_sprites(self):
        self._all_sprites = pygame.sprite.Group()
        self._all_sprites.add(
            self.player_sprites,
            self.opponent_sprites,
            self.caravan_sprites
        )

    def main_loop(self):
        acting_and_waiting = (player,opponent)
        running = True
        while running:
            #self.all_sprites.draw(self.display)
            hand_selection = HandSelection(self)
            CaravanPlacement(self)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if hand_selection.main_loop(acting_and_waiting[0]):
                            # self.player_sprites = pygame.sprite.Group()
                            self.all_sprites = pygame.sprite.Group()
                            # self.opponent_sprites = pygame.sprite.Group()
                            self._initialize_sprites()
                            self._initialize_display()
                            # HandSelection(self)
                            acting_and_waiting = (acting_and_waiting[1],acting_and_waiting[0])
                if event.type == pygame.QUIT:
                    running = False
        
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    c_set = CardSet()
    c_set.create_set_from_all_cards()
    deck = Deck(c_set)
    player = Player(deck)
    deck = Deck(c_set)
    opponent = Player(deck)
    player.deck.shuffle()
    player.deal_a_hand()
    opponent.deck.shuffle()
    opponent.deal_a_hand()
    
    c1 = Card('sylly', 'Spades', 7, False)
    c2 = Card('sylly', 'Hearts', 5, False)
    c3 = Card('sylly', 'Red', 0, True)
    c4 = Card('sylly', 'Diamonds', 12, True)
    c5 = Card('sylly', 'Spades', 13, True)
    opponent.caravans[0].insert_card(c1)
    opponent.caravans[0].insert_card(c2)
    opponent.caravans[0].insert_card(c3)
    opponent.caravans[0].insert_card(c4)
    opponent.caravans[0].insert_card(c5)
    player.caravans[0].insert_card(Card('sylly', 'Hearts', 2, False))
    player.caravans[1].insert_card(Card('sylly', 'Hearts', 4, False))
    player.caravans[2].insert_card(Card('minime453', 'Hearts', 6, False))
    opponent.caravans[1].insert_card(Card('sylly', 'Hearts', 2, False))
    player.caravans[2].insert_card(Card('minime453', 'Spades', 7, False))
    player.caravans[1].insert_card(Card('sylly', 'Diamonds', 5, False))
    opponent.caravans[1].insert_card(Card('sylly', 'Spades', 7, False))
    opponent.caravans[1].insert_card(Card('sylly', 'Diamonds', 5, False))
    player.hand.insert(-1,Card('sylly', 'Hearts', 11, True))
    pygame.init()
    gb = Gameboard(player,opponent)
    gb.main_loop()
    # piirretään all_sprites ryhmän spritet ikkunaan
    # pygame.display.set_caption("Caravan")
    # running = True
    # gb.all_sprites.draw(gb.display)
    # # käynnistään pelisilmukka
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_LEFT:
    #                 gb.player_selection -= 1
    #                 gb.player_hand_sprites.draw(gb.display)
    #             if event.key == pygame.K_RIGHT:
    #                 gb.player_selection += 1
    #                 gb.player_hand_sprites.draw(gb.display)
        
    #     pygame.display.flip()

    # pygame.quit()