from entities.cardset import CardSet  # pylint: disable=wrong-import-position
from entities.deck import Deck  # pylint: disable=wrong-import-position
from entities.caravan import Caravan  # pylint: disable=wrong-import-position # Order needed for if __name__=='__main__': tests to work
import sys
import os
dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, ".."))


class Player:
    def __init__(self, deck: Deck) -> None:
        self.caravans = (Caravan(), Caravan(), Caravan())
        self.deck = deck
        self.hand = []

    def deal_a_hand(self):
        self.hand = self.deck.deal_cards(8)

    def play_card(self, idx):
        if len(self.hand) == 0 or len(self.hand) < idx+1:
            return None
        card = self.hand.pop(idx)
        if len(self.hand) < 5:
            new_card = self.deck.deal_cards(1)
            if len(new_card) > 0:
                self.hand.append(new_card[0])
        return card

    def get_hand_as_str(self):
        return [str(c) for c in self.hand]

    def get_caravans_as_str(self):
        out = f'{"Caravan 1:":15} {"Caravan 2:":15} {"Caravan 3:":15}\n'
        longest_caravan_len = len(
            max(self.caravans, key=lambda c: len(c.cards)).cards)
        for i in range(longest_caravan_len):
            card_info = []
            for caravan in self.caravans:
                if len(caravan.cards) <= i:
                    card_info.append('')
                else:
                    card_info.append(str(caravan.cards[i]))
            out += f'{card_info[0]:15} {card_info[1]:15} {card_info[2]:15}\n'
        return out

if __name__ == '__main__':
    s = CardSet()
    s.create_set_from_all_cards()
    d = Deck(s)
    p = Player(d)
    p.deck.shuffle()
    p.deal_a_hand()
    p.caravans[0].insert_card(p.play_card(0))
    p.caravans[1].insert_card(p.play_card(0))
    p.caravans[2].insert_card(p.play_card(0))
    print(p.get_caravans_as_str())
