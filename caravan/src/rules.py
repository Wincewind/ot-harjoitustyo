"""Module for functions that check for the Caravan card game rules and 
effects of special cards given the current state of players' caravans."""
from entities.player import Player

CARAVAN_MIN = 21
CARAVAN_MAX = 26


def check_if_caravan_ready(car_val: int):
    """Check if caravan is ready to be sold.

    Args:
        car_val (int): The total value of a caravan's cards.

    Returns:
        bool: True if car_val is within range 21-26, else False.
    """
    return CARAVAN_MIN <= car_val <= CARAVAN_MAX


def check_if_caravan_sold(car_val: int, opposing_car_val: int):
    """Check if your caravan is ready and higher value than the opposing caravan.

    Args:
        car_val (int): Your caravan's value.

        opposing_car_val (int): Opponent's opposing caravan's value.

    Returns:
        bool: True if car_val is ready to be sold and higher in value than a ready opposing_car_val. 
        Else False.
    """
    if check_if_caravan_ready(car_val):
        if not check_if_caravan_ready(opposing_car_val):
            return True
        if car_val > opposing_car_val:
            return True
    return False


def check_if_legal_move(player: Player, opponent: Player, move: tuple):
    """General function to check if a action to be performed is legal according to the game rules.

    Args:
        player (Player): represents the one performing the action.

        opponent (Player): represents the opposing player during the action.

        move (tuple): tuple of (caravan,index,card): Caravan into 
        which the card object is being placed, 
        index at which the card is being placed at in the caravan. 
        The card object that's being placed.

    Returns:
        tuple(bool,str): A tuple of bool and str. False if 
        the move was illegal and a message explaining why. 
        True if the move is legal and an empty string.
    """
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
    """Check for caravan started statuses.

    Args:
        player (PLayer): Player object represents the one performing the action.
        move (tuple): tuple of (caravan,index,card), see 
        check_if_legal_move for more thorough description.

    Returns:
        bool: True if all caravans started or the card used is a number card on a 
        caravan that isn't started and the player owns. Else False.
    """
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
    """Check if a card is being placed in opponent's caravan and if the card is suited for that.
    """
    caravan, _, card = move
    if caravan in opponent.caravans and not card.special:
        return False
    return True


def using_number_card(move):
    """Check if the action performed is legal for a number card.
    """
    caravan, idx, card = move
    c_ord_desc = caravan.order_descending
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
        # If Queen is the top most card in caravan, it determins the suit.
        if caravan.cards[-1].value == 12:
            prev_suit = caravan.cards[-1].suit
        if legal_move and prev_suit == card.suit:
            return legal_move
        if c_ord_desc and prev_value <= card.value:
            legal_move = False
        if not c_ord_desc and prev_value >= card.value:
            legal_move = False
    return legal_move


def using_special_card(move):
    """Check if the action is legal for a special card (Jack, Queen, King, Joker).
    """
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
    """Get the cards that jack would remove from a caravan with the given action.

    Args:
        move (tuple): tuple of (caravan,index,card), see 
        check_if_legal_move for more thorough description.

    Returns:
        list: A list of card objects that should be removed, if the action were to be performed.
    """
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


def get_cards_removed_by_joker(player, opponent, move):
    """Get the cards that joker would remove from a caravan with the given action.

    Args:
        player (Player): represents the one performing the action.

        opponent (Player): represents the opposing player during the action.

        move (tuple): tuple of (caravan,index,card), see 
        check_if_legal_move for more thorough description.

    Returns:
        list: A list of card objects that should be removed, 
        if the action were to be performed and the card object, that joker is 
        to be placed upon, which is protected from removal.
    """
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
    """Find the next number card in the caravan and double its total.
    This function is to be refactored into the actions module.

    Args:
        move (tuple): tuple of (caravan,index,card), 
        see check_if_legal_move for more thorough description.
    """
    caravan, idx, _ = move
    if idx == -1:
        idx = len(caravan.cards) - 1
    for i in range(idx-1, -1, -1):
        if not caravan.cards[i].special:
            caravan.cards[i].total *= 2
            break


def is_player_winner(player, opponent):
    """Check if the player or opponent has won.

    Args:
        player (Player): Player in turn when the check is performed.
        opponent (Player): The opposing player when the check is performed.

    Returns:
        nullable bool: None if neither is a winner, 
        True if the player is and False if it's the opponent.
    """
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
