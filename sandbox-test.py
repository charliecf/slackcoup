from controller import *

print sc.api_call("im.open", user="U0NAWS465") # Charlie
print sc.api_call("im.open", user="U0NCAB0DD") # fakeCharlie
print sc.api_call("im.open", user="U0NBKF2BZ") # Jeff
print sc.api_call("im.open", user="U0NAWTM9D") # Yitong

user_charlie = "U0NAWS465"
user_fakecharlie = "U0NCAB0DD"
user_jeff = "U0NBKF2BZ"
user_yitong = "U0NAWTM9D"

newGamePlayersId = ['U0NAWS465', 'U0NCAB0DD']
print newGamePlayersId

# 2. Create Player Objects
players = {}
for player in newGamePlayersId:
    players[userListDic[player][0]] = makePlayer(gameDeck, 
        userListDic[player][0], player, userListDic[player][2])

for player in players:
    selfStatusUpdate(players[player])