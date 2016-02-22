#!/usr/bin/python
from coupDeck import *
from coupModel import *
from slackView import *

import time, pprint
from slackclient import SlackClient

# print "-----------------------------------------"
# token = "xoxb-22371870822-R4NMrSgKKyldo4xJj7nQNM4F" # Random Projects -- will need to change in the future
# sc = SlackClient(token)

# Game Starts:
postMessage(groupChannel, "Let the Coup BEGIN!")
print "-----------------------------------------"
# How many players?
temp_playerInputPlayers = 2
temp_playerInputNames = ['user_charlie', 'user_fakecharlie']
temp_playerInputIds = ['U0NAWS465', 'U0NCAB0DD']
temp_playerInputChannel = ['D0NAXBNTU', 'D0NCB3F8S']

# Initialize variables
# 1. Shuffle Deck
gameDeck = odeck[:]
gameDeck = shuffleDeck(gameDeck)
print gameDeck

# 2. Create Player Objects
players = {}
for player in temp_playerInputNames:
    postMessage(groupChannel, "creating %s player..." % player)
    players["player{0}".format(player)] = makePlayer(gameDeck, player, 
        temp_playerInputIds[temp_playerInputNames.index(player)], 
        temp_playerInputChannel[temp_playerInputNames.index(player)])

postMessage(groupChannel, displayBoard(players))

# goldAccounting(players['playerCharlie'], 20)
# coupTarget(players['playerCharlie'], players['playerAynRand'])
# coupTarget(players['playerCharlie'], players['playerAynRand'])
# displayBoard(players)

# Begin Game
print "-----------------------------------------"
while True:
    for playerID in range(temp_playerInputPlayers):
        if isPlayerAlive(players[str('player' + temp_playerInputNames[playerID])]):
            postMessage(groupChannel, "Player %s's turn!" % players[str('player' + temp_playerInputNames[playerID])].name)
            postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, 
                "Your turn! What will you do? \n \
                Income | Foreign Aid | Coup | Tax | Steal | Assassinate | Exchange")
            playerTurnTrigger = True
            while playerTurnTrigger == True:
                playerInput = getUserInput(players[str('player' + temp_playerInputNames[playerID])].slackId)
                # Player Inputs
                # For every other player, Accept | Challenge options + more
                if playerInput == "Income":
                    income(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                elif playerInput == "Foreign Aid":
                    print "Does anyone challenge?" # build challenge function

                    foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                elif playerInput == "Coup":
                    coupTarget(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                elif playerInput == "Tax":
                    foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                elif playerInput == "Steal":
                    foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                elif playerInput == "Assassinate":
                    foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                elif playerInput == "Exchange":
                    foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                else:
                    print "invalid input"

        # Check for victory condition
        deadPlayers = 0
        for i in range(temp_playerInputPlayers):
            if isPlayerAlive(players[str('player' + temp_playerInputNames[i])]):
                deadPlayers += 1
        if deadPlayers >= temp_playerInputPlayers - 1:
            print "GAME OVER!"
            break

