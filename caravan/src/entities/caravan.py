import sys
import os
from entities.card import Card  # pylint: disable=wrong-import-position # Order needed for if __name__=='__main__': tests to work
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, ".."))

class Caravan:
    def __init__(self) -> None:
        self.cards = []
        self.started = False

    def insert_card(self, card: Card, idx=-1):
        # function call to check rules if a legal placement.
        if len(self.cards) == 0:
            self.started = True
        if idx == -1:
            self.cards.append(card)
        else:
            self.cards.insert(idx, card)

        # return info on what was inserted and where
    @property
    def value(self):
        return sum(c.total for c in self.cards)
    
    # Order is determined by the last 2 number cards in the caravan and is then flipped by each Queen on top of the last number card.
    @property
    def order_decending(self):
        order_desc = None
        number_cards = [c for c in self.cards if not c.special]
        if len(number_cards) < 2 or number_cards[-1].value == number_cards[-2]:
            return order_desc
        if number_cards[-1].value < number_cards[-2].value:
            order_desc = True
        else:
            order_desc = False
        for crd in self.cards[::-1]:
            if crd.value == 12:
                order_desc = not order_desc
            if not crd.special:
                break
        return order_desc

    def __str__(self) -> str:
        return ''.join(f'{str(c)}\n' for c in self.cards)