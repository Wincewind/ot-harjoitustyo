import os
import sys
import pygame
from sprites.card import CardSprite
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "..",".."))
from entities.card import Card
from entities.cardset import CardSet
from entities.deck import Deck
from entities.player import Player



class GameBoard:
    WIDTH = 1600
    HEIGHT = 1000
    COLOR = (53,101,77)
    CARAVAN_BASE_COLOR = (202,154,178)
    def __init__(self, player: Player, opponent: Player):
        self.player = player
        self.opponent = opponent
        self.player_hand_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.opponent_sprites = pygame.sprite.Group()
        self.caravan_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self._player_selection = 0
        self.player_caravan_pos = [0,0,0]
        self.opponent_caravan_pos = [0,0,0]
        
        self._initialize_display()

        self._initialize_sprites()

    def _initialize_display(self):
        self.display = pygame.display.set_mode((GameBoard.WIDTH, GameBoard.HEIGHT))
        self.display.fill(GameBoard.COLOR)
        x = GameBoard.WIDTH*0.4 - CardSprite.CARD_DIMENSIONS[0]
        y = GameBoard.HEIGHT//2 - CardSprite.CARD_DIMENSIONS[1]
        w = CardSprite.CARD_DIMENSIONS[0] + 10
        h = CardSprite.CARD_DIMENSIONS[1] + 10
        for i in range(3):
            self.opponent_caravan_pos[i] = (x, y, w, h)
            pygame.draw.rect(self.display, GameBoard.CARAVAN_BASE_COLOR, (x, y, w, h), width=5, border_radius=3)
            x += CardSprite.CARD_DIMENSIONS[0] + 100
        x = GameBoard.WIDTH*0.4 - CardSprite.CARD_DIMENSIONS[0]
        y = GameBoard.HEIGHT//2 + CardSprite.CARD_DIMENSIONS[1]/2
        w = CardSprite.CARD_DIMENSIONS[0] + 10
        h = CardSprite.CARD_DIMENSIONS[1] + 10
        for i in range(3):
            self.player_caravan_pos[i] = (x, y, w, h)
            pygame.draw.rect(self.display,
                             GameBoard.CARAVAN_BASE_COLOR,
                             (x, y, w, h), width=5,
                             border_radius=3)
            x += CardSprite.CARD_DIMENSIONS[0] + 100
    
    def _initialize_caravan_sprites(self):
        self.caravan_sprites = pygame.sprite.Group()
        for i, caravan in enumerate(self.player.caravans):
            x = self.player_caravan_pos[i][0]+5
            y = self.player_caravan_pos[i][1]+5
            for crd in caravan.cards:
                spr = CardSprite(crd,x,y)
                self.caravan_sprites.add(spr)
                y += CardSprite.CARD_DIMENSIONS[1]/3.5
        for i, caravan in enumerate(self.opponent.caravans):
            x = self.opponent_caravan_pos[i][0]+5
            y = self.opponent_caravan_pos[i][1]+5
            for crd in caravan.cards:
                spr = CardSprite(crd,x,y)
                self.caravan_sprites.add(spr)
                y -= CardSprite.CARD_DIMENSIONS[1]/3.5

    def _initialize_player_hand_sprites(self):
        self.player_hand_sprites = pygame.sprite.Group()
        x = GameBoard.WIDTH // 3 - 50
        y = GameBoard.HEIGHT - CardSprite.CARD_DIMENSIONS[1] - 20
        for idx, crd in enumerate(self.player.hand):
            spr = CardSprite(crd,x,y)
            spr.set_overlay()
            if idx == self._player_selection:
                spr.set_overlay(CardSprite.OVERLAY_YELLOW)
            self.player_hand_sprites.add(spr)
            x += CardSprite.CARD_DIMENSIONS[0] + 10
        self.player_sprites.add(self.player_hand_sprites)

    def _initialize_sprites(self):
        self._initialize_player_hand_sprites()
        x = GameBoard.WIDTH - CardSprite.CARD_DIMENSIONS[0] - 10
        y = GameBoard.HEIGHT - CardSprite.CARD_DIMENSIONS[1] - 20
        self.player_sprites.add(CardSprite(self.player.deck.cards[-1],x,y,False))

        x = GameBoard.WIDTH // 3 - 50
        y = 20
        for crd in self.opponent.hand:
            self.opponent_sprites.add(CardSprite(crd,x,y,False))
            x += CardSprite.CARD_DIMENSIONS[0] + 10

        x = GameBoard.WIDTH - CardSprite.CARD_DIMENSIONS[0] - 10
        self.opponent_sprites.add(CardSprite(self.opponent.deck.cards[-1],x,y,False))
        self._initialize_caravan_sprites()
        
        self.all_sprites.add(
            self.player_sprites,
            self.opponent_sprites,
            self.player_hand_sprites,
            self.caravan_sprites
        )
    @property
    def player_selection(self):
        return self._player_selection

    @player_selection.setter
    def player_selection(self, a):
        self._player_selection = a
        self._initialize_player_hand_sprites()

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
    
    player.caravans[0].insert_card(Card('sylly', 'Hearts', 2, False))
    player.caravans[1].insert_card(Card('sylly', 'Hearts', 4, False))
    player.caravans[2].insert_card(Card('minime453', 'Hearts', 6, False))
    opponent.caravans[1].insert_card(Card('sylly', 'Hearts', 2, False))
    player.caravans[1].insert_card(Card('minime453', 'Spades', 7, False))
    player.caravans[1].insert_card(Card('sylly', 'Diamonds', 5, False))
    opponent.caravans[1].insert_card(Card('sylly', 'Spades', 7, False))
    opponent.caravans[1].insert_card(Card('sylly', 'Diamonds', 5, False))
    pygame.init()
    gb = GameBoard(player,opponent)
    # piirretään all_sprites ryhmän spritet ikkunaan
    pygame.display.set_caption("Caravan")
    running = True
    gb.all_sprites.draw(gb.display)
    # käynnistään pelisilmukka
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gb.player_selection -= 1
                    gb.player_hand_sprites.draw(gb.display)
                if event.key == pygame.K_RIGHT:
                    gb.player_selection += 1
                    gb.player_hand_sprites.draw(gb.display)
        
        pygame.display.flip()

    pygame.quit()