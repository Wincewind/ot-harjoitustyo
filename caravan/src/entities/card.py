class Card:
    suits = {'Diamonds':'\u2666', 'Hearts':'\u2665', 'Clubs':'\u2663', 'Spades':'\u2660'}
    values = list(range(14))

    def __init__(self, c_set: str, suit: str, value: int, special=False) -> None:
        self.set = c_set
        self.suit = suit
        self.value = value
        self.special = special

    def __str__(self) -> str:
        card_value = self.value
        if card_value == 0:
            return f"{self.suit}"# - {self.set}"
        if card_value == 1 or card_value > 10:
            specials = {1:'Ace',11:'Jack',12:'Queen',13:'King'}
            card_value = specials[card_value]

        return f"{card_value} of {Card.suits[self.suit]}"# - {self.set}"

if __name__=='__main__':
    c = Card('test','Hearts',12)
    print(c)
