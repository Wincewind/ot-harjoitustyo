from sprites.card import CardSprite
from entities.card import Card
import rules
import copy
import pygame

class CaravanPlacement:
    def __init__(self, gameboard, card: CardSprite=None) -> None:
        self.board = gameboard
        self.c_sprite = card
        self.pl_display_caravans = tuple(copy.copy(c) for c in self.board.player.caravans)
        self.op_display_caravans = tuple(copy.copy(c) for c in self.board.opponent.caravans)
        self.caravan_sprites = pygame.sprite.Group()
        if self.c_sprite is not None:
            self.pl_display_caravans[0].insert_card(self.c_sprite.card)
            self.pos = (0,len(self.pl_display_caravans[0].cards)-1)
        self._initialize_caravan_sprites()
        self.caravan_sprites.draw(self.board.display)
        self.player_caravan_pos = [0,0,0]
        self.opponent_caravan_pos = [0,0,0]

    def _initialize_caravan_sprites(self):
        self.caravan_sprites = pygame.sprite.Group()
        for i, caravan in enumerate(self.pl_display_caravans):
            x = self.board.player_caravan_pos[i][0]+5
            y = self.board.player_caravan_pos[i][1]+5
            for j, crd in enumerate(caravan.cards):
                spr = CardSprite(crd,x,y)
                if self.c_sprite is not None and self.c_sprite.card == crd:
                    # if j == len(caravan.cards)-1:
                    #     j = -1
                    move = (self.board.player.caravans[i], j, crd)
                    print(move[1])
                    print(rules.check_if_legal_move(self.board.player,self.board.opponent,move))
                    if rules.check_if_legal_move(self.board.player,self.board.opponent,move)[0]:
                        spr.set_overlay(CardSprite.OVERLAY_GREEN)
                    else:
                        spr.set_overlay(CardSprite.OVERLAY_RED)
                self.caravan_sprites.add(spr)
                y += CardSprite.CARD_DIMENSIONS[1]/3.5
        for i, caravan in enumerate(self.op_display_caravans):
            x = self.board.opponent_caravan_pos[i][0]+5
            y = self.board.opponent_caravan_pos[i][1]+5
            for j, crd in enumerate(caravan.cards):
                spr = CardSprite(crd,x,y)
                if self.c_sprite is not None and self.c_sprite.card == crd:
                    if j == len(caravan.cards)-1:
                        j = -1
                    move = (self.board.opponent.caravans[i], j, crd)
                    print(rules.check_if_legal_move(self.board.player,self.board.opponent,move))
                    if rules.check_if_legal_move(self.board.player,self.board.opponent,move)[0]:
                        spr.set_overlay(CardSprite.OVERLAY_GREEN)
                    else:
                        spr.set_overlay(CardSprite.OVERLAY_RED)
                self.caravan_sprites.add(spr)
                y -= CardSprite.CARD_DIMENSIONS[1]/3.5

    def clear_caravan_area(self):
        x = self.board.WIDTH*0.4 - CardSprite.CARD_DIMENSIONS[0]
        y = CardSprite.CARD_DIMENSIONS[1]+20
        w = (CardSprite.CARD_DIMENSIONS[0] + 100)*3
        h = (self.board.HEIGHT - CardSprite.CARD_DIMENSIONS[1]*2-40)
        rect = pygame.Rect(x, y, w, h)
        self.board.display.fill(self.board.COLOR,rect)
        x = self.board.WIDTH*0.4 - CardSprite.CARD_DIMENSIONS[0]
        y = self.board.HEIGHT//2 - CardSprite.CARD_DIMENSIONS[1]
        w = CardSprite.CARD_DIMENSIONS[0] + 10
        h = CardSprite.CARD_DIMENSIONS[1] + 10
        for i in range(3):
            self.opponent_caravan_pos[i] = (x, y, w, h)
            pygame.draw.rect(self.board.display, self.board.CARAVAN_BASE_COLOR, (x, y, w, h), width=5, border_radius=3)
            x += CardSprite.CARD_DIMENSIONS[0] + 100
        x = self.board.WIDTH*0.4 - CardSprite.CARD_DIMENSIONS[0]
        y = self.board.HEIGHT//2 + CardSprite.CARD_DIMENSIONS[1]/2
        w = CardSprite.CARD_DIMENSIONS[0] + 10
        h = CardSprite.CARD_DIMENSIONS[1] + 10
        for i in range(3):
            self.player_caravan_pos[i] = (x, y, w, h)
            pygame.draw.rect(self.board.display,
                             self.board.CARAVAN_BASE_COLOR,
                             (x, y, w, h), width=5,
                             border_radius=3)
            x += CardSprite.CARD_DIMENSIONS[0] + 100

    def move_card(self,movement):
        caravan_idx, placement_idx = self.pos
        if caravan_idx in range(3):
            self.pl_display_caravans[caravan_idx].cards.remove(self.c_sprite.card)
        else:
            self.op_display_caravans[caravan_idx-3].cards.remove(self.c_sprite.card)
        caravan_idx += movement[0]
        placement_idx += movement[1]
        if caravan_idx < 0:
            caravan_idx = 5
        elif caravan_idx > 5:
            caravan_idx = 0
        if caravan_idx in range(3):
            caravan = self.pl_display_caravans[caravan_idx]
        else:
            caravan = self.op_display_caravans[caravan_idx-3]
        placement_idx = max(placement_idx,0)
        if placement_idx >= len(caravan.cards):
            placement_idx = len(caravan.cards)
        caravan.insert_card(self.c_sprite.card,placement_idx)
        self.pos = (caravan_idx,placement_idx)
        self.clear_caravan_area()
        self._initialize_caravan_sprites()
        self.caravan_sprites.draw(self.board.display)


    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_card((-1,0))
                    if event.key == pygame.K_RIGHT:
                        self.move_card((1,0))
                    if event.key == pygame.K_UP:
                        self.move_card((0,-1))
                    if event.key == pygame.K_DOWN:
                        self.move_card((0,1))
                #         self.player_hand_sprites.draw(self.board.display)
        
            pygame.display.flip()
        return pygame.QUIT