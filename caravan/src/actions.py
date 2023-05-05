"""Module for the possible caravan game actions: playing a card, 
discarding a caravan or a card.
"""
import rules
from entities.player import Player


def play_card(player: Player, opponent: Player, move):
    """Place a card into a caravan.

    Args:
        player (Player): represents the one performing the action.

        opponent (Player): represents the opposing player during the action.

        move (tuple): tuple of (caravan,index,card): Caravan into 
        which the card object is being placed, 
        index at which the card is being placed at in the caravan. 
        The card object that's being placed.

    Returns:
        bool: False if the placement was illegal, otherwise True.
    """
    caravan = move[0]
    if not rules.check_if_legal_move(player, opponent, move)[0]:
        return False
    # print('crd to play',move[2])
    # print(player.get_hand_as_str())
    crd = player.play_card(player.hand.index(move[2]))
    if crd.special:
        cards_to_remove = []
        if crd.value == 11:
            cards_to_remove = rules.get_cards_removed_by_jack(move)
        elif crd.value == 0:
            cards_to_remove, protected = rules.get_cards_removed_by_joker(
                player, opponent, move)
        elif crd.value == 13:
            rules.double_total_with_king(move)
        for card in cards_to_remove:
            next(c for c in player.caravans +
                 opponent.caravans if card in c.cards).cards.remove(card)
    if crd.value != 11:
        idx = move[1]
        if crd.value == 0:
            idx = caravan.cards.index(protected)+1
        caravan.insert_card(crd, idx)
    return True


def discard_caravan(idx, player):
    """Discard one of the player's caravans, if it had cards.

    Args:
        idx (int): Index of the caravan.

        player (Player): Player object that has the caravans in its Player.caravans tuple attribute.

    Returns:
        bool: True if there were any cards to remove, else False.
    """
    if len(player.caravans[idx].cards) > 0:
        player.caravans[idx].cards = []
        return True
    return False


def discard_card(idx, player: Player):
    """Discard one of the cards in player's hand.

    Args:
        idx (int): Index of the card to be removed.

        player (Player): Player object whose Player.hand attribute the card is to be removed from.

    Returns:
        bool: True if all caravans had been started, there were any cards to remove and the index 
        was within that range of cards. Else False.
    """
    all_car_started = all(c.started for c in player.caravans)
    if all_car_started and len(player.hand) > 0 and idx in range(0, len(player.hand)-1):
        player.play_card(idx)
        return True
    return False
