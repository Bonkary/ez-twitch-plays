import os
import json
import sys
from constants import *
from typing import Literal, Any

# OPERATIONS
def create_preset(preset_name: dict, cmd: dict = None, cmd_type: Literal['single', 'combo'] | None = None) -> None:
    newPreset = {
            preset_name: {
                'single': [],
                'combo': []
            }
        }
    if cmd and cmd_type:
        newPreset[preset_name][cmd_type].append(cmd)
    PRESETS.update(newPreset)
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))


def update_preset(*, preset: str, cmd: dict, cmd_type: Literal['single', 'combo']) -> None:
    PRESETS[preset][cmd_type].append(cmd)
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))
        
def add_imports(presets: list[dict]) -> None:
    for preset in presets:
        PRESETS.update(preset)
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))

def update_settings(setting: str, value: Any) -> None:
    SETTINGS[setting][value]
    with open(files.SETTINGS, 'w') as file:
        file.write(json.dumps(SETTINGS))

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
        'channel_name': None,
        'export': {
            'clipboard': False
        }
    }
    with open(files.SETTINGS, 'w') as file:
        file.write(json.dumps(SETTINGS))
