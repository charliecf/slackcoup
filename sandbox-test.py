import time
import pprint
import json
from slackclient import SlackClient

token = "xoxb-22371870822-R4NMrSgKKyldo4xJj7nQNM4F" # Random Projects -- will need to change in the future
sc = SlackClient(token)
print token
print "-------------------"

print sc.api_call("api.test")

usersList = json.loads(sc.api_call("users.list"))['members']

for user in usersList:
	print user['name'], user['id']

imList = json.loads(sc.api_call("im.list"))['ims']

for im in imList:
	print im['user'], im['id']

userListDic = {}

exit()

for user in usersList:
	name = user['name']
	slackId = user['id']
	for im in imList:
		if im['user'] == slackId:
			channelId = im['id']
	userListDic[slackId] = [{'name': name}, slackId, channelId]

print userListDic

print userListDic['U0NAWS465'][0]