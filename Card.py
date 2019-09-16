symbolDict = {
    1: 'Ace',
    11: 'Jack',
    12: 'Queen',
    13: 'King'
}

class Card():
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        if number == 1 or number > 10:
            if number > 13 or number < 1: 
                raise Exception('Card number should not exceed 13 or be less than 1')
            self.symbol = symbolDict[number]
        else:
            self.symbol = str(number)

    def __str__(self):
        return self.symbol + " of " + self.suit
    
    def __repr__(self):
        return self.symbol + " of " + self.suit