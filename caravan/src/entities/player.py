import copy
from entities.caravan import Caravan
from entities.deck import Deck


class Player:
    """Class representing a player in the Caravan card game.

    Attributes:
        caravans: A tuple of 3 caravan objects.
        deck: A deck of cards object.
        hand: A list of card objects.
    """

    def __init__(self, deck: Deck) -> None:
        self.caravans = (Caravan(), Caravan(), Caravan())
        self.deck = deck
        self.hand = []

    def deal_a_hand(self):
        """Fill the hand attribute with 8 cards from the deck attribute.
        """
        self.hand = self.deck.deal_cards(8)

    def play_card(self, idx):
        """Play a card from the hand. If there are less than 4 cards 
        in hand after removing one and there are still cards in the deck; a 
        replacing card is dealt back into the hand.

        Args:
            idx (int): Index of the card to be played.

        Returns:
            Card: Card object that was selected.
        """
        if len(self.hand) == 0 or len(self.hand) < idx+1:
            return None
        card = self.hand.pop(idx)
        if len(self.hand) < 5:
            new_card = self.deck.deal_cards(1)
            if len(new_card) > 0:
                self.hand.append(new_card[0])
        return card

    def get_hand_as_str(self):
        """Get the str descriptions for the cards in player's hand.

        Returns:
            list: List of the cards' descriptions.
        """
        return [str(c) for c in self.hand]

    def get_caravans_as_str(self):
        """Get the str descriptions for the cards in player's caravans. 

        Returns:
            list: List of the cards' descriptions.
        """
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

    def __copy__(self):
        deck = copy.copy(self.deck)
        player = Player(deck)
        player.caravans = (copy.copy(self.caravans[0]),
                           copy.copy(self.caravans[1]),
                           copy.copy(self.caravans[2]))
        player.hand = [copy.copy(crd) for crd in self.hand]
        player.deck.cards = [copy.copy(crd) for crd in self.deck.cards]
        return player
