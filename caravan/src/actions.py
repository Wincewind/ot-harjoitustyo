import rules


def play_card(player, opponent, move):
    caravan = move[0]
    if not rules.check_if_legal_move(player, opponent, move)[0]:
        return False
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
            # caravan.cards.remove(card)
    if crd.value != 11:
        idx = move[1]
        if crd.value == 0:
            idx = caravan.cards.index(protected)+1
        caravan.insert_card(crd, idx)
    return True


def discard_caravan(idx, player):
    if len(player.caravans[idx].cards) > 0:
        player.caravans[idx].cards = []
        return True
    return False


def discard_card(idx, player):
    if len(player.hand) > 0 and idx in range(0, len(player.hand)-1):
        player.hand.pop(idx)
        return True
    return False
