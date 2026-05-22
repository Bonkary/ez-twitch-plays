import os
import json
import sys
from old.constants import *

# FILE OPERATIONS
def write_empty_console_config_file() -> None:
    with open(files.CONSOLE_CONFIGS, 'w') as newFile:
        newFile.write(json.dumps(empty.CONSOLES))

def write_empty_settings_file() -> None:
    with open(files.SETTINGS, 'w') as newFile:
        newFile.write(json.dumps(empty.SETTINGS))

def update_settings_file() -> None:
    with open(files.SETTINGS, 'w') as settingsFile:
        settingsFile.write(json.dumps(SETTINGS))

def update_console_configs_file() -> None:
    with open(files.CONSOLE_CONFIGS, 'w') as controlSchemeFile:
        controlSchemeFile.write(json.dumps(CONSOLES))


if not os.path.exists(dirs.CONFIGS):
    os.mkdir(dirs.CONFIGS)

##################### THE ACTUAL GOOD STUFF #############################

# CONTROLS
try:
    with open(files.CONSOLE_CONFIGS, 'r') as schemesFile:
        contents = schemesFile.read()
        if not contents:
            CONSOLES = empty.CONSOLES
            write_empty_console_config_file()
        else:
            CONSOLES = json.loads(contents)
except FileNotFoundError:
    CONSOLES = empty.CONSOLES
    write_empty_console_config_file()

# SETTINGS
try:
    with open(files.SETTINGS, 'r') as settingsFile:
        contents = settingsFile.read()
        if not contents:
            SETTINGS = empty.SETTINGS
            write_empty_settings_file()
        else:
            SETTINGS = json.loads(contents)
except FileNotFoundError:
    SETTINGS = empty.SETTINGS
    write_empty_settings_file()



