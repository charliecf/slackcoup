#!/usr/bin/python
from coupDeck import *
from coupModel import *

# Game Starts:
print "Let the Coup BEGIN!"
print "-----------------------------------------"
# How many players?
temp_playerInputPlayers = 3
temp_playerInputNames = ['Charlie', 'AynRand', 'Frankenstein']
# Initialize variables
# 1. Shuffle Deck
gameDeck = odeck[:]
gameDeck = shuffleDeck(gameDeck)
print gameDeck

# 2. Create Player Objects
players = {}
for player in temp_playerInputNames:
    print "creating %s player..." % player
    players["player{0}".format(player)] = makePlayer(gameDeck, player)
print players
print ""
print gameDeck

print ""
print "Killing Charlie..."
players['playerCharlie'].isAlive = False
print "%s is alive? %s" % (players['playerCharlie'].name, players['playerCharlie'].isAlive)
print "%s is alive? %s" % (players['playerAynRand'].name, players['playerAynRand'].isAlive)

print doesPlayerHaveCard(players['playerCharlie'], 'Assassin')
print doesPlayerHaveCard(players['playerCharlie'], 'fake card')
print doesPlayerHaveCard(players['playerCharlie'], players['playerCharlie'].cards[0])

displayBoard(players)

print players['playerCharlie'].gold

goldAccounting(players['playerCharlie'], 8)
print players['playerCharlie'].gold

coupTarget(players['playerCharlie'], players['playerAynRand'])
displayBoard(players)

stealTarget(players['playerAynRand'], players['playerCharlie'])
displayBoard(players)

income(players['playerAynRand'])

exchangeCards(gameDeck, players['playerCharlie'])

# Begin Game
print "-----------------------------------------"
while True:
    for playerID in range(temp_playerInputPlayers):
        print "Player %s your turn! What do you do?" % playerID
        print "Income | Foreign Aid | Coup | Tax | Steal | Assassinate | Exchange"
        playerInput = raw_input("> ")
        # Player Inputs
        # if playerInput == "Income":
        # For every other player, Accept | Challenge options + more
