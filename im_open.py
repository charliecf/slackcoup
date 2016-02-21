"""
Charlie's problem, seems to be a cygwin problem... that I have yet to fix
"""
# import sys
# sys.path.append('c:\python27\lib\site-packages')

from slackclient import SlackClient

token = "xoxb-22371870822-R4NMrSgKKyldo4xJj7nQNM4F" # Random Projects -- will need to change in the future
sc = SlackClient(token)
print token
print "-------------------"

print sc.api_call("api.test")
print sc.api_call("im.open", user="U0NAWS465")

user_charlie = "U0NAWS465"
user_yitong = "T0NAWQP09"
greeting = "Hello!\nNice to meet you."
print sc.api_call("chat.postMessage", as_user="true:", channel=user_charlie, text=greeting)

