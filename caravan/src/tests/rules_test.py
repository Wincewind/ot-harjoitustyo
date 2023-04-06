import unittest
from entities.deck import Deck
from entities.player import Player
from entities.cardset import CardSet
from entities.card import Card
import rules

class TestRules(unittest.TestCase):
    def setUp(self):
        c_set = CardSet()
        c_set.create_set_from_all_cards()
        deck = Deck(c_set)
        self.player = Player(deck)
        deck = Deck(c_set)
        self.opponent = Player(deck)
        self.player.deck.shuffle()
        self.player.deal_a_hand()
        self.opponent.deck.shuffle()
        self.opponent.deal_a_hand()


    def test_check_putting_card_into_wrong_deck_when_all_own_caravans_not_started(self):
        # Putting a card into opponents caravan when all your caravans are not started
        move = (self.opponent.caravans[2], 0,self.player.hand[0])
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],False)

        # Opponent puts card into your caravan when own not started
        move = (self.player.caravans[1], 0,self.opponent.hand[0])
        self.assertEqual(rules.check_if_legal_move(self.opponent,self.player,move)[0],False)

        # Putting a picture/special card into not started caravan
        move = (self.player.caravans[1], 0, Card(None,'Hearts',11,True))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],False)

        # Putting a card into a started caravan when all your caravans haven't been started
        self.player.caravans[0].insert_card(-1,Card(None,'Hearts',2,False))
        move = (self.player.caravans[0], 0, Card(None,'Hearts',3,False))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],False)
    
    def test_check_correct_caravan_starting(self):
        #Putting a number card into a not started caravan
        move = (self.player.caravans[0], 0, Card(None,'Hearts',2,False))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],True)

        #Putting a card into a started caravan when all your caravans have been started
        self.player.caravans[0].insert_card(-1,Card(None,'Hearts',2,False))
        self.player.caravans[1].insert_card(-1,Card(None,'Hearts',2,False))
        self.player.caravans[2].insert_card(-1,Card(None,'Hearts',2,False))
        self.opponent.caravans[1].insert_card(-1,Card(None,'Hearts',2,False))
        move = (self.opponent.caravans[1], 0, Card(None,'Hearts',11,True))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],True)
        move = (self.player.caravans[1], 0, Card(None,'Hearts',2,False))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],True)

    def test_putting_cards_into_opponent_caravan(self):
        #Putting a number card into opponent's caravan
        move = (self.opponent.caravans[0], 0, Card(None,'Hearts',2,False))
        self.assertEqual(rules.putting_card_into_opponent_caravan(self.opponent,move),False)

        #Putting a picture card into opponent's caravan
        self.opponent.caravans[0].insert_card(-1,Card(None,'Hearts',2,False))
        move = (self.opponent.caravans[0], 0, Card(None,'Hearts',12,True))
        self.assertEqual(rules.putting_card_into_opponent_caravan(self.opponent,move),True)

    def test_using_number_cards_correctly(self):
        # Add 2nd card
        self.player.caravans[0].insert_card(-1, Card(None,'Hearts',2,False))
        move = (self.player.caravans[0], -1, Card(None,'Hearts',3,False))
        self.assertEqual(rules.using_number_card(move),True)

        # Add 3rd card to a ascending caravan
        self.player.caravans[0].insert_card(-1, Card(None,'Hearts',3,False))
        move = (self.player.caravans[0], -1, Card(None,'Spades',7,False))
        self.assertEqual(rules.using_number_card(move),True)
        self.player.caravans[0].insert_card(-1, Card(None,'Spades',7,False))
        
        # Add a smaller card to asc car that is of the same suit
        move = (self.player.caravans[0], -1, Card(None,'Spades',3,False))
        self.assertEqual(rules.using_number_card(move),True)
        self.assertEqual(rules.reverse_ordering(move),True)

        # Add a higher card to asc car that is of the same suit
        self.player.caravans[1].insert_card(-1, Card(None,'Spades',7,False))
        self.player.caravans[1].insert_card(-1, Card(None,'Diamonds',5,False))
        self.player.caravans[1].insert_card(-1, Card(None,'Hearts',12,True))
        self.player.caravans[1].order_decending *= -1
        move = (self.player.caravans[1], -1, Card(None,'Hearts',9,False))
        self.assertEqual(rules.using_number_card(move),True)
        self.assertEqual(rules.reverse_ordering(move),True)

    def test_using_number_cards_incorrectly(self):
        # Add card of the same value
        self.player.caravans[0].insert_card(-1, Card(None,'Hearts',2,False))
        move = (self.player.caravans[0], -1, Card(None,'Hearts',2,False))
        self.assertEqual(rules.using_number_card(move),False)

        # Add a lower card to a ascending caravan
        self.player.caravans[0].insert_card(-1, Card(None,'Hearts',3,False))
        move = (self.player.caravans[0], -1, Card(None,'Spades',1,False))
        self.assertEqual(rules.using_number_card(move),False)
        #self.player.caravans[0].insert_card(-1, Card(None,'Spades',7,False))
        
        # Add a higher card to desc car
        self.player.caravans[1].insert_card(-1, Card(None,'Spades',7,False))
        self.player.caravans[1].insert_card(-1, Card(None,'Hearts',5,False))
        move = (self.player.caravans[1], -1, Card(None,'Spades',9,False))
        self.assertEqual(rules.using_number_card(move),False)

        
        #def test_using_number_cards_incorrectly(self):