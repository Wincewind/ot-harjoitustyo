from entities.card import Card


class Caravan:
    """ Class that represents a stack of playing cards in the game caravan.
        Each Player class has a tuple of 3 of these.

    Attributes:
        cards: A list containing the stacked Card objects.
        started: Important detail related to some game rules. This is set to True, 
                 once the first card is inserted into the cards and will stay so even if
                 the caravan is emptied.
    
    """
    def __init__(self) -> None:
        self.cards = []
        self.started = False

    def insert_card(self, card: Card, idx=-1):
        """ Inserts a card given into the caravan before the given index.
            Mostly just to set the caravan as started if it wasn't yet.

        Args:
            card (Card): Card object to insert.
            idx (int, optional): Where to insert the card. Defaults to -1.
        """
        if len(self.cards) == 0:
            self.started = True
        if idx == -1:
            self.cards.append(card)
        else:
            self.cards.insert(idx, card)

    @property
    def value(self):
        """Returns the value of the card total in the caravan. Needed for checking the winner.

        Returns:
            int: Sum of the card totals.
        """
        return sum(c.total for c in self.cards)

    @property
    def order_descending(self):
        """Property to return the 'order' of the caravan. 
        Order is determined by the last 2 number cards in the caravan 
        and is then flipped by each Queen on top of the last number card.

        Returns:
            nullable bool: True, if the order is descending, 
            False if ascending and None if order can't be determined. 
        """
        order_desc = None
        number_cards = [c for c in self.cards if not c.special]
        if len(number_cards) < 2 or number_cards[-1].value == number_cards[-2]:
            return order_desc
        order_desc = number_cards[-1].value < number_cards[-2].value
        for crd in self.cards[::-1]:
            if crd.value == 12:
                order_desc = not order_desc
            if not crd.special:
                break
        return order_desc

    def __str__(self) -> str:
        return ''.join(f'{str(c)}\n' for c in self.cards)

    def __copy__(self):
        caravan = Caravan()
        caravan.cards = self.cards.copy()
        caravan.started = self.started
        return caravan
