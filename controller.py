#!/usr/bin/python

from coupDeck import *
from coupModel import *
from slackView import *

import time, pprint
from slackclient import SlackClient

# ---------- controller functions start ----------
"""
These functions bridge the gap between Model and View
Functions in these category should require both player input as well as 
changing backend data
"""

def giveUpInfluence(player):
    """
    Requirements: doesPlayerHaveCard(), removeInfluence()

    player has lost an influence, needs to pick an influence to give up
    """
    postMessage(player.slackId, "You lost an influence... please pick an influence to lose")
    while True:
        card = getUserInput(player.slackChannel)
        if doesPlayerHaveCard(player, card):
            postMessage(player.slackId, "You have chosen to give up your %s" % card)
            postMessage(groupChannel, "%s has given up his %s" % (player.name, card))
            player.cards.remove(card)
            player.deadCards.append(card)
            removeInfluence(player)
            return
        else:
            postMessage(player.slackId, "You don't have a %s" % (card))

def challengesCard(deck, player, target, card):
    """
    Requirements: doesPlayerHaveCard()[coupModel], returnCardsToDeck()[coupModel], giveUpInfluence()

    player challenges target for card
    Check if target has card
        IF target does not have card: target loses influence
        ELSE player loses influence
    """
    postMessage(groupChannel, "%s challenges %s saying he does not have a %s!" % (player.name, target.name, card))
    if doesPlayerHaveCard(target, card) == True:
        postMessage(groupChannel, "%s does have a %s" % (target.name, card))
        postMessage(groupChannel, "%s loses an influence" % player.name)
        postMessage(player.slackId, "You lost the challenge!")
        giveUpInfluence(player)
        postMessage(groupChannel, "%s returns his %s into the deck and draws a new card" % (target.name, card))
        returnCardsToDeck(deck, target, card)
        dealCards(deck, player, 1)
        postMessage(player.slackId, "Your cards are: %s" % player.cards)
        return False
    else:
        postMessage(groupChannel, "%s is indeed a liar and does not have a %s" % (target.name, card))
        postMessage(groupChannel, "%s loses an influence" % target.name)
        postMessage(player.slackId, "You won the challenge! Winner winner chicken dinner!!!")
        giveUpInfluence(target)
        return True

def coupTarget(player, target):
    """
    Requirements: haveEnoughGold()[coupModel], goldAccounting()[coupModel], giveUpInfluence()

    player -7 coins
    Remove influence from target
    not possible to block or challenge
    """
    if haveEnoughGold(player, 7):
        postMessage(groupChannel, "%s launches a coup against %s" % (player.name, target.name))
        goldAccounting(player, -7)
        giveUpInfluence(target)
    else:
        print "You do not have enough money to coup... nice try..."

def stealTarget(player, target):
    """
    player attempts to steal from target (Captain ability)
        IF successful: -2 coins from target, player +2 coins
        ELSE: None
    """
    if target.gold == 0:
        postMessage(groupChannel, "%s stole from a broke man... (0 gold) from %s" % (player, target))
    elif target.gold == 1:
        postMessage(groupChannel, "%s stole 1 gold from %s" % (player, target))
        goldAccounting(player, +1)
        goldAccounting(target, -2)
    else:
        postMessage(groupChannel, "%s stole 2 gold from %s" % (player, target))
        goldAccounting(player, +2)
        goldAccounting(target, -2)

def assassinateTarget(player, target):
    """
    Requirements: haveEnoughGold()[coupModel], goldAccounting()[coupModel], giveUpInfluence()

    player -3 coins
    Attempts to assassinate target (Assassin ability)
        IF successful: remove influence from target
        ELSE: None
    """
    if haveEnoughGold(player, 3):
        goldAccounting(player, -3)
        giveUpInfluence(target)
    else:
        print "You do not have enough money to assassinate... nice try..."

def exchangeCards(deck, player):
    """
    Requirements: dealCards()[coupModel], returnCardsToDeck()[coupModel]

    player attempts to exchange cards (Ambassador ability)
        IF successful player +2 cards, return 2 cards
        ELSE: None
    """
    dealCards(deck, player, 2)
    while len(player.cards) != 2:
        card = raw_input("What card would you like to return? > ")
        returnCardsToDeck(deck, player, card)
    print "completed exchange!"


