import os
import json
import sys
from constants import *

def add_new_preset(preset_name: dict, cmd: dict = {}) -> None:
    if not preset_name in PRESETS:
        cmd = [cmd]
        PRESETS.update({preset_name: cmd})
    else:
        print(PRESETS[preset_name])
        PRESETS[preset_name].append(cmd)
        
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))

def update_preset(*, current_preset: str, new_cmd: dict) -> None:
    PRESETS[current_preset] = new_cmd
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))

if os.path.exists(files.PRESETS):
    with open(files.PRESETS, 'r') as file:
        PRESETS = json.loads(file.read())
else:
    PRESETS = {}
    with open(files.PRESETS, 'w') as file:
        file.write(json.dumps(PRESETS))


