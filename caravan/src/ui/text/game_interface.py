import os
from entities.deck import Deck
from entities.player import Player
from entities.cardset import CardSet
import rules


class GameInterface():
    def __init__(self) -> None:
        self.player = None
        self.opponent = None
        self.pl_nums = (1, 2)

    def game_setup(self):
        p1_set = CardSet()
        p1_set.create_basic_set()
        p1_deck = Deck(p1_set)
        self.player = Player(p1_deck)
        self.player.deck.shuffle()
        self.player.deal_a_hand()
        p2_set = CardSet()
        p2_set.create_basic_set()
        p2_deck = Deck(p2_set)
        self.opponent = Player(p2_deck)
        self.opponent.deck.shuffle()
        self.opponent.deal_a_hand()
        # self.player.caravans[0].insert_card(Card(None,'Hearts',10,False))
        # self.player.caravans[1].insert_card(Card(None,'Hearts',10,False))
        # self.player.caravans[2].insert_card(Card(None,'Hearts',10,False))
        # self.player.caravans[0].insert_card(Card(None,'Hearts',10,False))
        # self.player.caravans[1].insert_card(Card(None,'Hearts',10,False))
        # self.player.caravans[2].insert_card(Card(None,'Hearts',9,False))
        # self.player.caravans[0].insert_card(Card(None,'Hearts',5,False))
        # self.player.caravans[1].insert_card(Card(None,'Hearts',5,False))

    def clear_screen(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def print_setup(self):
        self.clear_screen()
        print("Opponent Caravans:")
        print(self.opponent.get_caravans_as_str())
        print("Caravan values:")
        print(  # Not sure how to make this shorter without one time var assingments for the values.
            f"{self.opponent.caravans[0].value:<15}{self.opponent.caravans[1].value:<15}{self.opponent.caravans[2].value:<15}"  # pylint: disable=line-too-long
        )
        print('\U0001F0A0 '*len(self.opponent.hand)+'\n')

        print("Your Caravans:")
        print(self.player.get_caravans_as_str())
        print("Caravan values:")
        print(  # Not sure how to make this shorter without one time var assingments for the values.
            f"{self.player.caravans[0].value:<15}{self.player.caravans[1].value:<15}{self.player.caravans[2].value:<15}"  # pylint: disable=line-too-long
        )
        print("Your hand:", self.player.get_hand_as_str())
        print('Remaining cards in your deck:', len(self.player.deck.cards))
        print()

    def change_player_turn(self):
        self.player, self.opponent = self.opponent, self.player
        self.pl_nums = (self.pl_nums[1], self.pl_nums[0])

    def parse_idx_input_or_quit(self, query: str, minimum: int, maximum: int):
        while True:
            self.print_setup()
            try:
                i = input(query)
                if i == '':
                    i = -1
                if i in ["quit", "q", 'c', 'cancel']:
                    break
                i = int(i)
                if minimum > i or i > maximum:
                    continue
                break
            except ValueError:
                continue
        return i

    def confirm_player_indexes(self):
        inputs_to_handle = ['caravan', 'card', 'placement']
        i = 0
        indexes = [-1, -1, -1]
        breakit = False
        while i < len(inputs_to_handle) and not breakit:
            if inputs_to_handle[i] == 'caravan':
                indexes[i] = self.parse_idx_input_or_quit(
                    'Choose one of the Caravans. Input index [0-5] ' +
                    '(0-2 yours, 3-5 opponents) or stop the game by typing "q":',
                    0,
                    5)
                if isinstance(indexes[i], str):
                    breakit = True
                    break
                if indexes[i] in [0, 1, 2]:
                    caravan = self.player.caravans[indexes[i]]
                else:
                    caravan = self.opponent.caravans[indexes[i]-3]

            if inputs_to_handle[i] == 'card':
                indexes[i] = self.parse_idx_input_or_quit(
                    f'Which card to add to Caravan {indexes[i-1]}? '
                    f'Input index [0-{len(self.player.hand)-1}]. '
                    'Cancel action with c or quit by typing "quit":',
                    0,
                    len(self.player.hand)-1)
                if isinstance(indexes[i], str):
                    if indexes[i] in ['c', 'cancel']:
                        i -= 1
                        continue
                    breakit = True
                    break

            if inputs_to_handle[i] == 'placement':
                indexes[i] = self.parse_idx_input_or_quit(
                    'Where do you want to place the card? '
                    "\n(If it's a number card, it has to be placed at the top "
                    "of the deck with idx -1 or "
                    f'{len(caravan.cards)-1}) \nInput index, cancel action with '
                    'c or quit by typing "quit":',
                    -2,
                    float('inf'))
                if isinstance(indexes[i], str):
                    if indexes[i] in ['c', 'cancel']:
                        i -= 1
                        continue
                    breakit = True
                    break
            i += 1
        if breakit:
            return None
        return (caravan, indexes[2], self.player.hand[indexes[1]])

    def play_cards(self):
        while True:
            move = self.confirm_player_indexes()
            if move is None:
                break
            caravan = move[0]
            is_allowed = rules.check_if_legal_move(
                self.player, self.opponent, move)
            if not is_allowed[0]:
                print(is_allowed[1])
                input('press any key to continue')
                continue
            crd = self.player.play_card(self.player.hand.index(move[2]))
            if crd.special:
                cards_to_remove = []
                if crd.value == 11:
                    cards_to_remove = rules.get_cards_removed_by_jack(move)
                elif crd.value == 0:
                    cards_to_remove = rules.get_cards_removed_by_joker(
                        self.player, self.opponent, move)
                elif crd.value == 13:
                    rules.double_total_with_king(move)
                for card in cards_to_remove:
                    caravan.cards.remove(card)
            caravan.insert_card(crd, move[1])
            if rules.is_player_winner(self.player, self.opponent) is None:
                self.change_player_turn()
            break

    def discard_caravan(self):
        idx = ''
        while not isinstance(idx, int):
            idx = self.parse_idx_input_or_quit(
                'Choose one of your caravans to discard. Input index [0-2]:',
                0,
                2)
        self.player.caravans[idx].cards = []
        self.change_player_turn()

    def discard_card(self):
        idx = ''
        while not isinstance(idx, int):
            idx = self.parse_idx_input_or_quit(
                'Choose one of the cards in your hand to discard.'
                f'Input index [0-{len(self.player.hand)-1}].',
                0,
                len(self.player.hand)-1)
        self.player.hand.pop(idx)
        self.change_player_turn()

    def game_loop(self):
        while rules.is_player_winner(self.player, self.opponent) is None:
            self.clear_screen()
            input('press any key to start your turn Player ' +
                  str(self.pl_nums[0]))
            self.print_setup()
            action_choices = 'Choose on of the following actions:\n1: Play a card\n2: Discard one of your caravans'
            max_choices = 2
            if all(c.started for c in self.player.caravans):
                action_choices += '\n3: Discard a card from your hand'
                max_choices += 1
            action_choices += '\nYou can also choose to end the game by typing "q".'
            action = self.parse_idx_input_or_quit(action_choices,
                                                  1,
                                                  max_choices)
            if isinstance(action, str):
                break
            if action == 1:
                self.play_cards()
            if action == 2:
                self.discard_caravan()
            if action == 3:
                self.discard_card()

        if rules.is_player_winner(self.player, self.opponent) is not None:
            self.print_setup()
            print(f'Congratulations Player {self.pl_nums[0]}, you\'ve won!')
