from twitch_chat_irc import twitch_chat_irc as irc
from platform_connections import Twitch
import sys



CHANNEL_NAME = 'bonkary'

twitch = Twitch()
twitch.set_channel_name(CHANNEL_NAME)

def print_message(msg):
    print(msg['message'])
    if msg['message'] == 'exit':
        sys.exit(0)

try:
    while True:
        allText = []
        messages = twitch.listen(on_message=print_message)
        
except KeyboardInterrupt:
    sys.exit(0)


