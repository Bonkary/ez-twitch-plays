from dataclasses import dataclass
import os
from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QBoxLayout

@dataclass
class strs:
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
    FIRST_START = 'first_start'

@dataclass
class colors:
    DEFAULT_TEXT = 'white' # also maybe #F9F871'
    PURPLE = '#5C3B99'
    DARK_PURPLE = '#4c3080'
    GREEN = 'green'
    RED = '#AD0F00'
    BLACK = 'black'
    WHITE = 'white'
    BG_RED = '#FF7073'

@dataclass
class gui:
    MAIN_WINDOW_SIZE = QSize(1600,1000)
    DEFAULT_FONT_FAMILY = "Arial"
    
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
class fonts:
    FONT_FAMILY = "Arial"
    DEFAULT = QFont(FONT_FAMILY, pointSize=15)
    DEFAULT_LARGE = QFont(FONT_FAMILY, pointSize=20)
    TITLE_FONT = QFont(FONT_FAMILY, pointSize=20)
    CONTAINER_TITLE_FONT = QFont(FONT_FAMILY, pointSize=DEFAULT.pointSize()+5)
    NICKNAME = QFont(gui.DEFAULT_FONT_FAMILY, pointSize=15)
    CHANNEL = QFont(gui.DEFAULT_FONT_FAMILY, pointSize=15)

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

@dataclass
class stylesheets:
    DROPDOWN_ALERT = "QComboBox { padding-left: 5px; border-color: %s}" % colors.RED
    DROPDOWN = "QComboBox { padding-left: 5px; border-color: %s}" % colors.BLACK
    LINE_EDIT = f"border: 2px solid black; background: {colors.DARK_PURPLE};"
    LINE_EDIT_ALERT = f"border: 2px solid black; background-color: rgba(255, 112, 115, 0.3)"
    PLAY_BUTTON = f"font-size: 15px; border: 2px solid black; background: {colors.DARK_PURPLE};"
    STOP_BUTTON = f"font-size: 15px; border: 2px solid black; background: {colors.RED};"
    TRASH_BUTTON = """
                QPushButton {
                    background-color: transparent;
                    border: 0px solid transparent;
                    width: 12px
                }
                QPushButton:hover {
                    background: %s    
                }
        """ % colors.DARK_PURPLE
    MAIN_WINDOW = """
            QPushButton {
                font-size: 15px;
                border: 2px solid black;
                width: 100px;
                height: 20px;
                background: %s;
            }
            QPushButton:hover {
                background: %s;
            }
            QComboBox {
                border: 2px solid black;
                background: %s;
            }
            QLabel {
                color: %s;
            }
        """ % (colors.DARK_PURPLE, colors.PURPLE, colors.DARK_PURPLE, colors.DEFAULT_TEXT)
    
@dataclass
class dialog:
    @dataclass
    class tutorial:
        INTRO = [
            "Welcome to Ez Twitch Plays!",
            "Here's a breakdown of what everything is."
        ]
        COMBOS = "There's single commands and combo commands. Combo commands are 2 keys pressed or held at the same time. Single is... a single key."
        NICKNAME = "This is what the command is called. The action its performing is a good name. (ex. Jump)"
        KEY = "Whatever key you want to be pressed."
        PRESS = "Chat command for a quick press of the key."
        HOLD = "Chat command for a short hold of the key."
        PROBABILITY = "How often you want the command to be allowed through. Good idea if the command is obnoxious or if you just wanna slow down the inputs.",
        TWITCH_CHANNEL = "On the top there is a place to put your channel name. It's a must."
        PRESETS = "You can save presets for games so you don't have to type everything in every time. Select them with the dropdown."
        COMMANDS = "After you add a command, you'll see it appear. You can click the X next to the nickname to delete it."
        IMPORT_EXPORT = "You can also import and export presets. When you export a preset, you can choose to save it and whether to copy the file to the clipboard or not."
        PLAY = "Once you have your preset and channel name, you can go ahead and hit that play button and it'll start taking in commands."








