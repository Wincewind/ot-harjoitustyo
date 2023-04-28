import unittest
from entities.player_data import PlayerData
from entities.cardset import CardSet
from entities.card import Card

class TestCardSetEntity(unittest.TestCase):
    def setUp(self):
        self.p_data = PlayerData('test',0,0,0,CardSet.sets)

    def test_preparing_player_with_one_set(self):
        player = self.p_data.prepare_player(CardSet.sets[0])
        self.assertEqual(len(player.deck.cards),46)

    def test_preparing_player_with_all_sets(self):
        player = self.p_data.prepare_player('ALL')
        self.assertEqual(len(player.deck.cards),100)