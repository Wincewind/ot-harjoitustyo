import pygame
import rules
import actions
from ui.eventqueue import EventQueue
from ui.renderer import Renderer
from ui.gamesprites import GameSprites
from repositories.player_data_repository import player_data_repository


class GameLoop:
    def __init__(self, renderer: Renderer, game_sprites: GameSprites,
                 event_queue: EventQueue, name: str = None):
        pygame.display.set_caption("Caravan")
        self._renderer = renderer
        self._game_sprites = game_sprites
        self._event_queue = event_queue
        self._states = ['turn_change', 'hand_selection', 'caravan_placement']
        self._player_turn = True
        self.pl_name = name

    def start(self):
        while True:
            if self._handle_events() is False:
                if self.pl_name is not None:
                    player_data_repository.increment_player_losses(
                        self.pl_name)
                break

            self._render()

    def _handle_events(self):  # pylint: disable=inconsistent-return-statements # Order needed for if __name__=='__main__': tests to work
        for event in self._event_queue.get():
            if event.type == pygame.KEYDOWN:
                if self._states[0] == 'turn_change':
                    if event.key == pygame.K_SPACE:
                        self._game_sprites.player_turn = self._player_turn
                        self._states.append(self._states.pop(0))
                        self._game_sprites.player_selection = 0
                    # if event.key == pygame.K_ESCAPE:
                    #     return False
                elif self._states[0] == 'hand_selection':
                    self.handle_card_selection_event(event)

                elif self._states[0] == 'caravan_placement':
                    self.handle_caravan_selection_event(event)

            if self._states[0] == 'game_over':
                winner = 1
                if rules.is_player_winner(self._game_sprites.player,
                                          self._game_sprites.opponent) is False:
                    winner = 2

                if self.pl_name is not None:
                    if winner == 2:
                        player_data_repository.increment_player_losses(
                            self.pl_name)
                    else:
                        player_data_repository.increment_player_wins(
                            self.pl_name)

                self._renderer.winner = winner

            if event.type == pygame.QUIT:
                return False

    def handle_card_selection_event(self, event):
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

    def handle_caravan_selection_event(self, event):
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

    def try_placing_card(self):
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

# if __name__=='__main__':
#     display = pygame.display.set_mode((config.BOARD_WIDTH, config.BOARD_HEIGHT))
#     c_set = CardSet()
#     c_set.create_basic_set()
#     deck = Deck(c_set)
#     player = Player(deck)
#     c_set = CardSet()
#     c_set.create_basic_set()
#     deck = Deck(c_set)
#     opponent = Player(deck)
#     player.deck.shuffle()
#     player.deal_a_hand()
#     opponent.deck.shuffle()
#     opponent.deal_a_hand()
#     gs = GameSprites(display,player,opponent)
#     renderer = Renderer(display, gs)
#     event_queue = EventQueue()
#     gl = GameLoop(renderer,gs,event_queue)
#     gl.start()
