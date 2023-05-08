import copy
import pygame
from entities.player import Player
import config
import rules
from ui.sprites.card import CardSprite


class GameSprites:
    """Class representing the gamesprites to be controlled during the game. 
    Things like: card positions, should the card front or backsides be shown, 
    what overlay to use depending if a card is selected or placed into a legal or illegal position.

    Attributes:
        _display: pygame display on to which draw shapes, before the sprites can be rendered.
        player: Player object representing the starting player with sprites 
        rendered at the bottom side of the screen.
        opponent: Player object representing the opposing player with sprites 
        at the upper side of the screen. 
        _player_turn: nullable bool value representing if it's the player's turn. 
        If it's False, it's the opponent's turn and if it's None, it's neither's and the turn is changing.
        player_sprites: pygame sprite group for the player's sprites.
        opponent_sprites: pygame sprite group for the opponent's sprites.
        caravan_sprites: pygame sprite group for all of the caravans.
        all: pygame sprite group for all sprites.
        _player_selection: int that represents the card selection in player's or opponent's hand.
        _chosen_crd_sprite: A card sprite chosen to be placed in a caravan.
        acting_player: Reference to either the player or opponent attribute, depending on whose turn it is.
        opposing_player: Reference to either the player or opponent attribute, depending on whose turn it is.
        pl_display_caravans: A copy of the player-attribute's caravan's 
        in which the moving of the card can be done before placing it and check if the placement is legal.
        op_display_caravans: Same as with pl_display_caravans but for the opponent-attribute.
    """

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

    @property
    def player_turn(self):
        """_player_turn attribute that controls the acting_player and opposing_player attributes. 
        If this is set to True, player attribute is set as acting_player 
        and opponent as opposing_player. If False, vice versa.
        """
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
        """int that represents the card selection in acting_player's hand. 
        When updated, the player_sprites and opponent_sprites are updated accordingly.
        """
        return self._player_selection

    @player_selection.setter
    def player_selection(self, idx):
        if 0 <= idx < len(self.acting_player.hand):
            self._player_selection = idx
            self.update_hand_sprites()

    @property
    def chosen_crd_sprite(self):
        """Set or get the a card sprite as the one selected 
        from acting_player's hand. This card's sprite will 
        then be placed in the acting_player's first "diplayed" caravan. 

        Returns:
            CardSprite: The selected CardSprite object.
        """
        return self._chosen_crd_sprite

    @chosen_crd_sprite.setter
    def chosen_crd_sprite(self, card):
        self._chosen_crd_sprite = card
        self._reset_display_caravans()
        if self._chosen_crd_sprite is not None:
            if not self.player_turn:
                self.op_display_caravans[0].insert_card(
                    self._chosen_crd_sprite.card)
                self.pos = (3, len(self.op_display_caravans[0].cards)-1)
            else:
                self.pl_display_caravans[0].insert_card(
                    self._chosen_crd_sprite.card)
                self.pos = (0, len(self.pl_display_caravans[0].cards)-1)
        self.update_caravan_sprites()

    def select_card(self):
        """Get the card sprite at current player_selection.

        Returns:
            CardSprite: CardSprite object from 
            either the player_sprites or opponent_sprites depending on the player_turn.
        """
        if self.player_turn:
            return self.player_sprites.sprites()[self.player_selection]
        return self.opponent_sprites.sprites()[self.player_selection]

    def _initialize_sprites(self):
        self.update_hand_sprites()
        self.clear_caravan_area()
        self.update_all_sprites()

    def update_all_sprites(self):
        """Update all attribute with current player_sprites, opponent_sprites and caravan_sprites."""
        self.all = pygame.sprite.Group()
        self.all.add(
            self.player_sprites,
            self.opponent_sprites,
            self.caravan_sprites
        )

    def update_hand_sprites(self):
        """Update the hand sprites of player and opponent. 
        Depending whose turn it is, either CardSprite backs or fronts are shown and a 
        overlay is added if the CardSprite in question is under player selection.
        """
        if self._player_turn is None:
            cards_to_show = (False, False)
        elif self._player_turn:
            cards_to_show = (True, False)
        else:
            cards_to_show = (False, True)

        # Update player hand sprites
        if cards_to_show == (False, False) or cards_to_show[0]:
            self.player_sprites.empty()
            x = config.BOARD_WIDTH / 3 - 50
            y = config.BOARD_HEIGHT - config.CARD_HEIGHT - 20
            for idx, crd in enumerate(self.player.hand):
                spr = CardSprite(crd, x, y, cards_to_show[0])
                spr.set_overlay()
                if cards_to_show[0] and idx == self._player_selection:
                    spr.set_overlay(CardSprite.OVERLAY_YELLOW)
                self.player_sprites.add(spr)
                x += CardSprite.CARD_DIMENSIONS[0] + 10
            x = config.BOARD_WIDTH - config.CARD_WIDTH - 10
            y = config.BOARD_HEIGHT - config.CARD_HEIGHT - 20
            self.player_sprites.add(CardSprite(
                self.player.deck.cards[-1], x, y, False))

        # Update opponent hand sprites
        if cards_to_show == (False, False) or cards_to_show[1]:
            self.opponent_sprites = pygame.sprite.Group()
            x = config.BOARD_WIDTH / 3 - 50
            y = 20
            for idx, crd in enumerate(self.opponent.hand):
                spr = CardSprite(crd, x, y, cards_to_show[1])
                spr.set_overlay()
                if cards_to_show[1] and idx == self._player_selection:
                    spr.set_overlay(CardSprite.OVERLAY_YELLOW)
                self.opponent_sprites.add(spr)
                x += CardSprite.CARD_DIMENSIONS[0] + 10
            x = config.BOARD_WIDTH - config.CARD_WIDTH - 10
            self.opponent_sprites.add(CardSprite(
                self.opponent.deck.cards[-1], x, y, False))

    def _reset_display_caravans(self):
        self.pl_display_caravans = tuple(
            copy.copy(c) for c in self.player.caravans)
        self.op_display_caravans = tuple(
            copy.copy(c) for c in self.opponent.caravans)

    def update_caravan_sprites(self):
        """Update the pl and op display_caravan card sprites. To be executed each 
        time the chosen_card is moved or if placement is done or canceled.
        CardSprite overlay color is set based on if the chosen_card's current 
        placement is legal or not. 
        """
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
        for setup in [pl_setup_details, op_setup_details]:
            for i, caravan in enumerate(setup['display caravans']):
                x = setup['caravan rects'][i][0]+5
                y = setup['caravan rects'][i][1]+5
                for j, crd in enumerate(caravan.cards):
                    spr = CardSprite(crd, x, y)
                    if self._chosen_crd_sprite is not None and self._chosen_crd_sprite.card == crd:
                        move = (setup['caravan owner'].caravans[i], j, crd)
                        if rules.check_if_legal_move(
                                self.acting_player, self.opposing_player, move)[0]:
                            spr.set_overlay(CardSprite.OVERLAY_GREEN)
                        else:
                            spr.set_overlay(CardSprite.OVERLAY_RED)
                    self.caravan_sprites.add(spr)
                    y = y + setup['caravan direction']*config.CARD_HEIGHT/3.5

    def _determine_caravan_font_color(self, car_val, opposing_car_val):
        """Set used caravan font color based on their value. White if yet to be sold, 
        yellow if sold and red if over limit. 

        Args:
            car_val (int): value of a caravan
            opposing_car_val (int): value of the opposing caravan.

        Returns:
            tuple(int,int,int): RGB values of the font.
        """
        font_color = (255, 255, 255)
        if rules.check_if_caravan_sold(car_val, opposing_car_val):
            font_color = (255, 226, 99)
        if rules.CARAVAN_MAX < car_val:
            font_color = (196, 65, 93)
        return font_color

    def clear_caravan_area(self):
        """Clear the game board center area of drawn CardSprites. 
        Write current values of caravans' on the side of the placement areas. 
        """
        self._display.fill(config.BOARD_COLOR, config.CARAVAN_AREA_RECT)
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
            total_x = config.PLAYER_CARAVAN_BASE_RECTS[i][0] + \
                caravan_base_width+5
            self._display.blit(crvn_total, (total_x,
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
            total_x = config.OPPONENT_CARAVAN_BASE_RECTS[i][0] + \
                caravan_base_width+5
            self._display.blit(crvn_total, (total_x,
                                            config.OPPONENT_CARAVAN_BASE_RECTS[i][1]))

    def move_card(self, movement):
        """Move card in the pl and op display_caravans.

        Args:
            movement (tuple(int,int)): A tuple of index movement from caravan 
            to another and placement within the cards of a caravan.
        """
        caravan_idx, placement_idx = self.pos
        if caravan_idx in range(3):
            self.pl_display_caravans[caravan_idx].cards.remove(
                self._chosen_crd_sprite.card)
        else:
            self.op_display_caravans[caravan_idx -
                                     3].cards.remove(self._chosen_crd_sprite.card)
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
        placement_idx = max(placement_idx, 0)
        if placement_idx >= len(caravan.cards):
            placement_idx = len(caravan.cards)
        caravan.insert_card(self._chosen_crd_sprite.card, placement_idx)
        self.pos = (caravan_idx, placement_idx)
        self.clear_caravan_area()
        self.update_caravan_sprites()
