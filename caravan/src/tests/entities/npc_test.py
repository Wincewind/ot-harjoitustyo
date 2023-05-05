import unittest
import copy
from entities.npc import Npc
from entities.deck import Deck
from entities.player import Player
from entities.cardset import CardSet
from entities.card import Card
import rules


class TestNpc(unittest.TestCase):
    def setUp(self):
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
        self.npc = Npc(player, opponent)

    def test_discarding_caravan(self):
        for c in self.npc._player.caravans:
            c.cards.insert(-1, Card('sylly', 'Hearts', 10, False))
            c.cards.insert(-1, Card('sylly', 'Hearts', 10, False))
            c.cards.insert(-1, Card('sylly', 'Hearts', 10, False))
        self.npc.perform_action()
        self.assertEqual(self.npc._player.caravans[0].cards, [])

    def test_playing_cards(self):
        for c in self.npc._player.caravans:
            c.insert_card(Card('sylly', 'Hearts', 10, False))
            c.insert_card(Card('sylly', 'Hearts', 9, False))
        h2 = Card('sylly', 'Hearts', 2, False)
        s4 = Card('sylly', 'Spades', 4, False)
        d3 = Card('sylly', 'Diamonds', 3, False)
        self.npc._player.hand = [h2, s4, d3]
        self.npc.perform_action()
        self.npc.perform_action()
        self.npc.perform_action()
        self.assertEqual(all(rules.check_if_caravan_ready(c.value)
                         for c in self.npc._player.caravans), True)
        self.assertEqual(self.npc._player.caravans[0].value, 21)
        self.assertEqual(self.npc._player.caravans[1].value, 23)
        self.assertEqual(self.npc._player.caravans[2].value, 22)


    def test_discarding_cards(self):
        for c in self.npc._player.caravans:
            c.insert_card(Card('sylly', 'Hearts', 10, False))
            c.insert_card(Card('sylly', 'Hearts', 9, False))
        self.npc._player.hand = [Card('sylly', 'Hearts', 9, False),
                                 Card('sylly', 'Hearts', 9, False)]
        self.npc.perform_action()
        self.assertEqual(all(c.value == 19 for c in self.npc._player.caravans),True)
        self.assertEqual(len([c for c in self.npc._player.hand if c.value == 9]),1)