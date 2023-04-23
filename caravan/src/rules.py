from entities.player import Player

CARAVAN_MIN = 21
CARAVAN_MAX = 26


def check_if_caravan_ready(car_val: int):
    return CARAVAN_MIN <= car_val <= CARAVAN_MAX


def check_if_caravan_sold(car_val: int, opposing_car_val: int):
    if check_if_caravan_ready(car_val):
        if not check_if_caravan_ready(opposing_car_val):
            return True
        if car_val > opposing_car_val:
            return True
    return False


def check_if_legal_move(player: Player, opponent: Player, move: tuple):
    _, _, card = move
    if not all_own_caravans_started_or_card_going_to_own_unstarted_caravan(player, move):
        return (False, 'You need to start all your caravans before placing cards elsewhere. ' +
                'Cards need to be either Ace or 2-10 value card.')
    if not putting_card_into_opponent_caravan(opponent, move):
        return (False, 'Only special cards (Jack, Queen, King, Joker) ' +
                'can be placed in opponents caravan.')
    if not card.special and not using_number_card(move):
        return (False, 'Illegal action for a number card.')
    if card.special and not using_special_card(move):
        return (False, 'Special cards need to be placed on top of other cards.')
    return (True, '',)


def all_own_caravans_started_or_card_going_to_own_unstarted_caravan(player, move) -> bool:
    caravan, _, card = move
    if not all(c.started for c in player.caravans):
        if caravan not in player.caravans:
            return False
        if caravan.started:
            return False
        if not card.value in range(1, 11):
            return False
    return True


def putting_card_into_opponent_caravan(opponent, move):
    caravan, _, card = move
    if caravan in opponent.caravans and not card.special:
        return False
    return True


def using_number_card(move):
    caravan, idx, card = move
    c_ord_desc = caravan.order_decending
    legal_move = True
    if idx <= len(caravan.cards)-1 and idx != -1:
        legal_move = False
    if len(caravan.cards) > 0:
        crd = next(c for c in caravan.cards[::-1] if not c.special)
        prev_value = crd.value
        prev_suit = crd.suit
        if prev_value == card.value:
            legal_move = False
        if legal_move and c_ord_desc is None:
            return legal_move
        if caravan.cards[-1].value == 12:  # Queen determins the suit
            prev_suit = caravan.cards[-1].suit
        if legal_move and prev_suit == card.suit:
            return legal_move
        if c_ord_desc and prev_value <= card.value:
            legal_move = False
        if not c_ord_desc and prev_value >= card.value:
            legal_move = False
    return legal_move


def using_special_card(move):
    caravan, idx, card = move
    # Queen can only be placed on top of the caravan.
    if idx == len(caravan.cards):
        idx = -1
    if card.value == 12 and idx != -1:
        return False
    # Can't place picture card into an empty caravan.
    if len(caravan.cards) == 0 or idx == 0:
        return False
    # To make sure that other specials are removed,
    # jack or joker can't be placed in between special and number cards.
    if card.value in [11, 0] and idx != -1:
        if caravan.cards[idx].special:
            return False
    return True


def get_cards_removed_by_jack(move):
    caravan, idx, _ = move
    cards_to_remove = []
    if idx == -1:
        idx = len(caravan.cards) - 1
    for i in range(idx-1, -1, -1):
        cards_to_remove.append(caravan.cards[i])
        if not caravan.cards[i].special:
            break
    return cards_to_remove


def _find_cards_to_remove(player, opponent, protected):
    cards_to_remove = []
    remove_following_specials = False
    for crvn in player.caravans + opponent.caravans:
        for crd in crvn.cards:
            if crd == protected:  # and crvn == caravan:
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


def get_cards_removed_by_joker(player, opponent, move):
    caravan, idx, _ = move
    if idx == -1:
        idx = len(caravan.cards) - 1
    for i in range(idx-1, -1, -1):
        if not caravan.cards[i].special:
            protected = caravan.cards[i]
            break
    cards_to_remove = _find_cards_to_remove(player, opponent, protected)
    return (cards_to_remove, protected)


def double_total_with_king(move):
    caravan, idx, _ = move
    if idx == -1:
        idx = len(caravan.cards) - 1
    for i in range(idx-1, -1, -1):
        if not caravan.cards[i].special:
            caravan.cards[i].total *= 2
            break


def is_player_winner(player, opponent):
    pcv = [c.value if CARAVAN_MIN <= c.value <= CARAVAN_MAX else
           -float('inf') for c in player.caravans]
    ocv = [c.value if CARAVAN_MIN <= c.value <= CARAVAN_MAX else
           -float('inf') for c in opponent.caravans]
    if sum(pcv) < 0 > sum(ocv):
        return None
    winning_caravans = 0
    for i in range(3):
        if pcv[i] > ocv[i]:
            winning_caravans += 1
        elif pcv[i] < ocv[i]:
            winning_caravans -= 1
    if winning_caravans == 0:
        return None
    if winning_caravans > 0:
        return True
    return False

# if __name__=='__main__':
    # c_set = CardSet()
    # c_set.create_set_from_all_cards()
    # deck = Deck(c_set)
    # player = Player(deck)
    # deck = Deck(c_set)
    # opponent = Player(deck)
    # player.deck.shuffle()
    # player.deal_a_hand()
    # opponent.deck.shuffle()
    # opponent.deal_a_hand()

    # player.caravans[1].insert_card(-1, Card(None,'Spades',7,False))
    # player.caravans[1].insert_card(-1, Card(None,'Diamonds',5,False))
    # self.player.caravans[1].insert_card(-1, Card(None,'Hearts',12,True))
    # # self.player.caravans[1].order_decending *= -1
    # move = (player.caravans[0], -1, Card(None,'Hearts',9,False))
    # # print(using_number_card(move))
    # player.caravans[0].insert_card(-1,Card(None,'Hearts',2,False))
    # player.caravans[0].insert_card(-1,Card(None,'Hearts',3,False))
    # player.caravans[0].insert_card(-1,Card(None,'Hearts',12,True))
    # player.caravans[0].insert_card(-1,Card(None,'Hearts',12,True))
    # player.caravans[2].insert_card(-1,Card(None,'Hearts',2,False))
    # opponent.caravans[1].insert_card(-1,Card(None,'Hearts',2,False))
    # move = (player.caravans[0], -1, Card(None,'Spades',1,False))
    # print(using_number_card(move))
