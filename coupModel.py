import random

# Player Object
class Player(object):
    """
    Player name
    Number of Gold
    Cards they have
    Influence/Cards left
    Still alive (in the game)
    """
    name = ""
    slackId = ""
    slackChannel = ""
    gold = 0
    cards = []
    deadCards = []
    influence = 0
    # isAlive = True

    def __init__(self, name, slackId, slackChannel, gold, cards, influence):
        self.name = name
        self.slackId = slackId
        self.slackChannel = slackChannel
        self.gold = gold
        self.cards = cards
        self.influence = influence

# Initialize a player, this occurs at the start of a game
def makePlayer(deck, name, slackId, slackChannel):
    """
    Requirements: dealCards()

    Start with 2 coins
    2 random cards
    Influence would equal to number of cards (vice versa), should equal 2
    """
    gold = 2
    cards = []
    influence = 2
    player = Player(name, slackId, slackChannel, gold, cards, influence)
    dealCards(deck, player, 2)
    print vars(player) # for logging purposes only
    return player

def shuffleDeck(deck):
    shuffledDeck = []
    for i in range(len(deck)):
        element = random.choice(deck)
        deck.remove(element)
        shuffledDeck.append(element)
    return shuffledDeck

# Deal numCards of cards from deck to player
def dealCards(deck, player, numCards):
    """
    deck = list
    player = object
    numCards = int

    This action occurs in multiple areas:
    When player is initialized (makePlayer)
    When player uses exchange ability
    When player win a challenge and need to draw new card
    """
    print "dealing %s cards to %s..." % (numCards, player.name)
    for card in range(numCards):
        card = deck[0]
        deck.pop(0)
        player.cards.append(card)
        print "added %s card for %s" % (card, player.name)
    print player.cards

def doesPlayerHaveCard(player, card):
    if card in player.cards:
        return True
    else:
        return False 

def returnCardsToDeck(deck, player, card):
    """
    Requirements: doesPlayerHaveCard()

    deck = list
    player = object
    card = string

    This action is used for:
    When player uses exchange ability
    When player win a challenge and need to draw new card
    """
    if doesPlayerHaveCard(player, card) == True:
        print "%s returns 1 card back into the deck..." % (player)
        player.cards.remove(card)
        deck.append(card)
    else:
        print "Error: %s does not have %s card" % (player, card)

def isPlayerAlive(player):
    if player.influence > 0:
        return True
    else:
        return False

def removeInfluence(player):
    """
    Requirements: isPlayerAlive()
    """
    if isPlayerAlive(player) == True:
        player.influence -= 1
    else:
        print "Player is dead already"
        return None

def giveUpInfluence(player):
    """
    Requirements: doesPlayerHaveCard(), removeInfluence()

    player has lost an influence, needs to pick an influence to give up
    """
    print "%s has lost an influence, please pick an influence to lose" % (player.name)
    while True:
        card = raw_input("> ")
        if doesPlayerHaveCard(player, card):
            print "%s has given up his %s" % (player.name, card)
            player.cards.remove(card)
            player.deadCards.append(card)
            removeInfluence(player)
            return
        else:
            print "You don't have a %s" % (card)

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
            displayResult += "%s has 1 life left, with %s and %s [DEAD] with %s gold" % (
                players[player].name, players[player].cards, 
                players[player].deadCards, players[player].gold)
            displayResult += "\n"
        else: 
            displayResult += "%s has 2 lives left, with %s with %s gold" % (players[player].name, 
                players[player].cards, players[player].gold)
            displayResult += "\n"

    return displayResult

def goldAccounting(player, amount):
    player.gold += int(amount)
    if player.gold < 0:
        player.gold = 0
    print "%s now has %s gold" % (player.name, player.gold)

def haveEnoughGold(player, amount):
    if player.gold >= int(amount):
        return True
    else:
        return False

def coupTarget(player, target):
    """
    Requirements: haveEnoughGold(), goldAccounting(), giveUpInfluence()

    player -7 coins
    Remove influence from target
    not possible to block or challenge
    """
    if haveEnoughGold(player, 7):
        goldAccounting(player, -7)
        giveUpInfluence(target)
    else:
        print "You do not have enough money to coup... nice try..."

def assassinateTarget(player, target):
    """
    Requirements: haveEnoughGold(), goldAccounting(), giveUpInfluence()

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

def stealTarget(player, target):
    """
    player attempts to steal from target (Captain ability)
        IF successful: -2 coins from target, player +2 coins
        ELSE: None
    """
    if target.gold == 0:
        print "%s stole from a broke man... (0 gold) from %s" % (player, target)
    elif target.gold == 1:
        print "%s stole 1 gold from %s" % (player, target)
        goldAccounting(player, +1)
        goldAccounting(target, -2)
    else:
        print "%s stole 2 gold from %s" % (player, target)
        goldAccounting(player, +2)
        goldAccounting(target, -2)

def income(player):
    """
    Requirements: goldAccounting()

    player +1 coin
    not possible to block or challenge
    """
    print "%s used income, +1 Gold" % player.name
    goldAccounting(player, 1)

def foreignAid(player):
    """
    Requirements: goldAccounting()

    player attempts to foreign aid
        IF successful: player +2 coins
        ELSE: None
    """
    print "%s used foreign aid, +2 Gold" % player.name
    goldAccounting(player, 2)

def taxDuke(player):
    """
    Requirements: goldAccounting()

    player attempts to tax (Duke ability)
        IF successful player +3 coins
        ELSE: None
    """
    print "%s abused his power as a Duke and taxed the poor, good job! +3 Gold" % player.name
    goldAccounting(player, 3)

def exchangeCards(deck, player):
    """
    Requirements: dealCards(), returnCardsToDeck()

    player attempts to exchange cards (Ambassador ability)
        IF successful player +2 cards, return 2 cards
        ELSE: None
    """
    dealCards(deck, player, 2)
    while len(player.cards) != 2:
        card = raw_input("What card would you like to return? > ")
        returnCardsToDeck(deck, player, card)
    print "completed exchange!"

# ======== GAME MASTER TOOLS ======== 
def killPlayer(player):
    players[player].influence = 0
    players[player].isAlive = False
    print vars(players[player])

