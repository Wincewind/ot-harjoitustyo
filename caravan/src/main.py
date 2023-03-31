import sys
import os
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parents[0]))
from entities.deck import Deck
from entities.player import Player
from entities.cardset import CardSet

def third_week_demo():
    c_set = CardSet()
    c_set.create_set_from_all_cards()
    deck = Deck(c_set)
    player = Player(deck)
    player.deck.shuffle()
    player.deal_a_hand()
    i = 0
    car = player.caravans[0]
    while True:
        os.system('cls')
        print('Your Caravan:')
        print(car)
        print('Caravan value',car.value)
        print('Your hand:',player.get_hand_as_str())
        print()
        idx = 100
        while  0 > idx or idx > 7:
            try:
                idx = input('Which card to add to Caravan? Input index [0-7] or quit by typing "quit":')
                if idx == 'quit':
                    break
                else:
                    idx = int(idx)
            except ValueError:
                pass
            c = player.play_card(idx)
            if c == None:
                break
            else:
                car.insert_card(i,c)
        i += 1
if __name__=='__main__':
    third_week_demo()