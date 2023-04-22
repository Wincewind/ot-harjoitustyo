from ui.sprites.card import CardSprite
# from entities.card import Card
import rules
import copy
import pygame
import config
import actions

class CaravanPlacement:
    def __init__(self, gameboard, acting_player=None, card: CardSprite=None) -> None:
        self.board = gameboard
        self.c_sprite = card
        self.acting_player = acting_player
        if self.acting_player is not self.board.opponent:
            self.opposing_player = self.board.opponent
            self.acting_player = self.board.player
        else:
            self.opposing_player = self.board.player
        self._reset_display_caravans()
        self.caravan_sprites = pygame.sprite.Group()
        if self.c_sprite is not None:
            if self.acting_player is self.board.opponent:
                self.op_display_caravans[0].insert_card(self.c_sprite.card)
                self.pos = (3,len(self.op_display_caravans[0].cards)-1)
            else:
                self.pl_display_caravans[0].insert_card(self.c_sprite.card)
                self.pos = (0,len(self.pl_display_caravans[0].cards)-1)
        self.update_caravan_sprites()
        self.caravan_sprites.draw(self.board.display)

    def _reset_display_caravans(self):
        self.pl_display_caravans = tuple(copy.copy(c) for c in self.board.player.caravans)
        self.op_display_caravans = tuple(copy.copy(c) for c in self.board.opponent.caravans)

    def update_caravan_sprites(self):
        self.caravan_sprites = pygame.sprite.Group()
        player = self.acting_player
        opponent = self.opposing_player
        if self.acting_player == self.board.opponent:
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
                    if self.c_sprite is not None and self.c_sprite.card == crd:
                        move = (setup['caravan owner'].caravans[i], j, crd)
                        print(self.opposing_player.get_hand_as_str())
                        print(rules.check_if_legal_move(self.acting_player,self.opposing_player,move))
                        if rules.check_if_legal_move(self.acting_player,self.opposing_player,move)[0]:
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
        self.board.display.fill(config.BOARD_COLOR,config.CARAVAN_AREA_RECT)
        caravan_base_width = config.PLAYER_CARAVAN_BASE_RECTS[0][2]
        for i in range(3):
            font_color = self._determine_caravan_font_color(
                self.board.player.caravans[i].value,
                self.board.opponent.caravans[i].value)
            pygame.draw.rect(self.board.display,
                             config.CARAVAN_BASE_COLOR,
                             config.PLAYER_CARAVAN_BASE_RECTS[i],
                             width=5, border_radius=3)

            crvn_total = config.FONT.render(str(self.board.player.caravans[i].value),
                                            True,
                                            font_color)
            total_x = config.PLAYER_CARAVAN_BASE_RECTS[i][0]+caravan_base_width+5
            self.board.display.blit(crvn_total,(total_x,
                                                config.PLAYER_CARAVAN_BASE_RECTS[i][1]))

            pygame.draw.rect(self.board.display,
                             config.CARAVAN_BASE_COLOR,
                             config.OPPONENT_CARAVAN_BASE_RECTS[i],
                             width=5, border_radius=3)
            
            font_color = self._determine_caravan_font_color(
                self.board.opponent.caravans[i].value,
                self.board.player.caravans[i].value)
            crvn_total = config.FONT.render(str(self.board.opponent.caravans[i].value),
                                            True,
                                            font_color)
            total_x = config.OPPONENT_CARAVAN_BASE_RECTS[i][0]+caravan_base_width+5
            self.board.display.blit(crvn_total,(total_x,
                                                config.OPPONENT_CARAVAN_BASE_RECTS[i][1]))

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
        self.update_caravan_sprites()
        self.caravan_sprites.draw(self.board.display)

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._reset_display_caravans()
                    self.clear_caravan_area()
                    self.update_caravan_sprites()
                    self.caravan_sprites.draw(self.board.display)
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
                    if event.key == pygame.K_ESCAPE:
                        self._reset_display_caravans()
                        self.clear_caravan_area()
                        self.update_caravan_sprites()
                        self.caravan_sprites.draw(self.board.display)
                        running = False
                    if event.key == pygame.K_SPACE:
                        caravan_idx, placement_idx = self.pos
                        if caravan_idx in range(3):
                            caravan = self.board.player.caravans[caravan_idx]
                        else:
                            caravan = self.board.opponent.caravans[caravan_idx-3]
                        move = (caravan,
                                placement_idx,
                                self.c_sprite.card)
                        if actions.play_card(self.acting_player,self.opposing_player,move):
                            self._reset_display_caravans()
                            self.clear_caravan_area()
                            self.update_caravan_sprites()
                            # self.caravan_sprites.draw(self.board.display)
                            # pygame.display.flip()
                            return True
            pygame.display.flip()
        return False