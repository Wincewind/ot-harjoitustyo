import sys
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parents[0]))
from entities.caravan import Caravan
from entities.deck import Deck

class Player:
    def __init__(self, deck: Deck) -> None:
        self.caravans = (Caravan(),Caravan(),Caravan())
        self.deck = deck
        self.hand = []

    def deal_a_hand(self):
        self.hand = self.deck.deal_cards(8)

    def play_card(self,idx):
        if len(self.hand) == 0 or len(self.hand) < idx+1:
            return None
        c = self.hand.pop(idx)
        new_card = self.deck.deal_cards(1)
        if len(new_card) > 0:
            self.hand.insert(idx,new_card[0])
        return c 

    def get_hand_as_str(self):
        return [str(c) for c in self.hand] 