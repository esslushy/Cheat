from Card import Card
import random

suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']

class Deck():
    def __init__(self, empty=False):
        if empty:
            self.cards = []
        else:
            self.newDeckOrder()

    def newDeckOrder(self):
        self.cards = []
        for suit in suits:
            if suit is 'Hearts' or suits is 'Clubs':
                for num in range(1, 14):
                    self.cards.append(Card(suit, num))
            else:
                for num in range(13, 0, -1):
                    self.cards.append(Card(suit, num))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, num=1):
        drawnCards = []
        for i in range(num):
            drawnCards.append(self.cards[i])
            self.cards.remove(self.cards[i])
        if(len(drawnCards) == 1):
            return drawnCards[0]
        else:
            return drawnCards

    def __str__(self):
        return self.cards