def action_stealTarget(deck, player, target):
    """
    Requirements: challengesCard(), stealTarget()
    """
    postMessage(groupChannel, "%s attempts to steal from %s in the name CaptainCrunch!" % (player.name, target.name))
    postMessage(target.slackId, "%s is trying to steal from you... what do you do?" % player.name)
    postMessage(target.slackId, "Allow | Block (with Captain) | Block (with Ambassador) | Challenge")
    playerInput = getUserInput(target.slackChannel)
    if playerInput == "Allow":
        postMessage(target.slackId, "I see you're taking it like a wuss huh?")
        stealTarget(player, target)

    elif playerInput == "Block (with Captain)":
        # Challenger claims to have a Captain
        postMessage(groupChannel, "%s claims to have a Captain, any challengers (30 seconds to respond)?" % player.name)
        postMessage(groupChannel, "Say: 'Challenge'")
        challengerInput = ""
        challengerInput = getUserInputTimeout(groupChannel, 30)
        challengerUser = getPlayerFromSlackId(players, challengerInput[1])
        if challengerInput[0] == "Challenge":
            # print challengerInput[1]
            challengesCard(gameDeck, challengerUser, players[str('player' + temp_playerInputNames[playerID])], "Captain")
            if challengesCard(gameDeck, challengerUser, players[str('player' + temp_playerInputNames[playerID])], "Captain") == False:
                postMessage(groupChannel, "Blocked Steal with Captain")
            else:
                stealTarget(player, target)
        else:
            postMessage(groupChannel, "Blocked Steal with Captain")

    elif playerInput == "Block (with Ambassador)":
        # Challenger claims to have a Ambassador
        postMessage(groupChannel, "%s claims to have a Ambassador, any challengers (30 seconds to respond)?" % player.name)
        postMessage(groupChannel, "Say: 'Challenge'")
        challengerInput = ""
        challengerInput = getUserInputTimeout(groupChannel, 30)
        challengerUser = getPlayerFromSlackId(players, challengerInput[1])
        if challengerInput[0] == "Challenge":
            # print challengerInput[1]
            challengesCard(gameDeck, challengerUser, players[str('player' + temp_playerInputNames[playerID])], "Ambassador")
            if challengesCard(gameDeck, challengerUser, players[str('player' + temp_playerInputNames[playerID])], "Ambassador") == False:
                postMessage(groupChannel, "Blocked Steal with Ambassador")
            else:
                stealTarget(player, target)
        else:
            postMessage(groupChannel, "Blocked Steal with Ambassador")

    elif playerInput == "Challenge":
        challengesCard(deck, player, target, "Captain")
        if challengesCard(deck, player, target, "Captain") == False:
            stealTarget(player, target)           
    else:
        postMessage(target.slackId, "I don't understand you... but I'll assume you like getting robbed")
        stealTarget(player, target)

def selfStatusUpdate(player):
    cards = player.cards
    deadCards = player.deadCards
    gold = player.gold
    postMessage(player.slackId, "You have %s gold" % gold)
    if deadCards == "":
        postMessage(player.slackId, "You have %s cards" % cards)
    else:
        postMessage(player.slackId, "You have %s cards and %s [DEAD]" % (cards, deadCards))

# ----------------------------------------------
# ---------- controller functions end ----------
# ----------------------------------------------

# Game Starts:
postMessage(groupChannel, "-----------------------------------------")
postMessage(groupChannel, "Let the Coup BEGIN!")
postMessage(groupChannel, "Listen up kids, I'm an alpha Octopus, so if you can't follow my instructions to the tee, go buy a dictionary!")
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

goldAccounting(players['playeruser_charlie'], 20)
# coupTarget(players['playerCharlie'], players['playerAynRand'])
# coupTarget(players['playerCharlie'], players['playerAynRand'])
# displayBoard(players)

# giveUpInfluence(players['playeruser_charlie'])
# challengesCard(gameDeck, players['playeruser_charlie'], players['playeruser_fakecharlie'], "Duke")

