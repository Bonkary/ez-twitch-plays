import pydirectinput
import time
from constants import *
from platform_connections import *
from typing import Literal
from configurations import PRESETS

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

def hold_key(key: str, *, duration: int = keys.HOLD_DURATION) -> None:
    '''
    Holds down the key for a certain interval.
    
    Arguments:
        key - The key to press down
        duration - How long you want the key pressed for
    '''
    print("sup")
    if pydirectinput.is_valid_key(key):
        pydirectinput.keyDown(key=key)
        time.sleep(duration)
        pydirectinput.keyUp(key=key)
    else:
        raise ValueError(f"{key} is not a valid key! Maybe a typo or something?")

def press_key(key: str) -> None:
    '''Simply presses and releases a key.'''
    pydirectinput.keyDown(key=key)
    time.sleep(keys.PRESS_DURATION)
    pydirectinput.keyUp(key=key)

def release_key(key: str) -> None:
    '''Simply releases a key'''
    pydirectinput.keyUp(key)

def press_combo_key(*, keys: tuple) -> None:
    '''
    Press 2 buttons at the same time.
    
    Arguments:
        keys - The keys to be pressed
    '''
    press_key(keys[0])
    press_key(keys[1])

def hold_combo_key(*, keys: (tuple), duration: int = keys.HOLD_DURATION) -> None:
    '''
    Hold 2 buttons at the same time.
    
    Arguments:
        key_1 - One of the 2 keys.
        key_2 - The other key.
    '''
    hold_key(keys[0], duration=duration)
    hold_key(keys[1], duration=duration)


# COMING SOON (maybe)
def left_click_mouse() -> None:
    raise NotImplementedError("left_click_mouse is yet to be implemented...")

def move_mouse(*, axis: Literal['x', 'y', 'xy'], distance: int, duration: int = 3) -> None:
    '''
    Moves the mouse in the desired direction.
    
    Arguments:
           axis - The axis you want the mouse to move on.
       distance - The amount you want to move the mouse.
       duration - How long you want it to take to get to the destination.
    '''
    raise NotImplementedError("left_click_mouse is yet to be implemented...")