import copy
from random import shuffle
from entities.cardset import CardSet


class Deck:
    """Class representing a deck of playing cards.

    Attributes:
        cards: list of the cards currently in the deck.
        __cardset: Used to make a copy of the deck.
    """

    def __init__(self, cardset: CardSet) -> None:
        self.cards = []
        if len(cardset) < 30:
            raise ValueError(
                f"Caravan decks consist of at least 30 cards. Please add {30-len(cardset)} " +
                "more cards to the set."
            )
        self.__cardset = cardset
        self.cards = cardset.get_cards()

    def shuffle(self):
        """Shuffles the deck using random.shuffle function.
        """
        shuffle(self.cards)

    def deal_cards(self, amount: int):
        """Deal a given amount of cards from the deck.

        Args:
            amount (int): Amount of cards to deal. 
            If the amount exceeds the remaining cards, 
            only the available amount of cards are returned. 
            If the deck is empty, an empty list is returned.

        Returns:
            list: List of card objects.
        """
        new_cards = []
        while amount > 0 < len(self.cards):
            new_cards.append(self.cards.pop())
            amount -= 1
        return new_cards

    def __copy__(self):
        deck = Deck(self.__cardset)
        deck.cards = [copy.copy(c) for c in self.cards]
        return deck
