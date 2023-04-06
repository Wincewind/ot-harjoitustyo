from random import shuffle
import sys
import os

dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, ".."))
from entities.cardset import ( # pylint: disable=wrong-import-position # Order needed for if __name__=='__main__': tests to work
    CardSet,
)

class Deck:
    def __init__(self, cardset: CardSet) -> None:
        self.cards = []
        if len(cardset) < 30:
            raise ValueError(
                f"Caravan decks consist of at least 30 cards. Please add {30-len(cardset)} "+
                "more cards to the set."
            )
        else:
            self.cards = cardset.get_cards()

    def shuffle(self):
        shuffle(self.cards)

    def deal_cards(self, amount: int):
        new_cards = []
        while amount > 0 < len(self.cards):
            new_cards.append(self.cards.pop())
            amount -= 1
        return new_cards


# if __name__=='__main__':
#     cardset = CardSet()
#     cardset.create_set_from_all_cards()
#     deck = Deck(cardset)
#     deck.shuffle()
#     print(deck.cards[0])
#     print(cardset.get_cards()[0])
