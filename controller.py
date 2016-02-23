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
        postMessage(groupChannel, "%s stole from a broke man... (0 gold) from %s" % (player.name, target.name))
    elif target.gold == 1:
        postMessage(groupChannel, "%s stole 1 gold from %s" % (player.name, target.name))
        goldAccounting(player, +1)
        goldAccounting(target, -2)
    else:
        postMessage(groupChannel, "%s stole 2 gold from %s" % (player.name, target.name))
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
    originalHand = player.cards
    switchCounter = 0
    dealCards(deck, player, 2)
    newHand = player.cards
    postMessage(player.slackId, "Your cards: %s" % newHand)
    while len(player.cards) != 2:
        postMessage(player.slackId, "What card would you like to return? > ")
        card = getUserInput(player.slackChannel)
        if card in originalHand:
            switchCounter += 1
        returnCardsToDeck(deck, player, card)

    newHand = player.cards
    postMessage(player.slackId, "Your new hand: %s" % newHand)
    postMessage(groupChannel, "%s switched out %s cards" % (player.name, switchCounter))

# action_ functions contains the challenge logic and calls the plain function 
# which assumes a successful action
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
        postMessage(groupChannel, "%s claims to have a Captain, any challengers (30 seconds to respond)?" % target.name)
        postMessage(groupChannel, "Say: 'Challenge'")
        challengerInput = ""
        challengerInput = getUserInputTimeout(groupChannel, 30)
        if challengerInput[0] == "Challenge":
            challengerUser = getPlayerFromSlackId(players, challengerInput[1])
            # print challengerInput[1]
            challengesCard(gameDeck, challengerUser, players[player], "Captain")
            if challengesCard(gameDeck, challengerUser, players[player], "Captain") == False:
                postMessage(groupChannel, "Blocked Steal with Captain")
            else:
                stealTarget(player, target)
        else:
            postMessage(groupChannel, "Blocked Steal with Captain")

    elif playerInput == "Block (with Ambassador)":
        # Challenger claims to have a Ambassador
        postMessage(groupChannel, "%s claims to have a Ambassador, any challengers (30 seconds to respond)?" % target.name)
        postMessage(groupChannel, "Say: 'Challenge'")
        challengerInput = ""
        challengerInput = getUserInputTimeout(groupChannel, 30)
        if challengerInput[0] == "Challenge":
            challengerUser = getPlayerFromSlackId(players, challengerInput[1])
            # print challengerInput[1]
            challengesCard(gameDeck, challengerUser, players[player], "Ambassador")
            if challengesCard(gameDeck, challengerUser, players[player], "Ambassador") == False:
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

def action_assassinateTarget(deck, player, target):
    """
    Requirements: challengesCard(), assassinateTarget()
    """
    postMessage(groupChannel, "%s calls the :bow_and_arrow: assassins on %s!" % (player.name, target.name))
    postMessage(target.slackId, "%s is trying to assassinate you... what do you do?" % player.name)
    postMessage(target.slackId, "Allow | Block (with Contessa) | Challenge")
    playerInput = getUserInput(target.slackChannel)
    if playerInput == "Allow":
        postMessage(target.slackId, "I see you're taking it like a wuss huh?")
        assassinateTarget(player, target)

    elif playerInput == "Block (with Contessa)":
        # Challenger claims to have a Contessa
        postMessage(groupChannel, "%s claims to have a Contessa, any challengers (30 seconds to respond)?" % target.name)
        postMessage(groupChannel, "Say: 'Challenge'")
        challengerInput = ""
        challengerInput = getUserInputTimeout(groupChannel, 30)
        if challengerInput[0] == "Challenge":
            challengerUser = getPlayerFromSlackId(players, challengerInput[1])
            # print challengerInput[1]
            challengesCard(gameDeck, challengerUser, players[player], "Contessa")
            if challengesCard(gameDeck, challengerUser, players[player], "Contessa") == False:
                postMessage(groupChannel, "Blocks Assassin with Contessa")
            else:
                assassinateTarget(player, target)
        else:
            postMessage(groupChannel, "%s blocks Assassin with Contessa" % target.name)

    elif playerInput == "Challenge":
        challengesCard(deck, target, player, "Assassin")
        if challengesCard(deck, target, player, "Assassin") == False:
            assassinateTarget(player, target)           
    else:
        postMessage(target.slackId, "I don't understand you... but I'll assume you like getting robbed")
        assassinateTarget(player, target)

