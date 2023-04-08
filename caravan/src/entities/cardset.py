import sys
import os
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, ".."))
from entities.card import Card  # pylint: disable=wrong-import-position # Order needed for if __name__=='__main__': tests to work


class CardSet:
    sets = ['sylly', 'minime453']
    values = range(1, 14)
    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

    def __init__(self) -> None:
        self.__set = []

    def create_set_from_all_cards(self):
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

    def add_card(self, card: Card):
        self.__set.append(card)

    def __str__(self) -> str:
        return str([str(c) for c in self.__set])

    def __len__(self) -> int:
        return len(self.__set)

    def get_cards(self):
        return self.__set.copy()

# if __name__=='__main__':
#     c_set = CardSet()
#     set.create_set_from_all_cards()
#     print(set)
