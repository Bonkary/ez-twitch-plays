import socket
import re
import random
import time
import constants as cnst

# I started this using DougDoug's code, but now I think it's barely recognizable. 
# I had to get it to work within seperate threads.
# Thanks, DougDoug and Ottomated and DDark and Wituz
MAX_TIME_TO_WAIT_FOR_LOGIN = 3
YOUTUBE_FETCH_INTERVAL = 1
REGEX_PATTERN = b'^(?::(?:([^ !\r\n]+)![^ \r\n]*|[^ \r\n]*) )?([^ \r\n]+)(?: ([^:\r\n]*))?(?: :([^\r\n]*))?\r\n'
REGEX_CORE = re.compile(REGEX_PATTERN, re.MULTILINE)
IRC_HOST = 'irc.chat.twitch.tv'
IRC_PORT = 6667
NO_NEW_MESSAGE_TIMEOUT = 5

IRC_CMDS_TO_IGNORE = ['JOIN', '001', '002', '003', '004', '375', '372', '376', '353', '366']

NAME = 1
COMMAND = 2
PARAMS = 3
TRAILING = 4


class Twitch():
    '''
    Handles the communications with Twitch.
    
    Arguments:
        channel_name - Name of the Twitch channel to connect to.
    '''
    
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._loginOk = False
        self._channelName = ''
        self._loginTimestamp = 0
        self._partial = []
    
    def connect(self, *, channel_name: str) -> None:
        '''Connect to the socket and login to Twitch'''
        print("Connecting to Twitch...")
        self._channelName = channel_name
        try:
            self._socket.connect((IRC_HOST, IRC_PORT))
        except OSError as err:
            if 'already connected' in str(err):
                print("already connected")
                pass
            else:
                print(f"idk what went wrong: {err}")
        self.login()
        
    def login(self) -> None:
        '''Creates a random username to login all sneaky-like'''
        user = 'justinfan%i' % random.randint(10_000, 99_999)
        try:
            self._socket.send(('PASS asdf\r\nNICK %s\r\n' % user).encode())
        except ConnectionAbortedError:
            TWITCH_MANAGER.reconnect()
        self._loginTimestamp = time.time()
        
        self._socket.settimeout(10)
        ircMessage = self._socket.recv(4096)
        matches = list(REGEX_CORE.finditer(ircMessage))
        for match in matches:
            command = (match.group(COMMAND) or b'').decode(errors='replace')
            if (command == '001' or command == 'JOIN') and not self._loginOk:
                bytesSent = self._socket.send((f'JOIN #{self._channelName}\r\n').encode())
                if bytesSent > 0:
                        print(f'Successfully logged in. Listening to channel: {self._channelName}')
                        self._loginOk = True
                else:
                    print("FAILED TO LOGIN")
            else:
                continue
    
    def is_connected(self) -> bool:
        isConnected = False
        check = None
        try:
            check = self._socket.recv(1024)
            if check:
                isConnected = True
        except OSError as err:
            if 'not connected' in str(err):
                isConnected = False
            else:
                print(f"Idk what the hell went wrong: {err}")

        return isConnected
    
    def reconnect(self, *, delay: int = 0) -> None:
        '''
        Attempt to reconnect to Twitch.
        
        Arguments:
            delay - Value of the delay between reconnect attempts
        '''
        time.sleep(delay)
        self.connect(self._channelName)
    
    def send(self, data: bytes) -> None:
        self._socket.send(data)
    
    def next_irc_message(self) -> bytes | None:
        try:
            newMessage = self._socket.recv(4096)
        except socket.timeout:
            newMessage = self.next_irc_message()
        except ConnectionAbortedError:
            self.reconnect()

        return newMessage
    
    def pong(self) -> None:
        self.send(b'PONG :tmi.twitch.tv\r\n')

