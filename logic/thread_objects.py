import pydirectinput
import time
from platform_connection import *
from PySide6.QtCore import QThread, QThreadPool, QRunnable, QObject, Slot, Signal
import logic.controller as cntrls
import random
from typing import Literal
from constants import *

THREAD_POOL = QThreadPool.globalInstance()
EXEC_THREAD = QThread()

def extract_chat_message(irc_message: bytes) -> dict[str:str]:
    message: dict = None
    matches = list(REGEX_CORE.finditer(irc_message))
    for match in matches:
        print(match)
        print("################################################")
        try:
            messageData = {
                'name': (match.group(NAME) or b'').decode(errors='replace'),
                'command':  (match.group(COMMAND) or b'').decode(errors='replace'),
                'params':   list(map(lambda p: p.decode(errors='replace'), (match.group(PARAMS) or b'').split(b' '))),
                'trailing': (match.group(TRAILING) or b'').decode(errors='replace'),
                }
        except IndexError as err:
            print("extract: ", err)
    
    if not messageData['command'] in IRC_CMDS_TO_IGNORE:
        match messageData['command']:
            case 'PRIVMSG':
                message = {
                    'username': messageData['name'],
                    'text': messageData['trailing']
                }
            case 'PING':
                TWITCH.pong()
            case _:
                pass
    return message

def get_cmd(cmd: str, preset: dict) -> str:
    key: str | tuple = None
    cmdType: str = None
    controls = preset[CONTROLS]
    combos = preset[COMBO_BUTTONS]
    
    for button in controls:
        try:
            if button == 'combo_buttons':
                continue
            pressCmd = controls[button][PRESS]
            holdCmd = controls[button][HOLD]
            if cmd in [pressCmd, holdCmd]:
                key = controls[button][KEY]
                cmdType = PRESS if cmd == pressCmd else HOLD
                break
            else:
                continue
        except (ValueError, AttributeError):
            pass
    
    if not key:
        for combo in combos:
            pressCmd = combo[PRESS]
            holdCmd = combo[HOLD]
            if cmd in [pressCmd, holdCmd]:
                key = (combo[KEY_1], combo[KEY_2])
                cmdType = PRESS if cmd == pressCmd else HOLD
                break
    return key, cmdType, controls[button][PROBABILITY]


def pull_chat(self) -> None:
    pass



class WorkerSignals(QObject):
    alert = Signal(str)
    paused = Signal(bool)
    running = Signal(bool)
    send = Signal()
    execute = Signal()

class ExecuteCommand(QRunnable):
    def __init__(self, key: str | tuple, cmdType: Literal['press', 'hold']):
        super().__init__()
        self._key = key
        self._cmdType = cmdType
        
    def run(self) -> None:
        if type(self._key) == tuple:
            if self._cmdType == PRESS:
                cntrls.press_combo_key(self._key)
            elif self._cmdType == HOLD:
                cntrls.hold_combo_key(self._key)
        else:
            if self._cmdType == PRESS:
                cntrls.press_key(self._key)
            elif self._cmdType == HOLD:
                cntrls.hold_key(self._key)
        

class KeypressExecutor(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ircMessages: list[bytes] = []    
        self._chatMessages: list[dict] = []
        self.isStarted = False
        self._isKilled = False
        self.isPaused = False
        self.signals = WorkerSignals()
        self.preset: str = None
    
    def run(self) -> None:
        while not self._isKilled:
            if not self.isPaused:
                # try:
                ircMessage = TWITCH.next_irc_message()
                if ircMessage:
                    message = extract_chat_message(ircMessage)
                    if not message:
                        continue
                    if message['text'] in self.preset[VALID_CMDS]: 
                        key, cmdType, prob = get_cmd(cmd=message['text'], preset=self.preset)
                        if random.randint(1,100) <= prob:
                            if key and pydirectinput.is_valid_key(key):
                                worker = ExecuteCommand(key, cmdType)
                                THREAD_POOL.start(worker)
                        
                # except Exception as err:
                #     print("oops: ", err)
                
    def kill(self) -> None:
        self._isKilled = True
    
    def pause(self) -> None:
        self.isPaused = True
    
    def resume(self) -> None:
        self.isPaused = False
    
    def set_preset(self, preset: dict) -> None:
        self.preset = preset

class Listener(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = WorkerSignals()
        self._isKilled = False
        self._isPaused = False
    
    def run(self) -> None:
        while not self._isKilled:
            if not self._isPaused:
                ircMessage = TWITCH_MANAGER.next_irc_message()
                if ircMessage:
                    pass
    
    def kill(self) -> None:
        self._isKilled = True
    
    def pause(self) -> None:
        self._isPaused = True
        
    def resume(self) -> None:
        self._isPaused = False
    
    
    
    
    
    
    
    