def action_exchangeCards(deck, player):
    """
    Requirements: challengesCard(), exchangeCards()
    """
    # Challenger claims to have a Ambassador
    postMessage(groupChannel, "%s claims to have an Ambassador, any challengers (30 seconds to respond)?" % player.name)
    postMessage(groupChannel, "Say: 'Challenge'")
    challengerInput = ""
    challengerInput = getUserInputTimeout(groupChannel, 30)
    if challengerInput[0] == "Challenge":
        challengerUser = getPlayerFromSlackId(players, challengerInput[1])
        # print challengerInput[1]
        challengesCard(gameDeck, challengerUser, players[player], "Ambassador")
        if challengesCard(gameDeck, challengerUser, players[player], "Ambassador") == False:
            postMessage(groupChannel, "Turns out he was posing as an Ambassador... a fake!")
        else:
            exchangeCards(deck, player)
    else:
        exchangeCards(deck, player)
    return None

# Status and Display related functions.
# These should not alter or modify any data

def selfStatusUpdate(player):
    cards = player.cards
    deadCards = player.deadCards
    gold = player.gold
    postMessage(player.slackId, ":moneybag:: %s gold" % gold)
    if len(cards) == 2:
        postMessage(player.slackId, ":flower_playing_cards:: {}, {}".format(*cards))
    else:
        postMessage(player.slackId, ":flower_playing_cards:: {}, {}[DEAD]".format(*(cards, deadCards)))
            

def displayBoard(players):
    """
    Displays all the status of every player:
    Influence Left and Cards
    Gold
    """
    displayResult = ""
    for player in players:
        if players[player].influence == 0:
            displayResult += "%s defeated with cards: %s" % (players[player].name, 
                players[player].deadCards)
            displayResult += "\n"
        elif players[player].influence == 1:
            displayResult += "%s: 1 life, " % (players[player].name)
            displayResult += "{}[DEAD], ".format(*players[player].deadCards)
            displayResult += "and %s gold" % (players[player].gold)
            displayResult += "\n"
        else: 
            displayResult += "%s: 2 lives and %s gold" % (
                players[player].name, players[player].gold)
            displayResult += "\n"

    return displayResult

# ----------------------------------------------
# ---------- controller functions end ----------
# ----------------------------------------------

# Game Starts:
postMessage(groupChannel, "-----------------------------------------")
postMessage(groupChannel, "Let the Coup BEGIN!")
postMessage(groupChannel, "Listen up kids, I'm an alpha :octopus:, so if you can't follow my instructions to the tee, TOUGH! :triumph: ")
print "-----------------------------------------"

# How many players?
userListDic = compileUserListDic()

postMessage(groupChannel, "Who's in? Type 'join game'")
newGamePlayersId = []
newGamePlayersName = []
timeoutTimer = 0
sc.rtm_connect()
while timeoutTimer < 30:
    new_evts = sc.rtm_read()
    for evt in new_evts:
        print(evt)
        if "type" in evt:
            if evt["type"] == "message" and "text" in evt and evt["channel"] == groupChannel:
                message = evt["text"]
                user = evt["user"]
                if message == 'join game':                
                    newGamePlayersId.append(user)
                    postMessage(groupChannel, "%s successfully joined" % userListDic[user][0])
                    newGamePlayersName.append(userListDic[user][0])
                    print sc.api_call("im.open", user=user)
                print newGamePlayersId
    time.sleep(1)
    timeoutTimer += 1

print newGamePlayersName
print newGamePlayersId

# Exit if not enough players
if len(newGamePlayersId) < 2:
    postMessage(groupChannel, "Not enough players :sob:")
    exit()

postMessage(groupChannel, "Starting a new game with: %s" % newGamePlayersName)

# Initialize variables
# 1. Shuffle Deck
gameDeck = odeck[:]
gameDeck = shuffleDeck(gameDeck)
print gameDeck

# 2. Create Player Objects
players = {}
for player in newGamePlayersId:
    players[userListDic[player][0]] = makePlayer(gameDeck, 
        userListDic[player][0], player, userListDic[player][2])

for player in players:
    selfStatusUpdate(players[player])

# print players
# goldAccounting(players['charlie'], 20)
# coupTarget(players['playerCharlie'], players['playerAynRand'])
# coupTarget(players['playerCharlie'], players['playerAynRand'])
# displayBoard(players)

# giveUpInfluence(players['playeruser_charlie'])
# challengesCard(gameDeck, players['playeruser_charlie'], players['playeruser_fakecharlie'], "Duke")

