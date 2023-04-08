import unittest
from entities.deck import Deck
from entities.cardset import CardSet
from entities.player import Player
from entities.card import Card


class TestPlayerEntity(unittest.TestCase):
    def setUp(self):
        c_set = CardSet()
        c_set.create_set_from_all_cards()
        deck = Deck(c_set)
        self.player = Player(deck)
        deck = Deck(c_set)
        self.player.deck.shuffle()
        self.player.deal_a_hand()

    def test_play_card(self):
        c1 = self.player.hand[-1]
        self.assertEqual(len(self.player.hand),8)
        c2 = self.player.play_card(-1)
        self.assertEqual(len(self.player.hand),7)
        self.assertEqual(c1,c2)
        self.player.play_card(-1)
        self.assertEqual(len(self.player.hand),6)
        self.player.play_card(-1)
        self.assertEqual(len(self.player.hand),5)
        self.player.play_card(-1)
        self.assertEqual(len(self.player.hand),5)
        self.player.deck.cards = []
        self.player.play_card(-1)
        self.assertEqual(len(self.player.hand),4)
        self.player.hand = []
        c = self.player.play_card(-1)
        self.assertEqual(c,None)
        

    def test_getting_hand_as_str(self):
        s1 = Card(None,'Spades',1,False)
        h5 = Card(None,'Hearts',5,False)
        dq = Card(None,'Diamonds',12,True)
        self.player.hand = [s1,h5,dq]
        self.assertEqual(self.player.get_hand_as_str(),['Ace of \u2660','5 of \u2665','Queen of \u2666'])

    def test_getting_caravans_as_str(self):
        s1 = Card(None,'Spades',1,False)
        h5 = Card(None,'Hearts',5,False)
        dq = Card(None,'Diamonds',12,True)
        self.player.caravans[0].insert_card(s1)
        self.player.caravans[1].insert_card(h5)
        crds = ['Ace of \u2660','5 of \u2665','']
        self.assertEqual(self.player.get_caravans_as_str(),
        f'{"Caravan 1:":15} {"Caravan 2:":15} {"Caravan 3:":15}\n{crds[0]:15} {crds[1]:15} {crds[2]:15}\n')
        