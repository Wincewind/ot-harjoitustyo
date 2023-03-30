from caravan import Caravan
from deck import Deck

class Player:
    def __init__(self, deck: Deck) -> None:
        self.caravans = (Caravan(),Caravan(),Caravan())
        self.deck = deck
        self.hand = []

    def deal_a_hand(self):
        self.hand = self.deck.deal_cards(8)
    
    def draw_card(self):
        new_card = self.deck.deal_cards(1)
        if len(new_card) != 0:
            self.hand.append(new_card[0])
            