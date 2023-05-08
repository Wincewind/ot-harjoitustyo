from entities.cardset import CardSet
from entities.player import Player
from entities.deck import Deck


class PlayerData:
    """Class representing a users player data.

    Attributes:
        name: Name of the player.
        wins: Number of wins.
        losses: Number of losses.
        card_sets: A collection of card sets to be picked from when creating a deck.
        row_number: row number, related to the save slot when selecting the user data.
    """

    def __init__(self, name: str, wins: int, losses: int, row_number: int, card_sets: list) -> None:
        self.name = name
        self.wins = wins
        self.losses = losses
        self.card_sets = card_sets
        self.row_number = row_number

    def prepare_player(self, set_name: str):
        """Used to prepare a Player object.

        Args:
            set_name (str): Name of the card set to be 
            used in creating the player's deck. If 'all' is given as input,
            deck is created from all available card sets.

        Returns:
            Player: A Player object with deck built, shuffled and hand dealt.
        """
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
