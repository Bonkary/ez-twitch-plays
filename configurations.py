import os
import json
import sys
from constants import *

def add_new_preset(new_preset: dict) -> None:
    pass

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


