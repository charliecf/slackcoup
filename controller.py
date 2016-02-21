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

displayBoard(players)

goldAccounting(players['playerCharlie'], 20)
coupTarget(players['playerCharlie'], players['playerAynRand'])
coupTarget(players['playerCharlie'], players['playerAynRand'])
displayBoard(players)

# Begin Game
print "-----------------------------------------"
while True:
    for playerID in range(temp_playerInputPlayers):
    	if isPlayerAlive(players[str('player' + temp_playerInputNames[playerID])]):	
	        print "Player %s your turn! What do you do?" % playerID
	        print "Income | Foreign Aid | Coup | Tax | Steal | Assassinate | Exchange"
	        playerInput = raw_input("> ")
	        # Player Inputs
	        # if playerInput == "Income":
	        # For every other player, Accept | Challenge options + more
		print "Phase 2"