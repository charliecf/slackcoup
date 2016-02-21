import random

# Coup Game
"""
Player Actions (During Turn):
+ Income (+1 Gold)
+ Foreign Aid (+2 Gold)
+ Coup (-7 Gold, coup _target_)
+ Assassin (-3 Gold, assassinate _target_)
+ Steal (+2 Gold from _target_ -2 Gold from _target_)
+ Tax (+3 Gold)
+ Exchange (Draw two character cards from the Court (the deck), choose which 
    (if any) to exchange with your face-down characters, then return two.)

Player Actions (During Opponent Turn):
+ Allow
+ Challenge

Player Action (if being assassinated):
+ Block with Contessa

Player Action (if being robbed):
+ Block with Captain
+ Block with Ambassador

Player Action (if _player_ Foreign Aid):
+ Block with Duke

"""

# Original deck
odeck = ['Assassin', 'Assassin', 'Assassin', 
        'Captain', 'Captain', 'Captain',
        'Duke', 'Duke', 'Duke',
        'Ambassador', 'Ambassador', 'Ambassador',
        'Contessa', 'Contessa', 'Contessa']

# Create new/temporary deck for the current game, 
# all deck manipulation should be done on gameDeck
gameDeck = odeck[:]

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
    gold = 0
    cards = []
    influence = 0
    isAlive = True

    def __init__(self, name, gold, cards, influence):
        self.name = name
        self.gold = gold
        self.cards = cards
        self.influence = influence

# Initialize a player, this occurs at the start of a game
def makePlayer(deck, name):
    """
    Start with 2 coins
    2 random cards
    Influence would equal to number of cards (vice versa), should equal 2
    """
    gold = 2
    cards = []
    influence = 2
    player = Player(name, gold, cards, influence)
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
    print "dealing %s cards..." % numCards
    for card in range(numCards):
        card = deck[0]
        deck.pop(0)
        player.cards.append(card)
        print "added %s card for %s" % (card, player.name)
    print player.cards
    # return player.cards

def returnCardsToDeck(deck, player, card):
    """
    deck = list
    player = object
    card = string

    This action is used for:
    When player uses exchange ability
    When player win a challenge and need to draw new card
    """
    return None

def isPlayerDead(player):
    return None

def removeInfluence(target):
    return None

def coupTarget(player, target):
    # player -7 coins
    # Remove influence from target
    return None

def assassinateTarget(player, target):
    # player -3 coins
    # Attempts to assassinate target
        # IF successful: remove influence from target
        # ELSE: None
    return None

def stealTarget(player, target):
    # player attempts to steal from target
        # IF successful: -2 coins from target, player +2 coins
        # ELSE: None
    return None

def income(player):
    # player +1 coin
    return None


def foreignAid(player):
    # player attempts to foreign aid
        # IF successful: player +2 coins
        # ELSE: None
    return None

def taxDuke(player):
    # player attempts to tax
        # IF successful player +3 coins
        # Else: None
    return None

def exchangeCards(player):
    return None

# ======== GAME MASTER TOOLS ======== 
def killPlayer(player):
    players[player].influence = 0
    players[player].isAlive = False
    print vars(players[player])

print gameDeck
gameDeck = shuffleDeck(gameDeck)
print gameDeck


# Game Starts:
print "Let the Coup BEGIN!"
print "-----------------------------------------"
# How many players?
temp_playerInputPlayers = 3
temp_playerInputNames = ['Charlie', 'AynRand', 'Frankenstein']
# Initialize variables
# 1. Shuffle Deck
gameDeck = shuffleDeck(gameDeck)
print gameDeck

# 2. Create Player Objects
players = {}
for player in temp_playerInputNames:
    print "creating %s player..." % player
    players["player{0}".format(player)] = makePlayer(gameDeck, player)
print players

# playerCharlie = makePlayer(gameDeck, 'Charlie')
# playerAynRand = makePlayer(gameDeck, 'AynRand')
# playerFrankenstein = makePlayer(gameDeck, 'Frankenstein')
print ""
print gameDeck

print ""
print "Killing Charlie..."
players['playerCharlie'].isAlive = False
print "%s is alive? %s" % (players['playerCharlie'].name, players['playerCharlie'].isAlive)
print "%s is alive? %s" % (players['playerAynRand'].name, players['playerAynRand'].isAlive)

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
