from dataclasses import dataclass
import os
from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QBoxLayout


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

@dataclass
class const:
    @dataclass
    class gui:
        MAIN_WINDOW_SIZE = QSize(1200,800)
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
        
        EXPORT_WINDOW_SIZE = QSize(300,400)
        
    @dataclass
    class colors:
        DEFAULT_TEXT = 'white' # also maybe #F9F871'
        TWITCH_PURPLE = '#5C3B99'
        DARK_PURPLE = '#4c3080'
        GREEN = 'green'
        RED = 'red'
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












