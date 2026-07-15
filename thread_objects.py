from PySide6.QtCore import QRunnable, QObject, Signal
from constants import *
from platform_connections import Twitch
from configurations import PRESETS
import random
if not DEV_ON_MAC:
    import controller as cntrl

class KeyPressWorker(QRunnable):
    '''Handles all of the key presses. This gets thrown into the QThreadPool'''
    def __init__(self, preset_name: str, cmd: str):
        super().__init__()
        self._presetName = preset_name
        self._cmd = cmd
        
    def run(self) -> None:
        '''Executes the key press after extracting what the key press should be.'''
        key, action, prob = cntrl.get_key(preset_name=self._presetName, chat_cmd=self._cmd)
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
    def __init__(self, channel_name: str):
        super().__init__(parent=None)
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
    
    def set_channel_name(self, channel_name: str) -> None:
        self.channelName = channel_name
        self._twitch.set_channel_name(channel_name)
    
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
    
    
    
