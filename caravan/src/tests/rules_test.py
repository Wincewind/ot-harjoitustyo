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
        self.player.caravans[0].insert_card(Card(None,'Hearts',2,False))
        move = (self.player.caravans[0], 0, Card(None,'Hearts',3,False))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],False)
    
    def test_check_correct_caravan_starting(self):
        #Putting a number card into a not started caravan
        move = (self.player.caravans[0], -1, Card(None,'Hearts',2,False))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move),(True,''))

        #Putting a card into a started caravan when all your caravans have been started
        self.player.caravans[0].insert_card(Card(None,'Hearts',2,False))
        self.player.caravans[1].insert_card(Card(None,'Hearts',2,False))
        self.player.caravans[2].insert_card(Card(None,'Hearts',2,False))
        self.opponent.caravans[1].insert_card(Card(None,'Hearts',2,False))
        move = (self.opponent.caravans[1], -1, Card(None,'Hearts',11,True))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],True)
        move = (self.player.caravans[1], -1, Card(None,'Hearts',3,False))
        self.assertEqual(rules.check_if_legal_move(self.player,self.opponent,move)[0],True)

    def test_putting_cards_into_opponent_caravan(self):
        #Putting a number card into opponent's caravan
        move = (self.opponent.caravans[0], 0, Card(None,'Hearts',2,False))
        self.assertEqual(rules.putting_card_into_opponent_caravan(self.opponent,move),False)

        #Putting a picture card into opponent's caravan
        self.opponent.caravans[0].insert_card(Card(None,'Hearts',2,False))
        move = (self.opponent.caravans[0], 0, Card(None,'Hearts',12,True))
        self.assertEqual(rules.putting_card_into_opponent_caravan(self.opponent,move),True)

    def test_using_number_cards_correctly(self):
        # Add 2nd card
        self.player.caravans[0].insert_card(Card(None,'Hearts',2,False))
        move = (self.player.caravans[0], -1, Card(None,'Hearts',3,False))
        self.assertEqual(rules.using_number_card(move),True)

        # Add 3rd card to a ascending caravan
        self.player.caravans[0].insert_card(Card(None,'Hearts',3,False))
        move = (self.player.caravans[0], -1, Card(None,'Spades',7,False))
        self.assertEqual(rules.using_number_card(move),True)
        self.player.caravans[0].insert_card(Card(None,'Spades',7,False))
        
        # Add a smaller card to asc car that is of the same suit
        move = (self.player.caravans[0], -1, Card(None,'Spades',3,False))
        self.assertEqual(rules.using_number_card(move),True)
        #self.assertEqual(rules.reverse_ordering(move),True)

        # Add a higher card to desc car that is of the same suit
        self.player.caravans[1].insert_card(Card(None,'Spades',7,False))
        self.player.caravans[1].insert_card(Card(None,'Diamonds',5,False))
        self.player.caravans[1].insert_card(Card(None,'Spades',12,True))
        self.player.caravans[1].insert_card(Card(None,'Hearts',12,True))
        move = (self.player.caravans[1], -1, Card(None,'Hearts',9,False))
        self.assertEqual(rules.using_number_card(move),True)
        #self.assertEqual(rules.reverse_ordering(move),True)

    def test_using_number_cards_incorrectly(self):
        # Add card of the same value
        self.player.caravans[0].insert_card(Card(None,'Hearts',2,False))
        move = (self.player.caravans[0], -1, Card(None,'Hearts',2,False))
        self.assertEqual(rules.using_number_card(move),False)

        # Add a lower card to a ascending caravan
        self.player.caravans[0].insert_card(Card(None,'Hearts',3,False))
        move = (self.player.caravans[0], -1, Card(None,'Spades',1,False))
        self.assertEqual(rules.using_number_card(move),False)
        #self.player.caravans[0].insert_card(-1, Card(None,'Spades',7,False))
        
        # Add a higher card to desc car
        self.player.caravans[1].insert_card(Card(None,'Spades',7,False))
        self.player.caravans[1].insert_card(Card(None,'Hearts',5,False))
        move = (self.player.caravans[1], -1, Card(None,'Spades',9,False))
        self.assertEqual(rules.using_number_card(move),False)

    def test_placing_pic_cards(self):
        self.player.caravans[0].insert_card(Card(None,'Spades',7,False))
        self.player.caravans[0].insert_card(Card(None,'Hearts',5,False))

        # Jack
        move = (self.player.caravans[0], -1, Card(None,'Spades',11,True))
        self.assertEqual(rules.using_special_card(move),True)

        # Queen
        move = (self.player.caravans[0], -1, Card(None,'Spades',12,True))
        self.assertEqual(rules.using_special_card(move),True)
        move = (self.player.caravans[0], 2, Card(None,'Spades',12,True))
        self.assertEqual(rules.using_special_card(move),False)

        # King
        move = (self.player.caravans[0], 1, Card(None,'Spades',13,True))
        self.assertEqual(rules.using_special_card(move),True)

        # Joker
        move = (self.player.caravans[0], -1, Card(None,'Red',0,True))
        self.assertEqual(rules.using_special_card(move),True)

    def test_jack_effect(self):
        c1 = Card(None,'Spades',7,False)
        c2 = Card(None,'Hearts',5,False)
        c3 = Card(None,'Red',0,True)
        c4 = Card(None,'Diamonds',12,True)
        c5 = Card(None,'Spades',13,True)
        self.opponent.caravans[0].insert_card(c1)
        self.opponent.caravans[0].insert_card(c2)
        self.opponent.caravans[0].insert_card(c3)
        self.opponent.caravans[0].insert_card(c4)
        self.opponent.caravans[0].insert_card(c5)
        move = (self.opponent.caravans[0], -1, Card(None,'Spades',11,True))
        self.assertEqual(rules.get_cards_removed_by_jack(move),[c5,c4,c3,c2])
        move = (self.opponent.caravans[0], 0, Card(None,'Spades',11,True))
        self.assertEqual(rules.get_cards_removed_by_jack(move),[c1])


    def test_joker_effect(self):
        s1 = Card(None,'Spades',1,False)
        s2 = Card(None,'Spades',2,False)
        s3 = Card(None,'Spades',3,False)
        s4 = Card(None,'Spades',4,False)
        s5 = Card(None,'Spades',5,False)
        h2 = Card(None,'Hearts',2,False)
        h21 = Card(None,'Hearts',2,False)
        d2 = Card(None,'Diamonds',2,False)
        sq = Card(None,'Spades',12,True)
        hk = Card(None,'Hearts',13,True)
        self.opponent.caravans[0].insert_card(s1)
        self.opponent.caravans[1].insert_card(s2)
        self.opponent.caravans[1].insert_card(sq)
        self.opponent.caravans[2].insert_card(s3)
        self.opponent.caravans[0].insert_card(d2)
        self.player.caravans[0].insert_card(s4)
        self.player.caravans[2].insert_card(h2)
        self.player.caravans[2].insert_card(hk)
        self.opponent.caravans[1].insert_card(h21)
        self.player.caravans[2].insert_card(s5)
        move = (self.opponent.caravans[0], -1, Card(None,'Red',0,True))
        self.assertEqual(set(rules.get_cards_removed_by_joker(self.player,self.opponent,move)),{s2,s3,s4,s5,sq})
        move = (self.player.caravans[2], 0, Card(None,'Red',0,True))
        self.assertEqual(set(rules.get_cards_removed_by_joker(self.player,self.opponent,move)),{s2,d2,h21,sq})