# Begin Game
print "-----------------------------------------"
postMessage(groupChannel, "-----------------------------------------")
while True:
    for player in players:
        # New turn
        postMessage(groupChannel, displayBoard(players))
        
        # Create a list of potential targets
        potentialTargets = []
        for otherplayer in players:
            if isPlayerAlive(players[otherplayer]) == True and otherplayer != player:
                potentialTargets.append(players[otherplayer].name)

        # Proceed if player is still alive
        if isPlayerAlive(players[player]):
            postMessage(groupChannel, ":arrow_right: %s's turn!" % players[player].name)
            postMessage(players[player].slackId, ":arrow_right: your move, what will you do?")
            selfStatusUpdate(players[player])
            postMessage(players[player].slackId, "Income | Foreign Aid | Coup | Tax | Steal | Assassinate | Exchange")
            playerTurnTrigger = True
            while playerTurnTrigger == True:
                playerInput = getUserInput(players[player].slackChannel)
                print "----------------HERE-------------------------"
                print playerInput
                # Player Inputs
                # For every other player, Accept | Challenge options + more
                if playerInput == "Income":
                    income(players[player])
                    postMessage(groupChannel, "%s takes Income, +1 gold" % players[player].name)
                    postMessage(players[player].slackId, "Your have gained +1 gold from Income")
                    playerTurnTrigger = False

                elif playerInput == "Foreign Aid":
                    postMessage(groupChannel, "%s claims Foreign Aid, any challengers (30 seconds to respond)?" % players[player].name)
                    postMessage(groupChannel, "Say: 'I have a Duke'")
                    challengerInput = ""
                    challengerInput = getUserInputTimeout(groupChannel, 30)
                    if challengerInput[0] != 'I have a Duke':
                        challengerUser = getPlayerFromSlackId(players, challengerInput[1])
                        # No challenges:
                        postMessage(groupChannel, "30 seconds up! I see no challengers...'")
                        foreignAid(players[player])
                        postMessage(groupChannel, "%s takes Foreign Aid, +2 gold" % players[player].name)
                        postMessage(players[player].slackId, "Your have gained +2 gold from Foreign Aid")
                    else:
                        # Challenger claims to have a Duke
                        postMessage(groupChannel, "%s claims to have a Duke, any challengers (30 seconds to respond)?" % challengerUser.name)
                        postMessage(groupChannel, "Say: 'Challenge'")
                        challengerInput2 = ""
                        challengerInput2 = getUserInputTimeout(groupChannel, 30)
                        if challengerInput[0] == "Challenge":
                            challengerUser2 = getPlayerFromSlackId(players, challengerInput[1])
                            # Check if there is Duke
                            # print challengerInput[1]
                            challengesCard(gameDeck, challengerUser2, challengerUser, "Duke")
                            if challengesCard(gameDeck, challengerUser2, challengerUser, "Duke") == False:
                                postMessage(groupChannel, "Blocked Foreign Aid with Duke")
                            else:
                                foreignAid(players[player])
                        else:
                            postMessage(groupChannel, "Blocked Foreign Aid with Duke")

                    playerTurnTrigger = False

                elif playerInput == "Coup":
                    if haveEnoughGold(players[player], 7) == True:
                        postMessage(players[player].slackId, 
                            "You can coup: " + ' or '.join(potentialTargets))
                        playerTargetInput = getUserInput(players[player].slackChannel)
                        coupTarget(players[player], players[str(playerTargetInput)])
                        selfStatusUpdate(players[player])
                        playerTurnTrigger = False
                    else:
                        postMessage(players[player].slackId, "??? You're... too poor brah...")

                elif playerInput == "Tax":
                    postMessage(groupChannel, "%s declares Tax abusing his power as Duke, any challengers (30 seconds to respond)?" % players[player].name)
                    postMessage(groupChannel, "Say: 'Challenge'")
                    challengerInput = ""
                    challengerInput = getUserInputTimeout(groupChannel, 30)
                    if challengerInput[0] == "Challenge":
                        challengerUser = getPlayerFromSlackId(players, challengerInput[1])
                        # Check if there is Duke
                        # print challengerInput[1]
                        challengesCard(gameDeck, challengerUser, players[player], "Duke")
                    else:
                        postMessage(groupChannel, "%s abused his power as a Duke and taxed the poor, good job! +3 Gold" % players[player].name)
                        taxDuke(players[player])
                    playerTurnTrigger = False

                elif playerInput == "Steal":
                    postMessage(players[player].slackId, 
                        "You can steal from: " + ' or '.join(potentialTargets))                    
                    playerTargetInput = getUserInput(players[player].slackChannel)
                    action_stealTarget(gameDeck, players[player], players[str(playerTargetInput)])
                    playerTurnTrigger = False

                elif playerInput == "Assassinate":
                    if haveEnoughGold(players[player], 3) == True:
                        postMessage(players[player].slackId, 
                            "You can assassinate: " + ' or '.join(potentialTargets))
                        playerTargetInput = getUserInput(players[player].slackChannel)
                        action_assassinateTarget(gameDeck, players[player], players[str(playerTargetInput)])
                        playerTurnTrigger = False
                    else:
                        postMessage(players[player].slackId, "??? You're... too poor brah...")

                elif playerInput == "Exchange":
                    action_exchangeCards(gameDeck, players[player])
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
