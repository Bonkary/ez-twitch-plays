from twitch_chat_irc import twitch_chat_irc as irc
from types import FunctionType
import time
import sys


class Killer():
    isKilled = False
    
    def kill(self):
        self.isKilled = True

KILLER = Killer() # THIS ENDED THE SEGFAULT. DONT ASK WHY. IT WAS A BIG PROBLEM FOR A WHILE AND IM JUST GLAD ITS OVER.

class Twitch():
    def __init__(self, channel_name: str | None = None):
        self._channelName = channel_name
        self._chat = irc.TwitchChatIRC(suppress_print=False)
    
    def set_channel_name(self, channel_name: str):
        self._channelName = channel_name
        
    def listen(self, on_message: FunctionType = None) -> None:
        if self._channelName:
            try:
                self._chat.listen(self._channelName, on_message=on_message)
            except OSError:
                if KILLER.isKilled:
                    print("killed")
        else:
            return
        
    def close(self) -> None:
        self._chat.close_connection()
        time.sleep(2)







