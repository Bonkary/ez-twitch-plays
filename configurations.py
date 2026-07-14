import os
import json
import sys
from constants import *
from typing import Literal, Any

# OPERATIONS
def create_preset(preset_name: dict, cmd: dict = None, cmd_type: Literal['single', 'combo'] | None = None) -> None:
    '''
    Creates a new Preset and adds the cmd to it, if applicable.
    
    Arguments:
        preset_name - The name of the Preset.
        cmd - The first command to be added.
        cmd_type - The type of command.
    '''
    
    newPreset = {
            preset_name: {
                strs.SINGLE: [],
                strs.COMBO: [],
                strs.VALID_CMDS: []
            }
        }
    if cmd and cmd_type:
        nickname = list(cmd.keys())[0]
        newPreset[preset_name][cmd_type].append(cmd)
        newPreset[preset_name][strs.VALID_CMDS].append(cmd[nickname][strs.PRESS])
        newPreset[preset_name][strs.VALID_CMDS].append(cmd[nickname][strs.HOLD])
    PRESETS.update(newPreset)
    update_presets_file()

def update_preset(*, preset_name: str, cmd: dict, cmd_type: Literal['single', 'combo']) -> None:
    '''
    Updates a Preset.
    
    Arguments:
        preset_name - Name of the preset.
        cmd - The command to add to the Preset.
        cmd_type - The type of command being added.
    '''
    
    PRESETS[preset_name][cmd_type].append(cmd)
    nickname = list(cmd.keys())[0]
    PRESETS[preset_name][strs.VALID_CMDS].append(cmd[nickname][strs.PRESS])
    PRESETS[preset_name][strs.VALID_CMDS].append(cmd[nickname][strs.HOLD])
    update_presets_file()
        
def add_imports(presets: list[tuple[str:dict]]) -> None:
    '''
    Adds Presets from an imported file.
    
    Arguments:
        presets - The Presets being added.
    '''
    
    for preset in presets:
        name = preset[0]
        cmds = preset[1]
        
        PRESETS.update({name: cmds})
    
    update_presets_file()

def update_setting(setting: str, value: Any) -> None:
    '''
    Updates the value of an app setting.
    
    Arguments:
        setting - The setting to be changed.
        value - The new value of the setting.
    '''
    
    if setting in [strs.CLIPBOARD, strs.SAVE, strs.PREV_SAVE_PATH]:
        SETTINGS[strs.EXPORT][setting] = value
    else:
        SETTINGS[setting] = value
    with open(files.SETTINGS, 'w') as file:
        file.write(json.dumps(SETTINGS))

def remove_command(preset_name: str, nickname: str, cmd_type: Literal['single', 'combo']) -> None:
    '''
    Remove a command from the Preset.
    
    Arguments:
        preset_name - The name of the Preset.
        nickname - The nickname of the command.
        cmd_type - The type of command.
    '''
    
    for cmd in PRESETS[preset_name][cmd_type]:
        if list(cmd.keys())[0] == nickname:
            toRemove = cmd
            break
    PRESETS[preset_name][cmd_type].remove(toRemove)
    update_presets_file()

def delete_preset(preset_name: str) -> None:
    '''
    Delete a Preset.
    
    Arguments:
        preset_name - The Preset to be deleted.
    '''
    
    if preset_name in PRESETS:
        del PRESETS[preset_name]
    update_presets_file()

def update_presets_file() -> None:
    '''Updates the preset.json file.'''
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))


# CONFIG
if not os.path.exists(dirs.CONFIG):
    os.makedirs(dirs.CONFIG, exist_ok=True)

# CONSTANTS
if os.path.exists(files.PRESETS):
    with open(files.PRESETS, 'r') as file:
        PRESETS = json.loads(file.read())
else:
    PRESETS = {}
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))

# SETTINGS
if os.path.exists(files.SETTINGS):
    with open(files.SETTINGS, 'r') as file:
        SETTINGS = json.loads(file.read())
else:
    SETTINGS = {
        strs.CHANNEL_NAME: None,
        strs.EXPORT: {
            strs.CLIPBOARD: True,
            strs.SAVE: False,
            strs.PREV_SAVE_PATH: dirs.DOWNLOADS
        },
        strs.FIRST_START: False
    }
    with open(files.SETTINGS, 'w') as file:
        file.write(json.dumps(SETTINGS))
