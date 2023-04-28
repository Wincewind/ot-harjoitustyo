from entities.card import Card
from config import AVAILABLE_CARDSETS


class CardSet:
    """Class representing a set of cards, used to 
    build a collection of card objects to be then used in a deck.

    Attributes:
        __set: A list into which a collection of cards is built.
    """
    sets = AVAILABLE_CARDSETS
    values = range(1, 14)
    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

    def __init__(self) -> None:
        self.__set = []

    def create_set_from_all_cards(self):
        """Creates a set from all available sets of cards.
        """
        self.__set = []
        for c_set in CardSet.sets:
            for suit in CardSet.suits:
                for value in CardSet.values:
                    special = False
                    if value > 10:
                        special = True
                    self.__set.append(Card(c_set, suit, value, special))
            self.__set.append(Card(c_set, 'Black Joker', 0, True))
            self.__set.append(Card(c_set, 'Red Joker', 0, True))

    def create_basic_set(self, set_name=sets[0]):
        """Creates a set of cards using only one set.

        Args:
            set_name (str, optional): set name to be used in the set creation.
            The first available set from configurations is used if none is given.
        """
        self.__set = []
        for suit in CardSet.suits:
            for value in CardSet.values:
                special = False
                if value > 10:
                    special = True
                self.__set.append(Card(set_name, suit, value, special))
        self.__set.append(Card(set_name, 'Black Joker', 0, True))
        self.__set.append(Card(set_name, 'Red Joker', 0, True))

    def add_card(self, card: Card):
        """Add a single card object into the set.

        Args:
            card (Card): a card object.
        """
        self.__set.append(card)

    def __str__(self) -> str:
        return str([str(c) for c in self.__set])

    def __len__(self) -> int:
        return len(self.__set)

    def get_cards(self):
        """Get the created set of cards as a list.

        Returns:
            list: List of the cards objects used in set creation.
        """
        return self.__set.copy()
