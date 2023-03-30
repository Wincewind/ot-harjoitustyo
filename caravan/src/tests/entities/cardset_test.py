import unittest
from entities.cardset import CardSet

class TestCardSetEntity(unittest.TestCase):
    def setUp(self):
        self.cardset = CardSet()

    def test_create_set_from_all_cards(self):
        self.cardset.create_set_from_all_cards()
        self.assertEqual(len(self.cardset), len(CardSet.sets)*(len(CardSet.suits)*(len(CardSet.values))+2))