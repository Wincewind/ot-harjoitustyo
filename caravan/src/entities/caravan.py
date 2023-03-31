import sys
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parents[0]))
from entities.card import Card

class Caravan:
    def __init__(self) -> None:
        self.cards = []
        self.order_decending = True
    
    def insert_card(self,idx: int, card: Card):
        #function call to check rules if a legal placement.

        if len(self.cards) == 1:
            if self.cards[0].value > card.value:
                self.order_decending = True
            else:
                self.order_decending = False
        self.cards.insert(idx,card)

        #return info on what was inserted and where
    @property
    def value(self):
        return sum([c.value for c in self.cards])

    def __str__(self) -> str:
        return ''.join(f'{str(c)}\n' for c in self.cards)
    