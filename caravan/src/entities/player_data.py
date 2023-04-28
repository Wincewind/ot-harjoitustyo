from entities.cardset import CardSet
from entities.player import Player
from entities.deck import Deck


class PlayerData:
    def __init__(self, name: str, wins: int, losses: int, row_number: int, card_sets: list) -> None:
        self.name = name
        self.wins = wins
        self.losses = losses
        self.card_sets = card_sets
        self._row_number = row_number

    def prepare_player(self, set_name: str):
        c_set = CardSet()
        if set_name.lower() == 'all':
            c_set.create_set_from_all_cards()
        else:
            c_set.create_basic_set(set_name)
        deck = Deck(c_set)
        player = Player(deck)
        player.deck.shuffle()
        player.deal_a_hand()
        return player
