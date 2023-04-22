import os
import sys
import pygame
import copy
import rules
from ui.sprites.card import CardSprite
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, "..",".."))
import config
from entities.player import Player

class GameSprites:
    def __init__(self, display, player: Player, opponent: Player) -> None:
        self._display = display
        self.player = player
        self.opponent = opponent
        self._player_turn = None
        self.player_sprites = pygame.sprite.Group()
        self.opponent_sprites = pygame.sprite.Group()
        self.caravan_sprites = pygame.sprite.Group()
        self.all = pygame.sprite.Group()
        self._player_selection = 0
        self._chosen_crd_sprite = None
        
        self._initialize_sprites()

        self._reset_display_caravans()
        self.caravan_sprites = pygame.sprite.Group()
    
    @property
    def player_turn(self):
        return self._player_turn

    @player_turn.setter
    def player_turn(self, player_turn: bool):
        self._player_turn = player_turn
        if self.player_turn is not None:
            if self.player_turn:
                self.acting_player = self.player
                self.opposing_player = self.opponent
            else:
                self.acting_player, self.opposing_player = self.opposing_player, self.acting_player
        self.update_hand_sprites()
    
    @property
    def player_selection(self):
        return self._player_selection

    @player_selection.setter
    def player_selection(self, idx):
        if 0 <= idx < len(self.acting_player.hand):
            self._player_selection = idx
            self.update_hand_sprites()

    @property
    def chosen_crd_sprite(self):
        return self._chosen_crd_sprite

    @chosen_crd_sprite.setter
    def chosen_crd_sprite(self, card):
        self._chosen_crd_sprite = card
        self._reset_display_caravans()
        if self._chosen_crd_sprite is not None:
            if not self.player_turn:
                    self.op_display_caravans[0].insert_card(self._chosen_crd_sprite.card)
                    self.pos = (3,len(self.op_display_caravans[0].cards)-1)
            else:
                self.pl_display_caravans[0].insert_card(self._chosen_crd_sprite.card)
                self.pos = (0,len(self.pl_display_caravans[0].cards)-1)
        self.update_caravan_sprites()

    def select_card(self):
        if self.player_turn:
            return self.player_sprites.sprites()[self.player_selection]
        return self.opponent_sprites.sprites()[self.player_selection]
    
    def _initialize_sprites(self):
        self.update_hand_sprites()
        self.clear_caravan_area()
        self.update_all_sprites()
        
    def update_all_sprites(self):
        self.all = pygame.sprite.Group()
        self.all.add(
            self.player_sprites,
            self.opponent_sprites,
            self.caravan_sprites
        )

    # def _clear_player_area(self):
    #     if self.player_turn:
    #         pygame.display.fill(config.BOARD_COLOR,config.PLAYER_AREA_RECT)
    #     else:
    #         pygame.display.fill(config.BOARD_COLOR,config.OPPONENT_AREA_RECT)

    def update_hand_sprites(self):
        if self._player_turn is None:
            cards_to_show = (False,False)
        elif self._player_turn:
            cards_to_show = (True,False)
        else:
            cards_to_show = (False,True)

        # Update player hand sprites
        if cards_to_show == (False, False) or cards_to_show[0]:
            self.player_sprites.empty()
            x = config.BOARD_WIDTH / 3 - 50
            y = config.BOARD_HEIGHT - config.CARD_HEIGHT - 20
            for idx, crd in enumerate(self.player.hand):
                spr = CardSprite(crd,x,y,cards_to_show[0])
                spr.set_overlay()
                if cards_to_show[0] and idx == self._player_selection:
                    spr.set_overlay(CardSprite.OVERLAY_YELLOW)
                self.player_sprites.add(spr)
                x += CardSprite.CARD_DIMENSIONS[0] + 10
            x = config.BOARD_WIDTH - config.CARD_WIDTH - 10
            y = config.BOARD_HEIGHT - config.CARD_HEIGHT - 20
            self.player_sprites.add(CardSprite(self.player.deck.cards[-1],x,y,False))

        # Update opponent hand sprites
        if cards_to_show == (False, False) or cards_to_show[1]:
            self.opponent_sprites = pygame.sprite.Group()
            x = config.BOARD_WIDTH / 3 - 50
            y = 20
            for idx, crd in enumerate(self.opponent.hand):
                spr = CardSprite(crd,x,y,cards_to_show[1])
                spr.set_overlay()
                if cards_to_show[1] and idx == self._player_selection:
                    spr.set_overlay(CardSprite.OVERLAY_YELLOW)
                self.opponent_sprites.add(spr)
                x += CardSprite.CARD_DIMENSIONS[0] + 10
            x = config.BOARD_WIDTH - config.CARD_WIDTH - 10
            self.opponent_sprites.add(CardSprite(self.opponent.deck.cards[-1],x,y,False))

    def _reset_display_caravans(self):
        self.pl_display_caravans = tuple(copy.copy(c) for c in self.player.caravans)
        self.op_display_caravans = tuple(copy.copy(c) for c in self.opponent.caravans)

    def update_caravan_sprites(self):
        self.caravan_sprites = pygame.sprite.Group()
        player = self.acting_player
        opponent = self.opposing_player
        if self.acting_player == self.opponent:
            player, opponent = opponent, player

        pl_setup_details = {'caravan rects': config.PLAYER_CARAVAN_BASE_RECTS,
                            'display caravans': self.pl_display_caravans,
                            'caravan owner': player,
                            'caravan direction': 1}
        op_setup_details = {'caravan rects': config.OPPONENT_CARAVAN_BASE_RECTS,
                            'display caravans': self.op_display_caravans,
                            'caravan owner': opponent,
                            'caravan direction': -1}
        for setup in [pl_setup_details,op_setup_details]:
            for i, caravan in enumerate(setup['display caravans']):
                x = setup['caravan rects'][i][0]+5
                y = setup['caravan rects'][i][1]+5
                for j, crd in enumerate(caravan.cards):
                    spr = CardSprite(crd,x,y)
                    if self._chosen_crd_sprite is not None and self._chosen_crd_sprite.card == crd:
                        move = (setup['caravan owner'].caravans[i], j, crd)
                        print(rules.check_if_legal_move(
                            self.acting_player,self.opposing_player,move))
                        if rules.check_if_legal_move(
                            self.acting_player,self.opposing_player,move)[0]:
                            spr.set_overlay(CardSprite.OVERLAY_GREEN)
                        else:
                            spr.set_overlay(CardSprite.OVERLAY_RED)
                    self.caravan_sprites.add(spr)
                    y = y + setup['caravan direction']*config.CARD_HEIGHT/3.5

    def _determine_caravan_font_color(self,car_val,opposing_car_val):
        font_color = (255,255,255)
        if rules.check_if_caravan_sold(car_val,opposing_car_val):
            font_color = (255, 226, 99)
        if rules.CARAVAN_MAX < car_val:
            font_color = (196, 65, 93)
        return font_color
         

    def clear_caravan_area(self):
        self._display.fill(config.BOARD_COLOR,config.CARAVAN_AREA_RECT)
        caravan_base_width = config.PLAYER_CARAVAN_BASE_RECTS[0][2]
        for i in range(3):
            font_color = self._determine_caravan_font_color(
                self.player.caravans[i].value,
                self.opponent.caravans[i].value)
            pygame.draw.rect(self._display,
                             config.CARAVAN_BASE_COLOR,
                             config.PLAYER_CARAVAN_BASE_RECTS[i],
                             width=5, border_radius=3)

            crvn_total = config.FONT.render(str(self.player.caravans[i].value),
                                            True,
                                            font_color)
            total_x = config.PLAYER_CARAVAN_BASE_RECTS[i][0]+caravan_base_width+5
            self._display.blit(crvn_total,(total_x,
                                                config.PLAYER_CARAVAN_BASE_RECTS[i][1]))

            pygame.draw.rect(self._display,
                             config.CARAVAN_BASE_COLOR,
                             config.OPPONENT_CARAVAN_BASE_RECTS[i],
                             width=5, border_radius=3)
            
            font_color = self._determine_caravan_font_color(
                self.opponent.caravans[i].value,
                self.player.caravans[i].value)
            crvn_total = config.FONT.render(str(self.opponent.caravans[i].value),
                                            True,
                                            font_color)
            total_x = config.OPPONENT_CARAVAN_BASE_RECTS[i][0]+caravan_base_width+5
            self._display.blit(crvn_total,(total_x,
                                                config.OPPONENT_CARAVAN_BASE_RECTS[i][1]))

    def move_card(self,movement):
        caravan_idx, placement_idx = self.pos
        if caravan_idx in range(3):
            self.pl_display_caravans[caravan_idx].cards.remove(self._chosen_crd_sprite.card)
        else:
            self.op_display_caravans[caravan_idx-3].cards.remove(self._chosen_crd_sprite.card)
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
        caravan.insert_card(self._chosen_crd_sprite.card,placement_idx)
        self.pos = (caravan_idx,placement_idx)
        self.clear_caravan_area()
        self.update_caravan_sprites()