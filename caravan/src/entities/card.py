class Card:
    """Class that represents a classic playing card with value and suit.
    In addition there are couple of other attributes relevant to the Caravan game.

    Attributes:
        set: The set from which the card is from. In this game, a deck can consist of more than one 
             of the same value and suit cards, as long as they're from a different set. 
             This represents that detail.
        suit: Suit of the card, also listed in the class variable __suits 
              that has the ascii codes of the suits.
        value: Value of the card, from 0-13.
        special: Bool value that is False for number cards and 
                 True for Joker and the other picture cards.
        total: Cards value used in calculating a caravan's value. This can be doubled by kings.
    """
    __suits = {'Diamonds': '\u2666', 'Hearts': '\u2665',
               'Clubs': '\u2663', 'Spades': '\u2660'}

    def __init__(self, c_set: str, suit: str, value: int, special=False) -> None:
        self.set = c_set
        self.suit = suit
        self.value = value
        self.special = special
        if special:
            self.total = 0
        else:
            self.total = value

    def __str__(self) -> str:
        card_value = self.value
        if card_value == 0:
            return f"{self.suit}"
        if card_value == 1 or card_value > 10:
            specials = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}
            card_value = specials[card_value]

        return f"{card_value} of {Card.__suits[self.suit]}"

    def __copy__(self):
        crd_copy = Card(self.set, self.suit, self.value, self.special)
        crd_copy.total = self.total
        return crd_copy