# Begin Game
print "-----------------------------------------"
while True:
    for playerID in range(temp_playerInputPlayers):
        if isPlayerAlive(players[str('player' + temp_playerInputNames[playerID])]):
            postMessage(groupChannel, "Player %s's turn!" % players[str('player' + temp_playerInputNames[playerID])].name)
            postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, 
                "Your turn! What will you do? \nIncome | Foreign Aid | Coup | Tax | Steal | Assassinate | Exchange")
            playerTurnTrigger = True
            while playerTurnTrigger == True:
                playerInput = getUserInput(players[str('player' + temp_playerInputNames[playerID])].slackChannel)
                print "----------------HERE-------------------------"
                print playerInput
                # Player Inputs
                # For every other player, Accept | Challenge options + more
                if playerInput == "Income":
                    income(players[str('player' + temp_playerInputNames[playerID])])
                    postMessage(groupChannel, "%s takes Income, +1 gold" % players[str('player' + temp_playerInputNames[playerID])].name)
                    postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, "Your have gained +1 gold from Income")
                    playerTurnTrigger = False

                elif playerInput == "Foreign Aid":
                    postMessage(groupChannel, "%s claims Foreign Aid, any challengers (30 seconds to respond)?" % players[str('player' + temp_playerInputNames[playerID])].name)
                    postMessage(groupChannel, "Say: 'I have a Duke'")
                    challengerInput = ""
                    challengerInput = getUserInputTimeout(groupChannel, 30)
                    challengerUser = getPlayerFromSlackId(players, challengerInput[1])
                    if challengerInput[0] != 'I have a Duke':
                        # No challenges:
                        postMessage(groupChannel, "30 seconds up! I see no challengers...'")
                        foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                        postMessage(groupChannel, "%s takes Foreign Aid, +2 gold" % players[str('player' + temp_playerInputNames[playerID])].name)
                        postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, "Your have gained +2 gold from Foreign Aid")
                    else:
                        # Challenger claims to have a Duke
                        postMessage(groupChannel, "%s claims to have a Duke, any challengers (30 seconds to respond)?" % challengerUser.name)
                        postMessage(groupChannel, "Say: 'Challenge'")
                        challengerInput2 = ""
                        challengerInput2 = getUserInputTimeout(groupChannel, 30)
                        challengerUser2 = getPlayerFromSlackId(players, challengerInput[1])
                        if challengerInput[0] == "Challenge":
                            # Check if there is Duke
                            # print challengerInput[1]
                            challengesCard(gameDeck, challengerUser2, challengerUser, "Duke")
                            if challengesCard(gameDeck, challengerUser2, challengerUser, "Duke") == False:
                                postMessage(groupChannel, "Blocked Foreign Aid with Duke")
                            else:
                                foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                        else:
                            postMessage(groupChannel, "Blocked Foreign Aid with Duke")

                    playerTurnTrigger = False

                elif playerInput == "Coup":
                    if haveEnoughGold(players[str('player' + temp_playerInputNames[playerID])], 7) == True:
                        postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, 
                            "You can coup: " + str(list(players.keys())))
                        playerTargetInput = getUserInput(players[str('player' + temp_playerInputNames[playerID])].slackChannel)
                        coupTarget(players[str('player' + temp_playerInputNames[playerID])], players[str(playerTargetInput)])
                        selfStatusUpdate(players[str('player' + temp_playerInputNames[playerID])])
                        playerTurnTrigger = False
                    else:
                        postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, "??? You're... too poor brah...")

                elif playerInput == "Tax":
                    postMessage(groupChannel, "%s declares Tax abusing his power as Duke, any challengers (30 seconds to respond)?" % players[str('player' + temp_playerInputNames[playerID])].name)
                    postMessage(groupChannel, "Say: 'Challenge'")
                    challengerInput = ""
                    challengerInput = getUserInputTimeout(groupChannel, 30)
                    challengerUser = getPlayerFromSlackId(players, challengerInput[1])
                    if challengerInput[0] == "Challenge":
                        # Check if there is Duke
                        # print challengerInput[1]
                        challengesCard(gameDeck, challengerUser, players[str('player' + temp_playerInputNames[playerID])], "Duke")
                    else:
                        postMessage(groupChannel, "%s abused his power as a Duke and taxed the poor, good job! +3 Gold" % players[str('player' + temp_playerInputNames[playerID])].name)
                        taxDuke(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                elif playerInput == "Steal":
                    postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, 
                        "You can steal from: " + str(list(players.keys())))                    
                    playerTargetInput = getUserInput(players[str('player' + temp_playerInputNames[playerID])].slackChannel)
                    action_stealTarget(gameDeck, players[str('player' + temp_playerInputNames[playerID])], players[str(playerTargetInput)])
                    playerTurnTrigger = False

                elif playerInput == "Assassinate":
                    if haveEnoughGold(players[str('player' + temp_playerInputNames[playerID])], 3) == True:
                        postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, 
                            "You can assassinate: " + str(list(players.keys())))
                        playerTargetInput = getUserInput(players[str('player' + temp_playerInputNames[playerID])].slackChannel)
                        coupTarget(players[str('player' + temp_playerInputNames[playerID])], players[str(playerTargetInput)])
                        selfStatusUpdate(players[str('player' + temp_playerInputNames[playerID])])
                        playerTurnTrigger = False
                    else:
                        postMessage(players[str('player' + temp_playerInputNames[playerID])].slackId, "??? You're... too poor brah...")

                elif playerInput == "Exchange":
                    foreignAid(players[str('player' + temp_playerInputNames[playerID])])
                    playerTurnTrigger = False

                else:
                    print "invalid input"

        # Check for victory condition
        # deadPlayers = 0
        # for i in range(temp_playerInputPlayers):
        #     if isPlayerAlive(players[str('player' + temp_playerInputNames[i])]):
        #         deadPlayers += 1
        # if deadPlayers >= temp_playerInputPlayers - 1:
        #     print "GAME OVER!"
        #     break
