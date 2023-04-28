import pygame
import config
import gameloop
from entities.cardset import CardSet
from entities.deck import Deck
from entities.player import Player
from entities.player_data import PlayerData
from ui.eventqueue import EventQueue
from ui.renderer import Renderer
from ui.gamesprites import GameSprites
from ui.text.game_interface import GameInterface
from ui.save_selection import SaveSelection
from ui.deck_creation import DeckCreation

# def third_week_demo():
#     c_set = CardSet()
#     c_set.create_set_from_all_cards()
#     deck = Deck(c_set)
#     player = Player(deck)
#     player.deck.shuffle()
#     player.deal_a_hand()
#     i = 0
#     while True:
#         c_idx = parse_idx_input_or_quit(
#             player,
#             'Choose one of your Caravans. Input index [0-2] or quit by typing "quit":',
#             0,
#             2,
#         )
#         if c_idx == "quit":
#             break
#         idx = parse_idx_input_or_quit(
#             player,
#             f'Which card to add to Caravan {c_idx}? Input index [0-7] or quit by typing "quit":',
#             0,
#             7,
#         )
#         if idx == "quit":
#             break
#         crd = player.play_card(idx)
#         if crd is None:
#             break
#         player.caravans[c_idx].insert_card(crd, i)
#         i += 1


def fourth_week_demo():
    game_int = GameInterface()
    game_int.game_setup()
    game_int.game_loop()


def fifth_week_demo():
    display = pygame.display.set_mode(
        (config.BOARD_WIDTH, config.BOARD_HEIGHT))
    c_set = CardSet()
    c_set.create_basic_set()
    deck = Deck(c_set)
    player = Player(deck)
    c_set = CardSet()
    c_set.create_basic_set()
    deck = Deck(c_set)
    opponent = Player(deck)
    player.deck.shuffle()
    player.deal_a_hand()
    opponent.deck.shuffle()
    opponent.deal_a_hand()
    game_sprites = GameSprites(display, player, opponent)
    renderer = Renderer(display, game_sprites)
    event_queue = EventQueue()
    game_loop = gameloop.GameLoop(renderer, game_sprites, event_queue)
    game_loop.start()


def sixth_week_demo():
    display = pygame.display.set_mode(
        (config.BOARD_WIDTH, config.BOARD_HEIGHT))
    event_queue = EventQueue()
    save_screen = SaveSelection(display, event_queue)
    pl_data = save_screen.main_loop()
    if pl_data is not None:
        deck_creation = DeckCreation(display, event_queue, pl_data)
        player = deck_creation.main_loop()
        if player is not None:
            opponent_data = PlayerData('Opponent',0,0,-1,[CardSet.sets[0]])
            opponent = opponent_data.prepare_player(CardSet.sets[0])
            game_sprites = GameSprites(display, player, opponent)
            renderer = Renderer(display, game_sprites)
            game_loop = gameloop.GameLoop(
                renderer, game_sprites, event_queue, pl_data.name)
            game_loop.start()


if __name__ == "__main__":
    # third_week_demo()
    # fourth_week_demo()
    # fifth_week_demo()
    sixth_week_demo()
