import unittest
import pygame
import config
from gameloop import GameLoop
from entities.cardset import CardSet
from entities.deck import Deck
from entities.player import Player
from entities.card import Card
from ui.gamesprites import GameSprites


class StubEvent:
    def __init__(self, event_type, key):
        self.type = event_type
        self.key = key


class StubEventQueue:
    def __init__(self, events):
        self._events = events

    def get(self):
        return self._events


class StubRenderer:
    def __init__(self) -> None:
        self.winner = 0

    def render(self):
        pass


class TestGameLoop(unittest.TestCase):
    def setUp(self):
        c_set = CardSet()
        c_set.create_basic_set()
        deck = Deck(c_set)
        self.player = Player(deck)
        c_set = CardSet()
        c_set.create_basic_set()
        deck = Deck(c_set)
        self.opponent = Player(deck)
        self.player.deck.shuffle()
        s10 = Card('sylly', 'Spades', 10, False)
        h9 = Card('sylly', 'Hearts', 9, False)
        h1 = Card('sylly', 'Hearts', 1, False)
        self.player.hand = [s10, h9, h1]
        self.opponent.deck.shuffle()
        s10 = Card('sylly', 'Spades', 10, False)
        h9 = Card('sylly', 'Hearts', 9, False)
        h1 = Card('sylly', 'Hearts', 1, False)
        self.opponent.hand = [s10, h9, h1]
        self.display = pygame.display.set_mode((1, 1))
        self.sprites = GameSprites(self.display, self.player, self.opponent)

    def test_player_turn_changes(self):
        events = [
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.QUIT, None)
        ]

        game_loop = GameLoop(
            StubRenderer(),
            self.sprites,
            StubEventQueue(events)
        )
        game_loop.npc_opponent = False
        game_loop.start()
        self.assertTrue(game_loop._player_turn)
        self.assertEqual(game_loop._game_sprites.player.caravans[0].value, 10)
        self.assertEqual(
            game_loop._game_sprites.opponent.caravans[0].value, 10)

    def test_player_card_actions(self):

        h10 = Card('sylly', 'Hearts', 10, False)
        h9 = Card('sylly', 'Hearts', 9, False)
        h2 = Card('sylly', 'Hearts', 2, False)
        h1 = Card('sylly', 'Hearts', 1, False)
        joker = Card('sylly', 'Red', 0, True)
        j = Card('sylly', 'Hearts', 11, True)
        self.sprites.player.caravans[0].insert_card(h10)
        self.sprites.player.caravans[1].insert_card(h9)
        self.sprites.player.caravans[2].insert_card(h2)
        self.sprites.player.caravans[0].insert_card(h1)
        self.sprites.player.hand = [joker, j]
        self.sprites.opponent.hand = [h10]
        events = [
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_LEFT),
            StubEvent(pygame.KEYDOWN, pygame.K_RIGHT),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_LEFT),
            StubEvent(pygame.KEYDOWN, pygame.K_RIGHT),
            StubEvent(pygame.KEYDOWN, pygame.K_UP),
            StubEvent(pygame.KEYDOWN, pygame.K_DOWN),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            # StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            # StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            # StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.QUIT, None)
        ]
        game_loop = GameLoop(
            StubRenderer(),
            self.sprites,
            StubEventQueue(events)
        )
        game_loop.npc_opponent = False
        game_loop.start()
        self.assertEqual(
            [c.value for c in game_loop._game_sprites.player.caravans], [1, 0, 0])
        events = [
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.QUIT, None)
        ]
        game_loop = GameLoop(
            StubRenderer(),
            game_loop._game_sprites,
            StubEventQueue(events)
        )
        game_loop.start()
        self.assertEqual(
            [c.value for c in game_loop._game_sprites.player.caravans], [0, 0, 0])

    def test_game_ending(self):
        s10 = Card('sylly', 'Spades', 10, False)
        h9 = Card('sylly', 'Hearts', 9, False)
        h2 = Card('sylly', 'Hearts', 2, False)
        self.sprites.player.caravans[0].cards = [s10, h9, h2]
        self.sprites.player.caravans[1].cards = [s10, h9, h2]
        self.sprites.player.caravans[2].cards = [s10, h9]
        self.sprites.player.hand = [h2]

        events = [
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_RIGHT),
            StubEvent(pygame.KEYDOWN, pygame.K_RIGHT),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.QUIT, None)
        ]

        game_loop = GameLoop(
            StubRenderer(),
            self.sprites,
            StubEventQueue(events)
        )
        game_loop.start()
        self.assertTrue(game_loop._states[0] == 'game_over')


    def test_discarding_caravans(self):
        s10 = Card('sylly', 'Spades', 10, False)
        h9 = Card('sylly', 'Hearts', 9, False)
        h2 = Card('sylly', 'Hearts', 2, False)
        self.sprites.player.caravans[0].cards = [s10, h9, h2]
        self.sprites.player.caravans[1].cards = [s10, h9, h2]
        self.sprites.player.caravans[2].cards = [s10, h9]
        self.sprites.player.hand = [h2]

        events = [
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_RIGHT),
            StubEvent(pygame.KEYDOWN, pygame.K_RIGHT),
            StubEvent(pygame.KEYDOWN, pygame.K_c),
            StubEvent(pygame.KEYDOWN, pygame.K_LEFT),
            StubEvent(pygame.KEYDOWN, pygame.K_e),
            StubEvent(pygame.KEYDOWN, pygame.K_ESCAPE),
            StubEvent(pygame.KEYDOWN, pygame.K_e),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_e),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_e),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.KEYDOWN, pygame.K_e),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE),
            StubEvent(pygame.QUIT, None)
        ]

        game_loop = GameLoop(
            StubRenderer(),
            self.sprites,
            StubEventQueue(events)
        )
        game_loop.npc_opponent = True
        game_loop.start()
        self.assertEqual([c.value for c in game_loop._game_sprites.player.caravans], [0, 0, 0])
