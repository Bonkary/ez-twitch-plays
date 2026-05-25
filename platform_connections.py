from twitch_chat_irc import twitch_chat_irc as irc
from types import FunctionType



class Twitch():
    def __init__(self, channel_name: str | None = None):
        self._channelName = channel_name
        self._chat = irc.TwitchChatIRC()
    
    def set_channel_name(self, channel_name: str):
        self._channelName = channel_name
        
    def listen(self, on_message: FunctionType = None) -> None:
        if self._channelName:
            return self._chat.listen(self._channelName, on_message=on_message)
        else:
            raise ValueError("There is no channel name set...")







