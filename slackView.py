import time
import pprint
from slackclient import SlackClient

token = "xoxb-22371870822-R4NMrSgKKyldo4xJj7nQNM4F" # Random Projects -- will need to change in the future
sc = SlackClient(token)

print sc.api_call("api.test")
print sc.api_call("im.open", user="U0NAWS465") # Charlie
print sc.api_call("im.open", user="U0NCAB0DD") # fakeCharlie
print sc.api_call("im.open", user="U0NBKF2BZ") # Jeff
print sc.api_call("im.open", user="U0NBKF2BZ") # Yitong

user_charlie = "U0NAWS465"
user_fakecharlie = "U0NCAB0DD"
user_jeff = "U0NBKF2BZ"
user_yitong = "U0NBKF2BZ"

groupChannel = "C0NCQ4K4K" # coup-game-test
# groupChannel = "C0NAXDD7S"

def postMessage(channel, message):
	print sc.api_call("chat.postMessage", channel=channel, text=message, as_user="true")

def getUserInput(channel):
	sc.rtm_connect()
	while True:
	    new_evts = sc.rtm_read()
	    # print new_evts
	    for evt in new_evts:
	        print(evt)
	        if "type" in evt:
	            if evt["type"] == "message" and "text" in evt:
	                message = evt["text"]
	                return message
	    time.sleep(3)


# postMesage(groupChannel, "msgGroupFunc Test\n second line?")