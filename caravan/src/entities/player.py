import sys
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parents[0]))
from entities.caravan import Caravan
from entities.deck import Deck
from entities.cardset import CardSet

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
    
    def get_caravans_as_str(self):
        s = f'{"Caravan 1:":15} {"Caravan 2:":15} {"Caravan 3:":15}\n'
        longest_caravan_len = len(max(self.caravans, key=lambda c: len(c.cards)).cards)
        for i in range(longest_caravan_len):
            card_info = []
            for c in self.caravans:
                if len(c.cards) <= i:
                    card_info.append('')
                else:
                    card_info.append(str(c.cards[i]))
            s += f'{card_info[0]:15} {card_info[1]:15} {card_info[2]:15}\n'
        return s
    
if __name__=='__main__':
    s = CardSet()
    s.create_set_from_all_cards()
    d = Deck(s)
    p = Player(d)
    p.deck.shuffle()
    p.deal_a_hand()
    p.caravans[0].insert_card(0,p.play_card(0))
    p.caravans[1].insert_card(0,p.play_card(0))
    p.caravans[2].insert_card(0,p.play_card(0))
    print(p.get_caravans_as_str())