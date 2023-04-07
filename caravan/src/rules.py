import os, sys
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, ".."))
from entities.player import Player
from entities.card import Card
from entities.cardset import CardSet
from entities.deck import Deck

def check_if_legal_move(player: Player, opponent: Player, move: tuple):
    _, _, card = move
    if not all_own_caravans_started_or_card_going_to_own_unstarted_caravan(player,move):
        return (False,'You need to start all your caravans before placing cards elsewhere. Cards need to be either Ace or 2-10 value card.')
    if not putting_card_into_opponent_caravan(opponent,move):
        return (False,'Only special cards (Jack, Queen, King, Joker) can be placed in opponents caravan.')
    if not card.special and not using_number_card(move):
        return (False,'Illegal action for a number card.')
    if card.special and not using_special_card(move):
        return (False,'Special cards need to be placed on top of other cards.')
    return (True,'',)

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
    c_ord_desc = caravan.order_decending
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
        if c_ord_desc is None:
            return True
        if caravan.cards[-1].value == 12: #Queen determins the suit
            prev_suit = caravan.cards[-1].suit
        if prev_suit == card.suit:
            return True
        if c_ord_desc and prev_value <= card.value:
            return False
        if not c_ord_desc and prev_value >= card.value:
            return False
    return True

# def reverse_ordering(move):
#     caravan, _, card = move
#     c_ord_desc = caravan.order_decending
#     if len([c for c in caravan.cards if not c.special]) < 2:
#         return False
#     if card.value == 12:
#         return True
#     for crd in caravan.cards[::-1]:
#         if not crd.special:
#             prev_value = crd.value
#             prev_suit = crd.suit
#             break
#     if caravan.cards[-1].value == 12: #top Queen determins the suit
#         prev_suit = caravan.cards[-1].suit
#     if c_ord_desc and prev_value < card.value:
#         if prev_suit == card.suit:
#             return True
#     if not c_ord_desc and prev_value > card.value:
#         if prev_suit == card.suit:
#             return True
#     return False

def using_special_card(move):
    caravan, idx, card = move
    if idx == 0:
        return False
    if card.value == 12 and idx != -1: # Queen can only be placed on top of the caravan.
        return False
    if len(caravan.cards) == 0:
        return False
    return True

def get_cards_removed_by_jack(move):
    caravan, idx, card = move
    cards_to_remove = []
    if idx == -1:
        idx = len(caravan.cards) - 1
    for i in range(idx,-1,-1):
        cards_to_remove.append(caravan.cards[i])
        if not caravan.cards[i].special:
            break
    return cards_to_remove

def get_cards_removed_by_joker(player, opponent, move):
    caravan, idx, card = move
    cards_to_remove = []
    if idx == -1:
        idx = len(caravan.cards) - 1
    for i in range(idx,-1,-1):
        if not caravan.cards[i].special:
            protected = caravan.cards[i]
    remove_following_specials = False
    for gamer in [player,opponent]:
        for crvn in gamer.caravans:
            for crd in crvn.cards:
                if crd == protected:
                    remove_following_specials = False
                    continue
                if not crd.special:
                    remove_following_specials = False
                    # If protected card was Ace, remove all of the same suit
                    if protected.value == 1 and protected.suit == crd.suit:
                        cards_to_remove.append(crd)
                        remove_following_specials = True
                    # If protected card was any other number card, remove all of the same value
                    elif protected.value != 1 and protected.value == crd.value:
                        cards_to_remove.append(crd)
                        remove_following_specials = True
                elif remove_following_specials:
                    cards_to_remove.append(crd)
    return cards_to_remove

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
    # self.player.caravans[1].insert_card(-1, Card(None,'Hearts',12,True))
    # # self.player.caravans[1].order_decending *= -1
    # move = (player.caravans[0], -1, Card(None,'Hearts',9,False))
    # print(using_number_card(move))
    player.caravans[0].insert_card(-1,Card(None,'Hearts',2,False))
    player.caravans[0].insert_card(-1,Card(None,'Hearts',3,False))
    player.caravans[0].insert_card(-1,Card(None,'Hearts',12,True))
    player.caravans[0].insert_card(-1,Card(None,'Hearts',12,True))
    player.caravans[2].insert_card(-1,Card(None,'Hearts',2,False))
    opponent.caravans[1].insert_card(-1,Card(None,'Hearts',2,False))
    move = (player.caravans[0], -1, Card(None,'Spades',1,False))
    print(using_number_card(move))