import os, sys
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, ".."))
from entities.player import Player
from entities.card import Card
from entities.cardset import CardSet
from entities.deck import Deck

def check_if_legal_move(player: Player, opponent: Player, move: tuple):
    caravan, idx, card = move
    reverse_order = False
    if not all_own_caravans_started_or_card_going_to_own_unstarted_caravan(player,move):
        return (False,'You need to start all your caravans before placing cards elsewhere. Cards need to be either Ace or 2-10 value card.')
    if not putting_card_into_opponent_caravan(opponent,move):
        return (False,'Only special cards (Jack, Queen, King, Joker) can be placed in opponents caravan.')
    
    return (True,'',reverse_order)

def all_own_caravans_started_or_card_going_to_own_unstarted_caravan(player, move) -> bool:
    caravan, _, card = move
    if not all(c.started for c in player.caravans):
        if caravan not in player.caravans:
            return False
        if caravan.started:
            return False
        if not card.value in range(1,11):
            return False
    return True

def putting_card_into_opponent_caravan(opponent,move):
    caravan, _, card = move
    if caravan in opponent.caravans and not card.special:
        return False
    return True

def using_number_card(move):
    caravan, idx, card = move
    if not card.value in range(1,11):
        return False
    if idx != -1:
        return False
    if len(caravan.cards) > 0:
        for crd in caravan.cards[::-1]:
            if not crd.special:
                prev_value = crd.value
                prev_suit = crd.suit
                break
        if prev_value == card.value:
            return False
        if caravan.order_decending is None:
            return True
        if caravan.cards[-1].value == 12: #Queen determins the suit
            prev_suit = caravan.cards[-1].suit
        if prev_suit == card.suit:
            return True
        if caravan.order_decending and prev_value <= card.value:
            return False
        if not caravan.order_decending and prev_value >= card.value:
            return False
    return True

def reverse_ordering(move):
    caravan, _, card = move
    if len([c for c in caravan.cards if not c.special]) < 2:
        return False
    if card.value == 12:
        return True
    for crd in caravan.cards[::-1]:
        if not crd.special:
            prev_value = crd.value
            prev_suit = crd.suit
            break
    if caravan.cards[-1].value == 12: #top Queen determins the suit
        prev_suit = caravan.cards[-1].suit
    if caravan.order_decending and prev_value < card.value:
        if prev_suit == card.suit:
            return True
    if not caravan.order_decending and prev_value > card.value:
        if prev_suit == card.suit:
            return True
    return False

def using_special_card(move):
    caravan, idx, card = move
    if idx == 0:
        return False
    if len(caravan.cards) == 0:
        return False
    # more checks
    return True


if __name__=='__main__':
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
    
    
    # player.caravans[1].insert_card(-1, Card(None,'Spades',7,False))
    # player.caravans[1].insert_card(-1, Card(None,'Diamonds',5,False))
    # # self.player.caravans[1].insert_card(-1, Card(None,'Hearts',12,True))
    # # self.player.caravans[1].order_decending *= -1
    # move = (player.caravans[0], -1, Card(None,'Hearts',9,False))
    # print(using_number_card(move))

    
    # # player.caravans[0].insert_card(-1, Card(None,'Hearts',7,False))
    # # move = (player.caravans[0], -1, Card(None,'Hearts',3,False))
    # # using_number_card(move)

    # # player.caravans[0].insert_card(-1, Card(None,'Hearts',5,False))
    # # move = (player.caravans[0], -1, Card(None,'Hearts',7,False))
    # # print(using_number_card(move))
    # print(reverse_ordering(move))
    # move = (player.caravans[2], 0, Card(None,'Hearts',2,True))
    # print(__all_own_caravans_started_or_card_going_to_own_unstarted_caravan(player,move))