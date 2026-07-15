from dataclasses import dataclass
import os
from pathlib import Path
from PySide6.QtCore import QSize, Qt, QThread, QThreadPool
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QBoxLayout
from threading import Event

def create_font(*, family: str, point_size: int = 11, bold: bool = False, underline: bool = False, pixel_size: int | None = None) -> QFont:
    font = QFont()
    font.setFamily(family)
    font.setBold(bold)
    font.setUnderline(underline)
    if pixel_size:
        font.setPixelSize(pixel_size)
    else:
        font.setPointSize(point_size)
        
    return font

THREAD_POOL = QThreadPool.globalInstance()
EXEC_THREAD = QThread()
KILL_THREADS_FLAG = Event()

DEV_ON_MAC = False

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
    @dataclass
    class index: # Stacked Layouts
        PLAY_BUTTON = 0
        STOP_BUTTON = 1
        
        HELP_SELECTION = 0
        HELP_DISPLAY = 1
        HELP_CONNECT = 0
        HELP_COMMANDS = 1
        HELP_PRESETS = 2
        HELP_PLAY = 3
    
    @dataclass
    class sizes:
        MAIN_WINDOW = QSize(1700,900)
        EXPORT_WINDOW = QSize(300,600)
        HELP_WINDOW = QSize(1200,600)
        VALID_KEYS_WINDOW = QSize(600,750)
        COMMAND_CONTAINER = QSize(620,620)
        
        DEFAULT_BUTTONS = QSize(100,25)
        HELP_BUTTONS = QSize(250,40)
    
    @dataclass
    class format:
        ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
        ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft
        ALIGN_RIGHT = Qt.AlignmentFlag.AlignRight
        ALIGN_TOP = Qt.AlignmentFlag.AlignTop
        ALIGN_BOTTOM = Qt.AlignmentFlag.AlignBottom
    
        LEFT_TO_RIGHT = QBoxLayout.Direction.LeftToRight
        RIGHT_TO_LEFT = QBoxLayout.Direction.RightToLeft
        TOP_TO_BOTTOM = QBoxLayout.Direction.TopToBottom
        BOTTOM_TO_TOP = QBoxLayout.Direction.BottomToTop
    
    

@dataclass
class fonts:
    FONT_FAMILY = "Arial"
    DEFAULT_POINT_SIZE = 11
    DEFAULT = QFont(FONT_FAMILY, pointSize=DEFAULT_POINT_SIZE)
    DEFAULT_LARGE = QFont(FONT_FAMILY, pointSize=DEFAULT_POINT_SIZE+5)
    TITLE = QFont(FONT_FAMILY, pointSize=DEFAULT_POINT_SIZE+10)
    CONTAINER_TITLE = QFont(FONT_FAMILY, pointSize=DEFAULT_POINT_SIZE+5)
    NICKNAME = QFont(FONT_FAMILY, pointSize=DEFAULT_POINT_SIZE+1)
    CHANNEL = QFont(FONT_FAMILY, pointSize=DEFAULT_POINT_SIZE+4)
    HELP_TEXT = create_font(family=FONT_FAMILY, point_size=DEFAULT_POINT_SIZE+3)
    HELP_BUTTON = create_font(family=FONT_FAMILY, point_size=DEFAULT_POINT_SIZE+5)
    IMPORTING = create_font(family=FONT_FAMILY, point_size=DEFAULT_POINT_SIZE+15)

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
class styles:
    DROPDOWN_ALERT = "QComboBox { padding-left: 5px; border-color: %s}" % colors.RED
    DROPDOWN = "QComboBox { padding-left: 5px; border-color: %s}" % colors.BLACK
    LINE_EDIT = f"border: 2px solid black; background: {colors.DARK_PURPLE};"
    LINE_EDIT_ALERT = f"border: 2px solid black; background-color: rgba(255, 112, 115, 0.3)"
    PLAY_BUTTON = """
                QPushButton {
                    border: 2px solid black; 
                    background: %s;
                }
                QPushButton:hover {
                    background: %s;
                }
                """ % (colors.DARK_PURPLE, colors.DARK_PURPLE)
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
                border: 2px solid black;
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
    MESSAGE_BOX_BUTTON = """
            QPushButton {
                width: 100px
            }
    """
    

@dataclass
class dialog:
    @dataclass
    class help:
        CONNECT = [
            "Towards the top, there is a place to enter your Twitch channel name.",
            "Make sure you type the name correctly, as it won't tell you whether it's valid or not.\n\n",
            "Once you click Start Playing, it will yoink what you typed in and the connection will be made.",
            "If you've already typed one in before, it'll connect to that off the rip.",
            "I've assumed you aren't changing your channel much."
        ]
        COMMANDS = [
            "Input Fields:\n\n",
            "  Nickname - This will be the nickname for the command. It is suggested that you use whatever the command does. (jump, run, etc.)\n\n",
            "  Key - The key(s) that is being pressed. You can see the valid keys by pressing the button 'Valid Keys'\n\n",
            "  Press Cmd - This is what chat will type to quickly tap the key(s).\n\n",
            "  Hold Cmd - This is what chat will type to briefly hold down the key(s).\n\n",
            "  Probability - This is the odds (percentage) that the key will actually be pressed. Mainly for large streams or annoying commands.\n\n",
        ]
        PRESETS = [
            "Presets are a collection of Commands.\n",
            "The idea of Presets are so you don't have to add commands each time you wanna play.\n",
            "I'd name them based on the game or console you're making them for, but you can do you.\n\n",
            "You can also Export or Import presets by clicking the respective button.\n",
            "You can choose to simply copy the file to your clipboard without needing to save the file. (Mainly to just paste the file in Discord).\n",
            "But you can also save the file if you want.\n",
            "You'll see the options."
        ]
        PLAY = [
            "Click 'Start Playing'.\n",
            "In order for this to work, the game window needs to be in focus.",
            "Otherwise, keys will still be mercilessly 'pressed' on the window you are focused on. That could be messy.\n",
            "There will be a short 3 second delay so that you can switch to the game window.\n",
            "Have fun."
        ]

@dataclass
class keys:
    HOLD_DURATION = 1.5
    PRESS_DURATION = 0.2
    
    VALID_LIST = [
        'A - Z',
        '0 - 9',
        'F1 - F12',
        'numpad0 - numpad9',
        'esc',
        'escape',
        'backspace',
        'return',
        'enter',
        'space',
        'shift',
        'shiftleft',
        'shiftright',
        'ctrl',
        'ctrlleft',
        'ctrlright',
        'alt',
        'altleft',
        'altright',
        '-',
        '=',
        'numlock',
        'up',
        'down',
        'left',
        'right'
    ]

    
@dataclass
class alerts:
    EMPTY_CHANNEL_NAME = 'channel_name'
    EMPTY_PRESET = 'preset'




