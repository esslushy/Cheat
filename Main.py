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

def didPlayerLie(computer, playedCard, numCards):
    return computer['knownCards'][playedCard] + numCards <= 4
    
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
            print(f'You don\'t have that card!!\nTry again and play cards you do have.')
            return takeTurn(player)
        else:
            cards.append(playedCard)
        # Reset if card is valid
        validCard = False
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

def buildKnownCards(computer):
    # Empty known cards
    computer['knownCards'] = {}
    # For each card increment number of them known by 1
    for card in computer['hand']:
        computer['knownCards'][int(card.number)] += 1

def takeRoboTurn(computer):
    cards = []
    # Check if computer has a card that is one up or one down from last card played
    if lastPlayedCard - 1 in computer['hand']:
        # Set played card to that
        playedCard = lastPlayedCard - 1
        # Find all cards of that type
        for card in computer['hand']:
            if card.number == playedCard:
                cards.append(card)
    elif lastPlayedCard + 1 in computer['hand']:
        # Set played card to that
        playedCard = lastPlayedCard + 1
        # Find all cards of that type
        for card in computer['hand']:
            if card.number == playedCard:
                cards.append(card)
    else:
        # If computer has no cards just randomly play a fake card and lie.
        if computer['knownCards'[lastPlayedCard - 1] < 4:
            # If the computer know that there are less than 4 of those cards play a fake one
            playedCard = lastPlayedCard - 1
            cards.append(computer['hand'][0])
            computer['cheated'] = True
        else:
            # If the smaller card has all 4 played play the larger. Even if this has 4 it has to be done this way.
            playedCard = lastPlayedCard + 1
            cards.append(computer['hand'][0])
            computer['cheated'] = True
    # Remove cards from computers hand
    for card in cards:
        computer['hand'].remove(card)
    return playedCard, len(cards)

numPlayers = int(input('How many players are playing: '))
if numPlayers <= 0:
    raise IndexError('Not a valid index')

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

# Split deck among players if more than 1 player
if len(players) > 1:
    for i in range(len(deck.cards)):
        players[i%numPlayers]['hand'].append(deck.draw())
# Split between player and computer
else: 
    # Set up computer
    computer = {
        'hand' : [],
        'cheated' : False,
        # Contains list of all possible card nums and how many of each it knows of
        'knownCards' : {}
    }
    # Setup categories for known cards
    for key in numberToCard:
        computer['knownCards'][key] = 0
    # Deal out deck
    for i in range(26):
        players[0]['hand'].append(deck.draw())
        computer['hand'].append(deck.draw())
    # Add computers cards to known cards
    buildKnownCards(computer)

# Start game
currentTurn = 1
playedDeck = Deck(True)
caught = False
winner = False

if len(players) > 1:
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
                        player['hand'].extend(playedDeck.cards)# Give player deck cards
                        playedDeck.cards = []# Empty deck
                        break # No longer need to continue for loop if already caught
                    else: # If they didn't cheat
                        print(f'Player {player["num"]} did not cheat. You get the deck.')
                        p['hand'].extend(playedDeck.cards)# Give accuser deck cards
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
else: # If there is only 1 player
    # Pull out only player
    player = players[0]
    while(not winner):
        print('It is the players turn.')
        if lastPlayedCard == -1:
            print('Play any card')
        else:
            print('Play a card one value above or below ' + numberToCard[lastPlayedCard])
        # Player takes turn
        lastPlayedCard, numCards = takeTurn(player)
        # Get computer to guess if player is lying
        if didPlayerLie(computer, lastPlayedCard, numCards):
            # If the computer thinks the player is lying and they are
            if player['cheated']:
                print('Player did cheat. They get the deck.')
                player['hand'].extend(playedDeck.cards)# Give player deck cards
                playedDeck.cards = []# Empty deck
            # Computer thought player was lying but they weren't
            else:
                print('Player did not cheat. Computer gets the deck.')
                # Give computer the deck
                computer['hand'].extend(playedDeck.cards)
                playedDeck.cards = []
                # Rebuild known cards from cards in hand
                buildKnownCards(computer)
        # If computer did not think the player is lying
        else:
            if player['cheated']:
                print('Peanut Butter')
                # Computer doesn't know what is played
            else:
                # Computer now knows more cards.
                computer['knownCards'][lastPlayedCard] += numCards
        # Check if player has won
        if len(player['hand']) == 0:
            print('Congratulations player. You have won!')
            winner = True
            break
        # Reset cheated status
        player['cheated'] = False
        # Computer's Turn
        lastPlayedCard, numCards = takeRoboTurn(computer)
        clear()
        print('Player\'s guess')
        print(f'Computer played {numCards} {numberToCard[lastPlayedCard]}(s)')
        print(player['hand'])
        thinkCheating = input('Player, do you think the computer is cheating? (yes or no)\n').lower()
        thinkCheating = thinkCheating == 'yes' or thinkCheating == 'y'# Makes true if yes otherwise false for no
        if thinkCheating:
            if computer['cheated']:
                print('Computer did cheat. They get the deck.')
                caught = True
                computer['hand'].extend(playedDeck.cards)# Give player deck cards
                playedDeck.cards = []# Empty deck
            else: # If they didn't cheat
                print('Computer did not cheat. You get the deck.')
                player['hand'].extend(playedDeck.cards)# Give accuser deck cards
                playedDeck.cards = []# Empty deck
        # If computer lied make them say peanut butter
        if not caught and computer['cheated']:
            print('peanut butter')
        # If computer's hand it empty at end of their turn they win
        if len(computer['hand']) == 0:
            winner = True
            print('The computer has won!')
            break
        # Reset status
        computer['cheated'] = False
        caught = False