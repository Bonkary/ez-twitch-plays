from twitch_chat_irc import twitch_chat_irc as irc
from types import FunctionType
import time
import sys
from constants import *

class Twitch():
    '''
    Handles communications with Twitch.
    
    Arguments:
        channel_name - The name of the Twitch channel to connect to.
    '''  
    def __init__(self, channel_name: str | None = None):
        self._channelName = channel_name
        self._chat = irc.TwitchChatIRC(suppress_print=False)
    
    def set_channel_name(self, channel_name: str):
        '''Sets a new channel name.'''
        self._channelName = channel_name
        
    def listen(self, on_message: FunctionType = None) -> None:
        '''
        Listens to the Twitch chat via IRC and executes a function call when a message is detected.
        
        Arguments:
            on_message - The function to call when a new message is heard.
        '''
        if self._channelName:
            try:
                self._chat.listen(self._channelName, on_message=on_message)
            except OSError:
                if KILL_THREADS_FLAG.is_set():
                    print("killed") # DEV
        else:
            return
        
    def close(self) -> None:
        '''Close the IRC connection with Twitch'''
        self._chat.close_connection()
        time.sleep(2)


# TODO: Add YouTube eventually. Seems like it'll take a lot of time... so it's a future me problem.
class YouTube():
    def __init__(self, channel_name: str | None = None):
        raise NotImplementedError("Sorry, YouTube connection hasnt been done yet :/")




