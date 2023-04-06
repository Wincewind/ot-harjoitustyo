import sys
import os
from pathlib import Path
from entities.deck import Deck
from entities.player import Player
from entities.cardset import CardSet

sys.path.append(str(Path(sys.path[0]).parents[0]))


def print_setup(player: Player):
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print("Your Caravans:")
    print(player.get_caravans_as_str())
    print("Caravan values:")
    print( # Not sure how to make this shorter without one time var assingments for the values.
        f"{player.caravans[0].value:<15}{player.caravans[1].value:<15}{player.caravans[2].value:<15}" #pylint: disable=line-too-long
    )
    print("Your hand:", player.get_hand_as_str())
    print()


def parse_idx_input_or_quit(player: Player, query: str, minimum: int, maximum: int):
    while True:
        print_setup(player)
        try:
            i = input(query)
            if i == "quit":
                break
            i = int(i)
            if minimum > i or i > maximum:
                continue
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
        c_idx = parse_idx_input_or_quit(
            player,
            'Choose one of your Caravans. Input index [0-2] or quit by typing "quit":',
            0,
            2,
        )
        if c_idx == "quit":
            break
        idx = parse_idx_input_or_quit(
            player,
            f'Which card to add to Caravan {c_idx}? Input index [0-7] or quit by typing "quit":',
            0,
            7,
        )
        if idx == "quit":
            break
        crd = player.play_card(idx)
        if crd is None:
            break
        player.caravans[c_idx].insert_card(i, crd)
        i += 1


if __name__ == "__main__":
    third_week_demo()
