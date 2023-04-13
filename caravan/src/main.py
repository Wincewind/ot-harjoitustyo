from ui.text.game_interface import GameInterface

# def third_week_demo():
#     c_set = CardSet()
#     c_set.create_set_from_all_cards()
#     deck = Deck(c_set)
#     player = Player(deck)
#     player.deck.shuffle()
#     player.deal_a_hand()
#     i = 0
#     while True:
#         c_idx = parse_idx_input_or_quit(
#             player,
#             'Choose one of your Caravans. Input index [0-2] or quit by typing "quit":',
#             0,
#             2,
#         )
#         if c_idx == "quit":
#             break
#         idx = parse_idx_input_or_quit(
#             player,
#             f'Which card to add to Caravan {c_idx}? Input index [0-7] or quit by typing "quit":',
#             0,
#             7,
#         )
#         if idx == "quit":
#             break
#         crd = player.play_card(idx)
#         if crd is None:
#             break
#         player.caravans[c_idx].insert_card(crd, i)
#         i += 1

def fourth_week_demo():
    game_int = GameInterface()
    game_int.game_setup()
    game_int.game_loop()



if __name__ == "__main__":
    #third_week_demo()
    fourth_week_demo()
