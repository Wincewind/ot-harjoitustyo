import unittest
from entities.deck import Deck
from entities.cardset import CardSet
from entities.card import Card

class TestCardSetEntity(unittest.TestCase):
    def setUp(self):
        self.cardset = CardSet()
        self.cardset.create_set_from_all_cards()

    def test_trying_to_create_deck_from_too_few_cards(self):
        cardset = CardSet()
        c = Card('test','Hearts',12)
        cardset.add_card(c)
        c = Card('test','Spades',12)
        cardset.add_card(c)
        self.assertRaises(ValueError, Deck, cardset)

    def test_dealing_one_card(self):
        deck = Deck(self.cardset)
        self.assertEqual(len(deck.deal_cards(1)),1)
        self.assertEqual(type(deck.deal_cards(1)[0]),Card)

    def test_dealing_several_cards(self):
        deck = Deck(self.cardset)
        self.assertEqual(len(deck.deal_cards(8)),8)

    def test_trying_to_deal_more_cards_than_there_are_in_the_deck(self):
        deck = Deck(self.cardset)
        deck.deal_cards(len(self.cardset)-5)
        self.assertEqual(len(deck.deal_cards(8)),5)

    def test_shuffle_deck(self):
        deck = Deck(self.cardset)
        deck.shuffle()
        print(deck.cards[0])
        print(self.cardset.get_cards()[0])
        self.assertNotEqual(deck.cards[0],self.cardset.get_cards()[0])