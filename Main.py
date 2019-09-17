from Deck import Deck
import os
from time import sleep

cardToNumber = {
    'Ace': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Jack': 11,
    'Queen': 12,
    'King': 13
}
numberToCard = {
    1: 'Ace',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: 'Jack',
    12: 'Queen',
    13: 'King'
}

lastPlayedCard = -1

clear = lambda: print(chr(27) + "[2J")
    
def takeTurn(player):
    cards = []
    print(player['hand'])
    numCards = int(input('How many cards do you want to play? \n'))
    for _ in range(numCards):
        playedCard = str(input('What card will you play? Please write it as shown above.\n'))
        # Make sure card is valid
        for card in player['hand']:
            # If the card is in hand and not already chosen
            if playedCard == str(card) and playedCard not in cards:
                validCard = True
        if not validCard:
            print('You don\'t have that card!!')
            return takeTurn(player)
        else:
            cards.append(playedCard)
    # Get the roots
    played = [card.split()[0] for card in cards]
    # What player is said they are playing
    whatIsSaid = str(input('What do you say you played? Please write the value as shown above. Ex: 2, 5, Ace, Queen. \n'))
    # If the root and what is said are off set player cheated to true
    for root in played:
        if root != whatIsSaid:
            player['cheated'] = True
    # Gets card as number
    whatIsSaid = cardToNumber[whatIsSaid]
    # If there was a last played card check to see if it fits
    if not lastPlayedCard == -1:
        # If its not 1 above or below the last card played, the player cheated
        if not whatIsSaid == lastPlayedCard-1 and not whatIsSaid ==  lastPlayedCard+1:
            player['cheated'] = True
    # Find the card the player is playing. Then ...
    for pCard in cards:
        for card in player['hand']:
            if str(card) == pCard:
                # Add it to the deck
                playedDeck.cards.append(card)
                # Remove it from their hand
                player['hand'].remove(card)
                break
    # Return what player said they played
    return whatIsSaid, numCards

numPlayers = int(input('How many players are playing: '))

players = []

# Setup players
for i in range(numPlayers):
    players.append({
        'num' : i + 1,
        'hand' : [],
        'cheated': False
    })

# Create default deck
deck = Deck()
deck.shuffle()

# Split deck among players
for i in range(len(deck.cards)):
    players[i%numPlayers]['hand'].append(deck.draw())

# Start game
currentTurn = 1
playedDeck = Deck(True)
caught = False
winner = False

while(not winner):
    for player in players:
        clear()
        print(f'Player {player["num"]}\'s turn')
        if lastPlayedCard == -1:
            print('Play any card')
        else:
            print('Play a card one value above or below ' + numberToCard[lastPlayedCard])
        lastPlayedCard, numCards = takeTurn(player)
        for p in players:
            # Skip if it is the same as the player who played the card
            if p is player: 
                continue
            # Clear Screen
            clear()
            print(f'Player {p["num"]}\'s guess')
            print(f'Player {player["num"]} played {numCards} {numberToCard[lastPlayedCard]}(s)')
            print(p['hand'])
            thinkCheating = input(f'Player {p["num"]}, do you think player {player["num"]} is cheating? (yes or no)\n').lower()
            thinkCheating = thinkCheating == 'yes' or thinkCheating == 'y'# Makes true if yes otherwise false for no
            if thinkCheating:
                if player['cheated']:
                    print(f'Player {player["num"]} did cheat. They get the deck.')
                    caught = True
                    player['hand'].extend(deck.cards)# Give player deck cards
                    playedDeck.cards = []# Empty deck
                    break # No longer need to continue for loop if already caught
                else: # If they didn't cheat
                    print(f'Player {player["num"]} did not cheat. You get the deck.')
                    p['hand'].extend(deck.cards)# Give accuser deck cards
                    playedDeck.cards = []# Empty deck
                    break # No longer need to continue if proven innocent
        # If player lied make them say peanut butter
        if not caught and player['cheated']:
            print('peanut butter')
        # If player's hand it empty at end of their turn they win
        if len(player['hand']) == 0:
                winner = True
                print(f'We have a winner!! Player {player["num"]}')
                break# Exit to while loop
        # Reset player states
        player['cheated'] = False
        caught = False
        # Give a couple seconds to see result
        sleep(3)