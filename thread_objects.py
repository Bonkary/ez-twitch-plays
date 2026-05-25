import pydirectinput
import time
from platform_connection import *
from PySide6.QtCore import QThread, QThreadPool, QRunnable, QObject, Slot, Signal
import logic.controller as cntrls
import random
from typing import Literal
from constants import *
from platform_connections import Twitch

THREAD_POOL = QThreadPool.globalInstance()
EXEC_THREAD = QThread()

class Executor(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isKilled = False
        self._isPaused = False
        self._isRunning = False
        
    def run(self) -> None:
        pass
    
    def execute(self, messages: str) -> None:
        for message in messages:
            pass
    
    def kill(self) -> None:
        self._isKilled = True
    
    def pause(self) -> None:
        pass
    
    def resume(self) -> None:
        pass