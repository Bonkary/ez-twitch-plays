from PySide6.QtCore import QRunnable, QObject, Slot, Signal, QEvent
if not ON_MAC:
    import logic.controller as cntrls
from typing import Literal
from constants import *
from platform_connections import Twitch
from configurations import PRESETS
import random
from threading import Event
import logic.controller as cntrl


def get_key(preset_name: str, chat_cmd: str) -> tuple[str, str, int | tuple, str, int]:
    '''
    Get the key to be pressed based on the chat command.
    
    Arguments:
        preset_name - The name of the Preset to look into.
        chat_cmd - The chat message of the command.
    '''
    preset: dict = PRESETS[preset_name]
    singles: list[dict] = preset[strs.SINGLE]
    combos: list[dict] = preset[strs.COMBO]
    key: str | tuple = None
    action: str = None
    prob: int = None
    foundCmd: dict = None
    for cmd in singles:
        nickname = list(cmd.keys())[0]
        pressCmd = cmd[nickname][strs.PRESS]
        holdCmd = cmd[nickname][strs.HOLD]
        if chat_cmd == pressCmd:
            foundCmd = cmd[nickname]
            action = strs.PRESS
            break
        elif chat_cmd == holdCmd:
            foundCmd = cmd[nickname]
            action = strs.HOLD
            break
        else:
            continue
    
    if foundCmd:
        key = foundCmd[strs.KEY]
        prob = cmd[nickname][strs.PROBABILITY]
    else:
        for cmd in combos:
            nickname = list(cmd.keys())[0]
            pressCmd = cmd[nickname][strs.PRESS]
            holdCmd = cmd[nickname][strs.HOLD]
            if chat_cmd == pressCmd:
                foundCmd = cmd[nickname]
                action = strs.PRESS
                break
            elif chat_cmd == holdCmd:
                foundCmd = cmd[nickname]
                action = strs.HOLD
                break
            else:
                continue
        
        key = (foundCmd[strs.KEY1], foundCmd[strs.KEY2])
        prob = foundCmd[strs.PROBABILITY]
        
    return key, action, prob

class KeyPressWorker(QRunnable):
    '''Handles all of the key presses. This gets thrown into the QThreadPool'''
    def __init__(self, preset_name: str, cmd: str):
        super().__init__()
        self._presetName = preset_name
        self._cmd = cmd
        
    def run(self) -> None:
        '''Executes the key press after extracting what the key press should be.'''
        key, action, prob = get_key(preset_name=self._presetName, chat_cmd=self._cmd)
        print(key, action, prob)
        if random.randint(1,100) <= prob:
            if type(key) == str:
                if action == strs.PRESS:
                    cntrl.press_key(key)
                else:
                    cntrl.hold_key(key)
            else:
                if action == strs.PRESS:
                    cntrl.press_combo_key(key)
                else:
                    cntrl.hold_combo_key(key)
        else:
            return

class ManagerSignals(QObject):
    noPreset = Signal()
    noChannel = Signal()
    clearPresetAlert = Signal()
    clearChannelAlert = Signal()

class TwitchPlaysManager(QObject):
    '''
    Manages all the communication with Twitch.
    
    Arguments:
        channel_name - The name of the Twitch channel to connect to.
    '''
    def __init__(self, channel_name: str, parent=None):
        super().__init__(parent)
        self._isKilled = False
        self._isPaused = True
        self._isStarted = False
        self._twitch = Twitch(channel_name=channel_name)
        self._presetName: str = None
        self.signals = ManagerSignals()
        
        self.channelName = channel_name
    
    def run(self) -> None:
        '''Never stops listening for a new chat message.'''
        self._isStarted = True
        while not self._isKilled:
            self._twitch.listen(on_message=self.execute)
            
    def execute(self, message: str) -> None:
        '''Creates the KeyPressWorker and throws it into the QThreadPool.'''
        if self._isPaused:
            return
        print(message['message']) # DEV
        command = message['message']
        if command in PRESETS[self._presetName][strs.VALID_CMDS]:
            executor = KeyPressWorker(preset_name=self._presetName, cmd=command)
            THREAD_POOL.start(executor)
        else:
            return
    
    def close(self) -> None:
        self._twitch.close()
        self.kill()
    
    def start_listening(self) -> None:
        self.run()
    
    def set_preset(self, preset_name: str) -> None:
        self._presetName = preset_name
    
    def set_channel_name(self, name: str) -> None:
        self.channelName = name
        self._twitch.set_channel_name(name)
    
    def kill(self) -> None:
        self._isKilled = True
        THREAD_POOL.clear()
        
    def pause(self) -> None:
        self._isPaused = True
    
    def resume(self) -> None:
        isSuccess = False
        if not self._presetName:
            self.signals.noPreset.emit()
        else:
            self.signals.clearPresetAlert.emit()
            
        if not self.channelName:
            self.signals.noChannel.emit()
        else:
            self.signals.clearChannelAlert.emit()
            
        if self.channelName and self._presetName:
            isSuccess = True
            self._isPaused = False
        return isSuccess
    
    
    
