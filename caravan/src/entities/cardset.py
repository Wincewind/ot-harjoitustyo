try:
    from entities.card import Card
except ModuleNotFoundError:
    from card import Card

class CardSet:
    sets = ['sylly','minime453']
    values = range(1,14)
    suits = ['Spades','Clubs','Diamonds','Hearts']

    def __init__(self) -> None:
        self.__set = []

    def create_set_from_all_cards(self):
        self.__set = []
        for set in CardSet.sets:
            for suit in CardSet.suits:
                for value in CardSet.values:
                    special = False
                    if value == 1 or value > 10:
                        special = True
                    self.__set.append(Card(set,suit,value,special))
            self.__set.append(Card(set,'Black Joker',0,True))
            self.__set.append(Card(set,'Red Joker',0,True))

    def add_card(self, card: Card):
        self.__set.append(card)

    def __str__(self) -> str:
        return str([str(c) for c in self.__set])
    
    def __len__(self) -> int:
        return len(self.__set)
    
    def get_cards(self):
        return self.__set.copy()

if __name__=='__main__':
    set = CardSet()
    set.create_set_from_all_cards()
    print(set)