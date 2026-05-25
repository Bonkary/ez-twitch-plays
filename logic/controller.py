import pydirectinput
import time
from constants import *
from old.platform_connection import *
from PySide6.QtCore import QThread, QThreadPool, QRunnable, QObject
from logic.controller import *
from typing import Literal


def hold_key(key: str, *, duration: int = keys.HOLD_KEY_DURATION) -> None:
    '''
    Holds down the key for a certain interval.
    
    Arguments:
           key - The key to press down
      duration - How long you want the key pressed for
    '''
    if pydirectinput.is_valid_key(key):
        pydirectinput.keyDown(key=key)
        time.sleep(duration)
        pydirectinput.keyUp(key=key)
    else:
        raise ValueError(f"{key} is not a valid key! Maybe a typo or something?")

def press_key(key: str) -> None:
    '''Simply presses and releases a key.'''
    pydirectinput.keyDown(key=key)
    time.sleep(keys.PRESS_TIME_DURATION)
    pydirectinput.keyUp(key=key)

def release_key(key: str) -> None:
    '''Simply releases a key'''
    pydirectinput.keyUp(key)

def press_combo_key(*, key: tuple) -> None:
    '''
    Press 2 buttons at the same time.
    
    Arguments:
        key_1 - One of the 2 keys.
        key_2 - The other key.
    '''
    press_key(key[0])
    press_key(key[1])

def hold_combo_key(*, key_1: str, key_2: str, duration: int = keys.HOLD_KEY_DURATION) -> None:
    '''
    Hold 2 buttons at the same time.
    
    Arguments:
        key_1 - One of the 2 keys.
        key_2 - The other key.
    '''
    hold_key(key_1, duration=duration)
    hold_key(key_2, duration=duration)



def left_click_mouse() -> None:
    pass

def move_mouse(*, axis: Literal['x', 'y', 'xy'], distance: int, duration: int = 3) -> None:
    '''
    Moves the mouse in the desired direction.
    
    Arguments:
           axis - The axis you want the mouse to move on.
       distance - The amount you want to move the mouse.
       duration - How long you want it to take to get to the destination.
    '''
    pass