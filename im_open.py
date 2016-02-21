"""
Charlie's problem, seems to be a cygwin problem... that I have yet to fix
"""
# import sys
# sys.path.append('c:\python27\lib\site-packages')

from slackclient import SlackClient

token = "xoxb-22367344306-1zqg2wHJSJUPt9EqbbsJdGbH"
sc = SlackClient(token)
print token
print "-------------------"
print sc.api_call("api.test")
print sc.api_call("im.open", user="U0E467GTG")

chan = "U0E467GTG"
greeting = "Hello!\nNice to meet you."
print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=greeting)
