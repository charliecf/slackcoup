"""
Charlie's problem, seems to be a cygwin problem... that I have yet to fix
"""
# import sys
# sys.path.append('c:\python27\lib\site-packages')

import time
import pprint
from slackclient import SlackClient

token = "xoxb-22371870822-R4NMrSgKKyldo4xJj7nQNM4F" # Random Projects -- will need to change in the future
sc = SlackClient(token)
print token
print "-------------------"

print sc.api_call("api.test")
print sc.api_call("im.open", user="U0NAWS465")
print sc.api_call("im.open", user="U0NBKF2BZ") # opens the channel for dm to a user

user_charlie = "U0NAWS465"
user_fakecharlie = "U0NCAB0DD"
user_jeff = "U0NBKF2BZ"
user_yitong = "U0NBKF2BZ"
greeting = "Hello!\nNice to meet you."
# print sc.api_call("chat.postMessage", as_user="true:", channel=user_charlie, text=greeting)
# print sc.api_call("chat.postMessage", as_user="true:", channel=user_yitong, text=greeting)
# print sc.api_call("chat.postMessage", as_user="true:", channel="C0NAXDD7S", text=greeting)

# To the channel
message = "Hello team, let's start a game of Coup!"
# print sc.api_call("chat.postMessage", channel="C0NAXDD7S", text=message, as_user="true")

# if sc.rtm_connect():
#     while True:
#         print sc.rtm_read()
#         time.sleep(1)
# else:
#     print "Connection Failed, invalid token?"

l = [{u'text': u'So only this channel... hmm', u'ts': u'1456102030.000055', u'user': u'U0NAWS465', u'team': u'T0NAWQP09', u'type': u'message', u'channel': u'C0NAXDD7S'}]
pprint.pprint(l)
if 'only' in l:
    print "It works!!!!!"
else:
    print "poop............."