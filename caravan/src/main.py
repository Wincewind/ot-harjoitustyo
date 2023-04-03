import sys
import os
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parents[0]))
from entities.deck import Deck
from entities.player import Player
from entities.cardset import CardSet

def print_setup(p: Player):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print('Your Caravans:')
    print(p.get_caravans_as_str())
    print('Caravan values:') 
    print(f'{p.caravans[0].value:<15}{p.caravans[1].value:<15}{p.caravans[2].value:<15}')
    print('Your hand:',p.get_hand_as_str())
    print()

def parse_idx_input_or_quit(p: Player, query: str, a: int, b: int):
    while True:
        print_setup(p)
        try:
            i = input(query)
            if i == 'quit':
                break
            else:
                i = int(i)
                if a > i or i > b:
                    continue
                else:
                    break
        except ValueError:
            continue
    return i

def third_week_demo():
    c_set = CardSet()
    c_set.create_set_from_all_cards()
    deck = Deck(c_set)
    player = Player(deck)
    player.deck.shuffle()
    player.deal_a_hand()
    i = 0
    while True:
        c_idx = parse_idx_input_or_quit(player,'Choose one of your Caravans. Input index [0-2] or quit by typing "quit":',0,2)
        if c_idx == 'quit':
            break
        idx = parse_idx_input_or_quit(player,f'Which card to add to Caravan {c_idx}? Input index [0-7] or quit by typing "quit":',0,7)
        if idx == 'quit':
            break
        c = player.play_card(idx)
        if c == None:
            break
        else:
            player.caravans[c_idx].insert_card(i,c)
        i += 1
        
if __name__=='__main__':
    third_week_demo()