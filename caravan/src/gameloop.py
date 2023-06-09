import pygame
import rules
import actions
import config
from ui.eventqueue import EventQueue
from ui.renderer import Renderer
from ui.gamesprites import GameSprites
from repositories.player_data_repository import player_data_repository
from entities.npc import Npc


class GameLoop:
    """Class that handles the Caravan card game gameloop. 
    Processes user actions and renders card sprites accordingly.

    Attributes:
        _renderer: Renderer object that draws and updates the given sprites on its pygame display.
        _game_sprites: GameSprites object that is used to control 
        the placement and color of player and opponent card sprites.
        _event_queue: EventQueue object that outputs the user inputs.
        _states: a list of states the game can be in and are used to only 
        monitor for certain user inputs depending on the state. 
        These can currently be: 'turn_change', 'hand_selection', 
        'caravan_placement', 'caravan_discarding' or 'game_over'.
        _player_turn: bool value representing if it's the player's turn 
        (True) or the opponent's (False).
        pl_data_ids: Name and save slot row number associated with 
        their player data. This is used to update 
        the player_data_repository wins and losses. 
    """

    def __init__(self, renderer: Renderer, game_sprites: GameSprites,
                 event_queue: EventQueue, pl_data_ids: tuple = None):
        pygame.display.set_caption("Caravan")
        self._renderer = renderer
        self._game_sprites = game_sprites
        self._event_queue = event_queue
        self._states = ['turn_change', 'hand_selection', 'caravan_placement']
        self._player_turn = True
        self.pl_data_ids = pl_data_ids

        self.npc_opponent = config.NPC_OPPONENT
        self.npc = Npc(self._game_sprites.opponent, self._game_sprites.player)

    def start(self):
        """Starts the loop of handling events caused by user inputs.
        """
        while True:
            if self._handle_events() is False:
                if self.pl_data_ids is not None and self._renderer.winner == 0:
                    player_data_repository.increment_player_losses(
                        self.pl_data_ids[0],self.pl_data_ids[1])
                break

            self._render()

    def _handle_events(self):
        """Handle user events and depending on the current state, different actions are taken.

        Returns:
            bool: Return false if the game display is quit.
        """
        for event in self._event_queue.get():
            if event.type == pygame.KEYDOWN:
                if self._states[0] == 'turn_change':
                    if not self._player_turn and self.npc_opponent:
                        self.npc_action()
                        continue
                    if event.key == pygame.K_SPACE:
                        self._game_sprites.player_turn = self._player_turn
                        self._states.append(self._states.pop(0))
                        self._game_sprites.player_selection = 0

                elif self._states[0] == 'hand_selection':
                    self.handle_card_selection_event(event)

                elif self._states[0] == 'caravan_placement':
                    self.handle_caravan_selection_event(event)

                elif self._states[0] == 'caravan_discarding':
                    self.handle_caravan_discarding_event(event)

            if self._states[0] == 'game_over' and self._renderer.winner == 0:
                winner = 1
                if rules.is_player_winner(self._game_sprites.player,
                                          self._game_sprites.opponent) is False:
                    winner = 2

                if self.pl_data_ids is not None:
                    if winner == 2:
                        player_data_repository.increment_player_losses(
                            self.pl_data_ids[0],self.pl_data_ids[1])
                    else:
                        player_data_repository.increment_player_wins(
                            self.pl_data_ids[0],self.pl_data_ids[1])

                self._renderer.winner = winner

            if event.type == pygame.QUIT:
                return False
        return None

    def _init_carava_discard(self):
        try:
            self._game_sprites.selected_caravan = next(i for i, c in enumerate(
                self._game_sprites.acting_player.caravans) if len(c.cards) > 0)
            self._states.insert(0, 'caravan_discarding')
            self._game_sprites.update_hand_sprites()
        except StopIteration:
            pass

    def handle_card_selection_event(self, event):
        """Modify the player hand sprites based on the user input.  

        Args:
            event (pygame.event): user input.
        """
        if event.key == pygame.K_SPACE:
            selected_card = self._game_sprites.select_card()
            self._states.append(self._states.pop(0))
            self._game_sprites.chosen_crd_sprite = selected_card
        if event.key == pygame.K_LEFT:
            self._game_sprites.player_selection -= 1
        if event.key == pygame.K_RIGHT:
            self._game_sprites.player_selection += 1
        if event.key == pygame.K_ESCAPE:
            self._states.insert(0, self._states.pop())
            self._game_sprites.player_turn = None
        if event.key == pygame.K_c:
            if actions.discard_card(self._game_sprites.player_selection,
                                    self._game_sprites.acting_player):
                self._game_sprites.player_turn = None
                self._game_sprites.update_hand_sprites()
                self._player_turn = not self._player_turn
                self._states.insert(0, self._states.pop())
        if event.key == pygame.K_e:
            self._init_carava_discard()

    def handle_caravan_discarding_event(self,event):
        """Modify acting player caravan sprites, if they contain cards. 
        Discard a caravan or cancel action based on user input. 

        Args:
            event (pygame.event): user input.
        """
        if event.key in [pygame.K_SPACE,pygame.K_e]:
            if actions.discard_caravan(self._game_sprites.selected_caravan,
                                       self._game_sprites.acting_player):
                self._game_sprites.selected_caravan = None
                self._states = ['turn_change', 'hand_selection', 'caravan_placement']
                self._game_sprites.player_turn = None
                self._player_turn = not self._player_turn
        if event.key == pygame.K_LEFT:
            self._game_sprites.selected_caravan -= 1
        if event.key == pygame.K_RIGHT:
            self._game_sprites.selected_caravan += 1
        if event.key == pygame.K_ESCAPE:
            self._states.pop(0)
            self._game_sprites.selected_caravan = None

    def handle_caravan_selection_event(self, event):
        """Modify the card sprites in caravans based on user inputs.

        Args:
            event (pygame.event): user input.
        """
        if event.key == pygame.K_LEFT:
            self._game_sprites.move_card((-1, 0))
        if event.key == pygame.K_RIGHT:
            self._game_sprites.move_card((1, 0))
        if event.key == pygame.K_UP:
            self._game_sprites.move_card((0, -1))
        if event.key == pygame.K_DOWN:
            self._game_sprites.move_card((0, 1))
        if event.key == pygame.K_ESCAPE:
            self._states.insert(0, self._states.pop())
            self._game_sprites.chosen_crd_sprite = None
        if event.key == pygame.K_SPACE:
            self.try_placing_card()

    def npc_action(self):
        """Perform an action for a npc opponent.
        """
        self.npc.perform_action()
        self._game_sprites.update_hand_sprites()
        self._game_sprites.chosen_crd_sprite = None
        self._player_turn = not self._player_turn
        if rules.is_player_winner(self._game_sprites.player,
                                  self._game_sprites.opponent) is not None:
            self._states.insert(0, "game_over")

    def try_placing_card(self):
        """Check if placing a card is possible into a caravan and if so, 
        do it and change the player_turn. If one of the players has sold 
        all their caravans, set current game state as 'game_over'.
        """
        caravan_idx, placement_idx = self._game_sprites.pos
        if caravan_idx in range(3):
            caravan = self._game_sprites.player.caravans[caravan_idx]
        else:
            caravan = self._game_sprites.opponent.caravans[caravan_idx-3]
        move = (caravan,
                placement_idx,
                self._game_sprites.chosen_crd_sprite.card)

        acting_player = self._game_sprites.player
        opposing_player = self._game_sprites.opponent
        if not self._player_turn:
            acting_player, opposing_player = opposing_player, acting_player
        if actions.play_card(acting_player,
                             opposing_player, move):
            self._game_sprites.player_turn = None
            self._game_sprites.chosen_crd_sprite = None
            self._player_turn = not self._player_turn
            self._states.append(self._states.pop(0))
            self._game_sprites.update_caravan_sprites()
            if rules.is_player_winner(self._game_sprites.player,
                                      self._game_sprites.opponent) is not None:
                self._states.insert(0, "game_over")

    def _render(self):
        self._renderer.render()
