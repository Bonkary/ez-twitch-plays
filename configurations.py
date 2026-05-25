import os
import json
import sys
from constants import *
from typing import Literal, Any

# OPERATIONS
def create_preset(preset_name: dict, cmd: dict = None, cmd_type: Literal['single', 'combo'] | None = None) -> None:
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

def update_preset(*, preset: str, cmd: dict, cmd_type: Literal['single', 'combo']) -> None:
    PRESETS[preset][cmd_type].append(cmd)
    nickname = list(cmd.keys())[0]
    PRESETS[preset][strs.VALID_CMDS].append(cmd[nickname][strs.PRESS])
    PRESETS[preset][strs.VALID_CMDS].append(cmd[nickname][strs.HOLD])
    update_presets_file()
        
def add_imports(presets: list[tuple[str:dict]]) -> None:
    for preset in presets:
        name = preset[0]
        cmds = preset[1]
        
        PRESETS.update({name: cmds})
    
    update_presets_file()

def update_setting(setting: str, value: Any) -> None:
    print("update settings")
    if setting in [strs.CLIPBOARD, strs.SAVE, strs.PREV_SAVE_PATH]:
        SETTINGS[strs.EXPORT][setting] = value
    else:
        SETTINGS[setting] = value
    with open(files.SETTINGS, 'w') as file:
        file.write(json.dumps(SETTINGS))

def remove_command(preset: str, nickname: str, cmd_type: Literal['single', 'combo']) -> None:
    for cmd in PRESETS[preset][cmd_type]:
        if list(cmd.keys())[0] == nickname:
            toRemove = cmd
            break
    PRESETS[preset][cmd_type].remove(toRemove)
    update_presets_file()

def remove_preset(preset: str) -> None:
    if preset in PRESETS:
        del PRESETS[preset]
    update_presets_file()

def update_presets_file() -> None:
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
        }
    }
    with open(files.SETTINGS, 'w') as file:
        file.write(json.dumps(SETTINGS))
