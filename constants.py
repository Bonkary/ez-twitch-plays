from dataclasses import dataclass
import os
from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QBoxLayout
from platform_connection import Twitch
import dotenv

# DOTENV
dotenvPath = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenvPath)

TWITCH = Twitch()

# Common Strings
KEY = 'key'
KEY1 = 'key1'
KEY2 = 'key2'
COMMAND = 'command'
PRESS = 'press'
HOLD = 'hold'
PROBABILITY = 'probability'
NICKNAME = 'nickname'
SINGLE = 'single'
COMBO = 'combo'
EXPORT = 'export'
CLIPBOARD = 'clipboard'
SAVE = 'save'
PREV_SAVE_PATH = 'save_path'
CHANNEL_NAME = 'channel_name'
VALID_CMDS = 'valid_cmds'

@dataclass
class const:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    @dataclass
    class gui:
        MAIN_WINDOW_SIZE = QSize(1500,1000)
        DEFAULT_FONT_FAMILY = "Arial"
        DEFAULT_FONT = QFont(DEFAULT_FONT_FAMILY, pointSize=13)
        TITLE_FONT = QFont(DEFAULT_FONT_FAMILY, pointSize=20)
        
        ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
        ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft
        ALIGN_RIGHT = Qt.AlignmentFlag.AlignRight
        ALIGN_TOP = Qt.AlignmentFlag.AlignTop
        ALIGN_BOTTOM = Qt.AlignmentFlag.AlignBottom
        
        LEFT_TO_RIGHT = QBoxLayout.Direction.LeftToRight
        RIGHT_TO_LEFT = QBoxLayout.Direction.RightToLeft
        TOP_TO_BOTTOM = QBoxLayout.Direction.TopToBottom
        BOTTOM_TO_TOP = QBoxLayout.Direction.BottomToTop
        
        EXPORT_WINDOW_SIZE = QSize(300,600)
        
    @dataclass
    class colors:
        DEFAULT_TEXT = 'white' # also maybe #F9F871'
        TWITCH_PURPLE = '#5C3B99'
        DARK_PURPLE = '#4c3080'
        GREEN = 'green'
        RED = '#AD0F00'
        BLACK = 'black'
        WHITE = 'white'

@dataclass
class dirs:
    ROOT = Path(__file__).resolve().parent
    CONFIG = os.path.join(ROOT, 'config')
    TEMP = os.path.join(ROOT, 'temp')
    DOWNLOADS = str(Path.home() / "Downloads")

@dataclass
class files:
    PRESETS = os.path.join(dirs.ROOT, 'config', 'presets.json')
    SETTINGS = os.path.join(dirs.CONFIG, 'settings.json')












