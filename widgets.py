import sys
from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox, QInputDialog, QGridLayout, QFileDialog, QStyle, QMessageBox, QStackedLayout
from PySide6.QtGui import QPalette, QFont, QIcon
from constants import *
from typing import Literal, Any
from configurations import PRESETS, SETTINGS
import configurations as cfg
import shutil
import json
import subprocess
import popups
import time
from thread_objects import TwitchManager, EXEC_THREAD

class WidgetSignals(QObject):
    textChanged = Signal()

# General 
class TitledDropdown(QFrame):
    '''
    General Combobox that has a label to 'ID' it, I guess?
    
    Arguments:
              title - Text above the dropdown
          titleFont - Font of the title
     titlePlacement - Where to place the title
    
    '''
    def __init__(self, *, title: str, titlePlacement: Literal['top', 'side'], titleFont: QFont = const.gui.DEFAULT_FONT):
        super().__init__()
        self.signals = DropwdownSignals()
        self._values: list[str] = []
        self.alertActive = False
        
        self.setMinimumHeight(0)
        match titlePlacement:
            case 'top':
                mainLayout = NoPadVBoxLayout()
                mainLayout.setDirection(const.gui.TOP_TO_BOTTOM)
            case 'side':
                mainLayout = NoPadHBoxLayout()
                mainLayout.setDirection(const.gui.LEFT_TO_RIGHT)
            case _: 
                raise ValueError(f"{titlePlacement} is not a valid value (must be 'top' or 'side')")
        self.setLayout(mainLayout)
        
        titleLabel = QLabel(text=title)
        titleLabel.setFont(const.gui.DEFAULT_FONT)
        titleLabel.setContentsMargins(0,0,0,0)
        
        self._dropdown = QComboBox()
        self._dropdown.setStyleSheet("QComboBox { padding-left: 5px; }")
        self._dropdown.setFixedWidth(200)
        self._dropdown.setContentsMargins(0,0,0,0)
        self._dropdown.setFont(const.gui.DEFAULT_FONT)
        
        mainLayout.addWidget(titleLabel, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addWidget(self._dropdown)
        
        self._dropdown.currentTextChanged.connect(self.signals.textChanged.emit)
        
    def addItem(self, item: str|int) -> None:
        '''
        Add item to the dropdown
        
        Arguments:
            item - Value to add to the dropdown
        '''
        
        self._dropdown.addItem(item)
        self._values.append(item)
        
    def setCurrentText(self, text: str|int) -> None:
        '''
        Set the current value on the dropdown.
        
        Arguments:
            text - Text to set the dropdown to.
        '''
        self._dropdown.setCurrentText(text)
        
    def setCurrentIndex(self, index: int) -> None:
        '''
        Set the index of the dropdown.
        
        Arguments:
            index - Index to the set dropdown to.
        '''
        
        self._dropdown.setCurrentIndex(index)
        
    def getCurrentText(self) -> str:
        ''' Get the current text of the dropdown.'''
        return self._dropdown.currentText().strip()
        
    def removeItem(self, item: str) -> None:
        '''
        Remove item from the dropdown.
        
        Arguments:
            item - Value to remove from the dropdown.
        '''
        
        self._values.remove(item)
        self._dropdown.clear()
        for value in self._values:
            self._dropdown.addItem(value)
    
    def alert(self) -> None:
        self.alertActive = True
        self._dropdown.setStyleSheet(stylesheets.DROPDOWN_ALERT)
    
    def clearAlert(self) -> None:
        self.alertActive = False
        self._dropdown.setStyleSheet(stylesheets.DROPDOWN)

class TitledLineEdit(QFrame):
    '''
    LineEdit that has a title.
    
    Arguments:
               title - Title of the LineEdit
               width - Width of the LineEdit
             spacing - Spacing between the title and LineEdit
      titlePlacement - Where to place the title.
      titleAlignment - Alignment of the title
    '''
    def __init__(self, *, title: str, titlePlacement: Literal['top', 'side'], 
                 titleFont: QFont = const.gui.DEFAULT_FONT,
                 titleAlignment: Literal['left', 'right', 'center'] = 'left',
                 spacing: int = 10, width: int = 100, center_stretch: bool = False,
                 padding: tuple[int:int] = (0,0), center_padding: int = 0):
        super().__init__()
        self.signals = WidgetSignals()
        self.alertActive = False
        match titlePlacement:
            case 'top':
                mainLayout = NoPadVBoxLayout()
                alignment = const.gui.ALIGN_CENTER
            case 'side':
                mainLayout = NoPadHBoxLayout()
                alignment = const.gui.ALIGN_CENTER
            case _: 
                raise ValueError(f"{titlePlacement} is not a valid value")
        
        match titleAlignment:
            case 'left':
                titleAlignment = const.gui.ALIGN_LEFT
            case 'right':
                titleAlignment = const.gui.ALIGN_RIGHT
            case 'center':
                titleAlignment = const.gui.ALIGN_CENTER
        
        
        self.setLayout(mainLayout)
        
        titleLabel = QLabel(text=title)
        titleLabel.setFont(titleFont)
        
        self._entry = QLineEdit()
        self._entry.setStyleSheet(f"border: 2px solid black; background: {colors.DARK_PURPLE};")
        self._entry.setFixedWidth(width)
        self._entry.setFont(const.gui.DEFAULT_FONT)

        mainLayout.addSpacing(padding[0])
        mainLayout.addWidget(titleLabel, alignment=titleAlignment)
        mainLayout.addSpacing(spacing)
        if titlePlacement == 'side' and center_stretch:
            mainLayout.addStretch()
        if center_padding:
            mainLayout.addSpacing(center_padding)
        mainLayout.addWidget(self._entry, alignment=alignment)
        mainLayout.addSpacing(padding[1])
        
        self.signals.textChanged.connect(lambda: self._entry.textChanged.emit(self.getText()))
        
    def getText(self) -> str:
        '''Get the text from the LineEdit'''
        return self._entry.text().strip()
    
    def setText(self, text: str) -> None:
        '''Set the text in the LineEdit'''
        self._entry.setText(text)

    def clear(self) -> None:
        '''Clear the LineEdit'''
        self._entry.setText("")
        self.clear_error()

    def alert(self) -> None:
        '''Highlight the border red'''
        self.alertActive = True
        self._entry.setStyleSheet(f"border: 2px solid red; background: {colors.DARK_PURPLE};")
        
    def clearAlert(self) -> None:
        '''Remove the red border'''
        self.alertActive = False
        self._entry.setStyleSheet(f"border: 2px solid black; background: {colors.DARK_PURPLE};")

class TitledLabel(QFrame):
    '''
    Label that has a title.
    
    Arguments: 
        title - 
    '''
    def __init__(self, title: str, text: str, title_font: QFont = const.gui.DEFAULT_FONT, 
                 text_font: QFont = const.gui.DEFAULT_FONT, spacing: int = 3, underline: bool = True):
        super().__init__()
        
        mainLayout = NoPadVBoxLayout()
        mainLayout.setAlignment(const.gui.ALIGN_CENTER)
        self.setLayout(mainLayout)
        
        titleLabel = QLabel(title)
        title_font.setUnderline(underline)
        titleLabel.setFont(title_font)
        
        textLabel = QLabel(text)
        textLabel.setFont(text_font)
        
        mainLayout.addWidget(titleLabel, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(textLabel, alignment=const.gui.ALIGN_CENTER)

# Layouts
class NoPadHBoxLayout(QHBoxLayout):
    '''QHBoxLayout that has no padding around it.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(const.gui.ALIGN_CENTER)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        
class NoPadVBoxLayout(QVBoxLayout):
    '''QVBoxLayout that has no padding around it.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(const.gui.ALIGN_CENTER)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

# Inputs
# TODO: dont allow duplicate nickname
class SingleCommandInputs(QFrame):
    '''
    This is where all the inputs are for the single commands.
    
    Arguments:
        control_manager - The ControlManager
    '''
    
    def __init__(self, control_manager: ControlManager, parent=None):
        super().__init__(parent)
        self.signals = InputSignals()
        self._presetManager = control_manager
        
        rootLayout = NoPadHBoxLayout() # Squishes it all together
        self.setLayout(rootLayout)
        
        mainLayout = NoPadVBoxLayout()
        
        # Title
        title = QLabel(text="New Command")
        title.setFont(const.gui.CONTAINER_TITLE_FONT)
        
        # Input Widgets
        centerStretch = True
        self._nicknameInput = TitledLineEdit(title="Nickname", titlePlacement='side', center_stretch=centerStretch)
        self._keyInput = TitledLineEdit(title="Key", titlePlacement='side', center_stretch=centerStretch)
        self._pressCmdInput = TitledLineEdit(title="Press Cmd", titlePlacement='side', center_stretch=centerStretch)
        self._holdCmdInput = TitledLineEdit(title="Hold Cmd", titlePlacement='side', center_stretch=centerStretch)
        self._probInput = TitledLineEdit(title="Probability (0-100)", titlePlacement='side', center_stretch=centerStretch)
        
        # Button Layout
        buttonLayout = NoPadHBoxLayout()
        self._clearButton = QPushButton(text="Clear")
        self._addButton = QPushButton(text="Add")
        buttonLayout.addWidget(self._clearButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._addButton)
        
        spacing = 10
        mainLayout.addWidget(title, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(self._nicknameInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._keyInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._pressCmdInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._holdCmdInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._probInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addLayout(buttonLayout)
        
        rootLayout.addStretch()
        rootLayout.addLayout(mainLayout)
        rootLayout.addStretch()
        
        self._addButton.clicked.connect(self.add)
        self._clearButton.clicked.connect(self.clear_inputs)
        
    def get_inputs(self) -> dict:
        '''Get the inputs. If there are empty ones, it will let you know.'''
        if self._probInput.getText():
            try:
                prob = int(self._probInput.getText())
            except ValueError:
                # JUST DEV STUFF RN
                print("not a valid value dude")
                prob = 0
        else:
            prob = 100
        
        nickname = self._nicknameInput.getText().lower()
        key = self._keyInput.getText().lower()
        press = self._pressCmdInput.getText().lower()
        hold = self._holdCmdInput.getText().lower()
        
        if not nickname:
            self._nicknameInput.error()
        else:
            self._nicknameInput.clear_error()
            
        if not key:
            self._keyInput.error()
        else:
            self._keyInput.clear_error()
            
        if not press and not hold:
            self._pressCmdInput.error()
            self._holdCmdInput.error()
        elif press and not hold:
            hold = "N/A"
            self._pressCmdInput.clear_error()
            self._holdCmdInput.clear_error()
        elif not press and hold:
            press = "N/A"
            self._pressCmdInput.clear_error()
            self._holdCmdInput.clear_error()
        else:
            self._pressCmdInput.clear_error()
            self._holdCmdInput.clear_error()
        
        if not nickname or not key or (not press and not hold):
            return None
        
        return {
            strs.NICKNAME: self._nicknameInput.getText().lower(),
            strs.KEY: self._keyInput.getText().lower(),
            strs.PRESS: self._pressCmdInput.getText().lower(),
            strs.HOLD: self._holdCmdInput.getText().lower(),
            strs.PROBABILITY: prob
        }
    
    def clear_inputs(self) -> None:
        '''Clear all the inputs.'''
        self._nicknameInput.clear()
        self._keyInput.clear()
        self._pressCmdInput.clear()
        self._holdCmdInput.clear()
        self._probInput.clear()

    def add(self) -> None:
        '''Add a new single command.
           If there's no preset already set, then it'll prompt for a name.
        '''
        inputs = self.get_inputs()
        if not inputs:
            return
        cmd = {
            inputs[strs.NICKNAME]: {
                strs.KEY: inputs[strs.KEY],
                strs.PRESS: inputs[strs.PRESS],
                strs.HOLD: inputs[strs.HOLD],
                strs.PROBABILITY: inputs[strs.PROBABILITY]
            }
        }
        
        presetName = self._presetManager.get_preset()
        if not presetName:
            name, ok = QInputDialog.getText(self, "New Preset Name",'Give preset name. If not, no save.', QLineEdit.Normal, "")
            if ok and name:
                cfg.create_preset(preset_name=name, cmd=cmd, cmd_type=strs.SINGLE)
                self._presetManager.add_preset(name)
        else:
            cfg.update_preset(preset=presetName, cmd=cmd, cmd_type=strs.SINGLE)
        
        newCmd = SingleCommand(cmd=cmd)
        self.signals.addCommand.emit(newCmd)
        self.clear_inputs()
            
class ComboCommandInputs(QFrame):
    '''
    The inputs for the ComboCommands.
    
    Arguments:
        control_manager - The ControlManager
    
    '''
    def __init__(self, control_manager: ControlManager, parent=None):
        super().__init__(parent)
        self._presetManager = control_manager
        self.signals = InputSignals()
        
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        title = QLabel("New Combo Command")
        title.setFont(const.gui.CONTAINER_TITLE_FONT)
        
        # Input Widgets
        self._nicknameInput = TitledLineEdit(title='Nickname', titlePlacement='side', spacing=22, padding=(88,0), center_padding=30)
        self._pressInput = TitledLineEdit(title='Press Cmd', titlePlacement='side', spacing=22, padding=(81,0), center_padding=30)
        self._holdInput = TitledLineEdit(title='Hold Cmd', titlePlacement='side', spacing=22, padding=(88,0), center_padding=30)
        self._probInput = TitledLineEdit(title='Probability (0-100)', titlePlacement='side', spacing=22, padding=(70,0), center_padding=0)
        
        # Key1/Key2 Layout
        keyLayout = NoPadHBoxLayout()
        self._key1Input = TitledLineEdit(title="Key 1", titlePlacement='side')
        self._key2Input = TitledLineEdit(title="Key 2", titlePlacement='side')
        keyLayout.addStretch()
        keyLayout.addWidget(self._key1Input)
        keyLayout.addSpacing(10)
        keyLayout.addWidget(self._key2Input)
        keyLayout.addStretch()
        
        # Buttons Layout
        buttonLayout = NoPadHBoxLayout()
        self._clearButton = QPushButton(text="Clear")
        self._clearButton.setStyleSheet("font-size: 15px;")
        self._addButton = QPushButton(text="Add")
        self._addButton.setStyleSheet("font-size: 15px;")
        buttonLayout.addWidget(self._clearButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._addButton)
        
        spacing = 10
        mainLayout.addWidget(title, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(self._nicknameInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._pressInput, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._holdInput, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._probInput, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addLayout(keyLayout)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(buttonLayout)
        
        self._clearButton.clicked.connect(self.clear_inputs)
        self._addButton.clicked.connect(self.add)

    def clear_inputs(self) -> None:
        """Clear all the inputs"""
        self._nicknameInput.clear()
        self._key1Input.clear()
        self._key2Input.clear()
        self._pressInput.clear()
        self._holdInput.clear()
        self._probInput.clear()
    
    def get_inputs(self) -> dict:
        '''Get all the inputs'''
        prob = self._probInput.getText()
        if prob:
            try:
                prob = int(prob)
            except ValueError:
                # DEV STUFF RN
                print("not a valid value dummy")
                prob = 0
        else:
            prob = 100
            
        return {
            strs.NICKNAME: self._nicknameInput.getText().lower(),
            strs.KEY1: self._key1Input.getText().lower(),
            strs.KEY2: self._key2Input.getText().lower(),
            strs.PRESS: self._pressInput.getText().lower(),
            strs.HOLD: self._holdInput.getText().lower(),
            strs.PROBABILITY: prob
        }
    
    def add(self) -> None:
        '''This prepares the command to be added by creating the widget'''
        inputs = self.get_inputs()
        cmd = {
            inputs[strs.NICKNAME]: {
                strs.KEY1: inputs[strs.KEY1],
                strs.KEY2: inputs[strs.KEY2],
                strs.PRESS: inputs[strs.PRESS],
                strs.HOLD: inputs[strs.HOLD],
                strs.PROBABILITY: inputs[strs.PROBABILITY]
            }
        }
        
        presetName = self._presetManager.get_preset()
        if not presetName:
            name, ok = QInputDialog.getText(self, "New Preset Name",'Give preset name. If not, no save.', QLineEdit.Normal, "")
            if ok and name:
                cfg.create_preset(preset_name=name, cmd=cmd, cmd_type=strs.COMBO)
                self._presetManager.add_preset(name)
        else:
            cfg.update_preset(preset=presetName, cmd=cmd, cmd_type=strs.COMBO)
        
        newCmd = ComboCommand(cmd=cmd)
        self.signals.addCommand.emit(newCmd)
        self.clear_inputs()

# Commands
class SingleCommand(QFrame):
    '''
    This widget is a container for the info about the command
    
    Arguments:
        cmd - The command to add
    '''
    def __init__(self, cmd: dict, parent=None):
        super().__init__(parent)
        self.signals = CommandSignals()
        
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        self.nickname = list(cmd.keys())[0]
        key = cmd[self.nickname][strs.KEY]
        pressCmd = cmd[self.nickname][strs.PRESS]
        holdCmd = cmd[self.nickname][strs.HOLD]
        prob = cmd[self.nickname][strs.PROBABILITY]
        
        # Nickname
        nicknameLayout = NoPadHBoxLayout()
        nicknameLabel = QLabel(self.nickname)
        nicknameFont = QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=15)
        nicknameFont.setUnderline(True)
        nicknameLabel.setFont(nicknameFont)
        
        trashIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)
        self.trashButton = QPushButton(flat=True)
        self.trashButton.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 0px solid transparent;
                    width: 12px
                }
                QPushButton:hover {
                    background: %s    
                }
        """ % colors.DARK_PURPLE)
        self.trashButton.setIcon(QIcon(trashIcon))
        
        nicknameLayout.addWidget(nicknameLabel)
        nicknameLayout.addSpacing(10)
        nicknameLayout.addWidget(self.trashButton)
        
        pressLabel = QLabel(f"Press: {pressCmd}")
        pressLabel.setFont(const.gui.DEFAULT_FONT)
        holdLabel = QLabel(f"Hold: {holdCmd}")
        holdLabel.setFont(const.gui.DEFAULT_FONT)
        keyLabel = QLabel(f'Key: {key}')
        probLabel = QLabel(f"Probability: {prob}")
        
        mainLayout.addLayout(nicknameLayout)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(pressLabel)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(holdLabel)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(keyLabel)
        mainLayout.addSpacing(3)
        mainLayout.addWidget(probLabel)
        
        self.trashButton.clicked.connect(self.delete)

    def delete(self) -> None:
        '''This is kinda a middleman to delete a command'''
        self.signals.deleteCommand.emit(self.nickname)

class ComboCommand(QFrame):
    '''
    This widget is a container for the info about the command
    
    Arguments:
        cmd - The command to add
    '''
    def __init__(self, cmd: dict, parent=None):
        super().__init__(parent)
        self.signals = CommandSignals()
        
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        self.nickname = list(cmd.keys())[0]
        key1 = cmd[self.nickname][strs.KEY1]
        key2 = cmd[self.nickname][strs.KEY2]
        pressCmd = cmd[self.nickname][strs.PRESS]
        holdCmd = cmd[self.nickname][strs.HOLD]
        prob = cmd[self.nickname][strs.PROBABILITY]
        
        # Nickname
        nicknameLayout = NoPadHBoxLayout()
        nicknameLabel = QLabel(self.nickname)
        nicknameFont = QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=15)
        nicknameFont.setUnderline(True)
        nicknameLabel.setFont(nicknameFont)
        
        trashIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)
        self.trashButton = QPushButton(flat=True)
        self.trashButton.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 0px solid transparent;
                    width: 12px
                }
                QPushButton:hover {
                    background: %s    
                }
        """ % colors.DARK_PURPLE)
        self.trashButton.setIcon(QIcon(trashIcon))
        
        nicknameLayout.addWidget(nicknameLabel)
        nicknameLayout.addSpacing(10)
        nicknameLayout.addWidget(self.trashButton)
        
        pressLabel = QLabel(f"Press: {pressCmd}")
        pressLabel.setFont(const.gui.DEFAULT_FONT)
        holdLabel = QLabel(f"Hold: {holdCmd}")
        holdLabel.setFont(const.gui.DEFAULT_FONT)
        keyLabel = QLabel(f'Keys: {key1} + {key2}')
        probLabel = QLabel(f"Probability: {prob}")
        
        mainLayout.addLayout(nicknameLayout)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(pressLabel)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(holdLabel)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(keyLabel)
        mainLayout.addSpacing(3)
        mainLayout.addWidget(probLabel)
        
        self.trashButton.clicked.connect(self.delete)
        
    def delete(self) -> None:
        '''A middleman kinda thing to delete a command'''
        self.signals.deleteCommand.emit(self.nickname)

# Managers
class ControlManager(QFrame):
    '''This is where all the preset controls, import/export and start/stop'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = ManagerSignals()
        self._twitchManager = TwitchManager(channel_name=SETTINGS[strs.CHANNEL_NAME])
        
        self._twitchManager.moveToThread(EXEC_THREAD)
        EXEC_THREAD.started.connect(self._twitchManager.start_listening)
        EXEC_THREAD.start()
        
        # UI
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        channelFont = QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=15)
        self._channelInput = TitledLineEdit(title="Twitch Channel", titlePlacement='top',
                                            titleAlignment=const.gui.ALIGN_CENTER, titleFont=channelFont)
        if SETTINGS[strs.CHANNEL_NAME]:
            self._channelInput.setText(SETTINGS[strs.CHANNEL_NAME])
        
        self._presetDropdown = TitledDropdown(title='Preset', titlePlacement='top')
        for name in PRESETS:
            self._presetDropdown.addItem(name)
        self._presetDropdown.setCurrentIndex(-1)
        
        presetButtonStyleSheet = f"font-size: 15px; border: 2px solid black; width: 86px; height: 20px; background: {colors.DARK_PURPLE};"
        stopButtonStyleSheet = f"font-size: 15px; border: 2px solid black; width: 100px; height: 40px; background: {colors.RED};"
        
        self._newButton = QPushButton(text='New')
        self._newButton.setStyleSheet(presetButtonStyleSheet)
        self._deleteButton = QPushButton(text='Delete')
        self._deleteButton.setStyleSheet(presetButtonStyleSheet)
        self._autosave = QCheckBox(text='Autosave')
        self._importButton = QPushButton(text='Import')
        self._exportButton = QPushButton(text='Export')
        self._playButton = QPushButton(text="Start Playing")
        self._stopButton = QPushButton(text="Stop Playing")
        self._stopButton.setStyleSheet(stopButtonStyleSheet)
        
        # New/Delete Layout
        buttonLayout = NoPadHBoxLayout()
        buttonLayout.addWidget(self._newButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._deleteButton)
        
        # Import/Export Layout
        importLayout = NoPadVBoxLayout()
        importLayout.addWidget(self._importButton)
        importLayout.addSpacing(10)
        importLayout.addWidget(self._exportButton)
        
        # Play/Stop
        self._playLayout = QStackedLayout()
        self._playLayout.insertWidget(0, self._playButton)
        self._playLayout.insertWidget(1, self._stopButton)
        self._playLayout.setCurrentWidget(self._playButton)
        
        # Main Layout
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self._channelInput)
        mainLayout.addSpacing(40)
        mainLayout.addWidget(self._presetDropdown)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(importLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(self._playLayout)
        
        self._newButton.clicked.connect(self.new_preset)
        self._exportButton.clicked.connect(self.create_export_window)
        self._presetDropdown.signals.textChanged.connect(lambda: self.signals.fillContainer.emit(self._presetDropdown.getCurrentText()))
        self._deleteButton.clicked.connect(self.delete)
        self._importButton.clicked.connect(self.import_presets)
        self._playButton.clicked.connect(self.play)
        self._stopButton.clicked.connect(self.stop)
        self._channelInput.signals.textChanged.connect(self.set_channel_name)
        self._twitchManager.signals.noPreset.connect(lambda: self.alert("preset"))
        self._twitchManager.signals.noChannel.connect(lambda: self.alert("channel"))
        self._twitchManager.signals.clearPresetAlert.connect(lambda: self.clear_alert("preset"))
        self._twitchManager.signals.clearChannelAlert.connect(lambda: self.clear_alert("channel"))
        
    def get_preset(self) -> str:
        '''Get the current preset from the dropdown'''
        return self._presetDropdown.getCurrentText().strip()

    def add_preset(self, name: str) -> None:
        '''
        Add a new preset and set it into the dropdown
        
        Arguments:
            name - name of the preset to add
        '''
        self._presetDropdown.addItem(name)
        self._presetDropdown.setCurrentText(name)
        self.signals.clearContainer.emit()
    
    def set_channel_name(self, name: str) -> None:
        self._twitchManager.set_channel_name(name)
    
    @Slot()
    def new_preset(self) -> None:
        '''Create a popup that prompts for the new preset name'''
        name, ok = QInputDialog.getText(self, "New Preset Name", "Give name for preset.", QLineEdit.Normal, "")
        if name and ok:
            cfg.create_preset(preset_name=name)
            self.add_preset(name)
            
    def import_presets(self) -> None:
        '''Import a preset_export.json file (or whatever its named)'''
        path, _ = QFileDialog.getOpenFileName(self, "Select Preset file", "", "JSON files (*.json)")
        if path:
            with open(path, 'r') as file:
                newPresets = json.loads(file.read())
            
            presetList = []
            for preset in newPresets:
                presetList.append((preset, newPresets[preset]))
                self._presetDropdown.addItem(preset)
            cfg.add_imports(presetList)
        self.signals.fillContainer.emit(self._presetDropdown.getCurrentText())
    
    @Slot()
    def create_export_window(self) -> None:
        '''Creates the popup for the Export options'''
        if not PRESETS:
            msg = QMessageBox(text="Ye doth have nothin' to export.")
            
            msg.setFont(const.gui.DEFAULT_FONT)
            msg.exec()
            return
            
        popup = popups.Export()
        popup.exec()

    @Slot()
    def delete(self) -> None:
        '''Delete the preset that is currently in the dropdown'''
        preset = self._presetDropdown.getCurrentText()
        if preset:
            answer = QMessageBox.question(None, "Confirmation", f"Are you sure you want to delete {preset}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if answer == QMessageBox.StandardButton.Yes:
                self.signals.clearContainer.emit()
                self._presetDropdown.removeItem(preset)
                self._presetDropdown.setCurrentIndex(-1)
                cfg.remove_preset(preset)
            else:
                return

    @Slot()
    def play(self) -> None:
        '''Start the thread for listening and sending commands'''

        if not self._twitchManager.channelName:
            self._twitchManager.set_channel_name(self._channelInput.getText())
        if not self._twitchManager.channelName == SETTINGS[strs.CHANNEL_NAME]:
            cfg.update_setting(setting=strs.CHANNEL_NAME, value=self._twitchManager.channelName)
            
        preset = self._presetDropdown.getCurrentText()
        self._twitchManager.set_preset(preset)
        resumeSuccess = self._twitchManager.resume()
        if resumeSuccess:
            self._playLayout.setCurrentWidget(self._stopButton)
        else:
            return
    
    def stop(self) -> None:
        '''Stop the thread for listening and sending commands'''
        self._playLayout.setCurrentWidget(self._playButton)
        self._twitchManager.pause()

    def alert(self, alert: Literal['preset', 'channel']) -> None:
        match alert:
            case 'preset':
                self._presetDropdown.alert()
            case 'channel':
                self._channelInput.alert()

    def clear_alert(self, alert: Literal['preset', 'channel']) -> None:
        match alert:
            case 'preset':
                self._presetDropdown.clearAlert()
            case 'channel':
                self._channelInput.clearAlert()

# Containers 
class CommandContainer(QFrame):
    def __init__(self, control_manager: ControlManager, cmd_type: Literal['single', 'combo'], parent=None):
        super().__init__(parent)
        self._presetManager = control_manager
        self._cmdType = cmd_type
        self._existingNicknames: list[str] = []
        self.signals = ContainerSignals()
        
        self.setFixedSize(QSize(620,620))     
        self._nextRow = 0
        self._nextColumn = 0
        self._widgetCache: list[SingleCommand | ComboCommand] = []
        
        rootLayout = NoPadVBoxLayout()
        rootLayout.setAlignment(const.gui.ALIGN_CENTER)
        self.setLayout(rootLayout)
        
        margin = 15
        self._mainLayout = QGridLayout()
        
        self._mainLayout.setContentsMargins(margin, margin, margin, margin)
        self._mainLayout.setSpacing(40)
        
        rootLayout.addLayout(self._mainLayout)
        rootLayout.addStretch()
    
    @Slot(object)
    def add(self, cmd: SingleCommand | ComboCommand) -> None:
        if cmd.nickname in self._existingNicknames:
            return
        else:
            self._existingNicknames.append(cmd.nickname)
        cmd.signals.deleteCommand.connect(self.delete)
        self._mainLayout.addWidget(cmd, self._nextRow, self._nextColumn)
        self._widgetCache.append(cmd)
        if self._nextColumn == 3:
            self._nextColumn = 0
            self._nextRow += 1
        else:
            self._nextColumn += 1
            self._mainLayout.setColumnStretch(self._nextColumn, 1)
    
    def delete(self, nickname: str) -> None:
        preset = self._presetManager.get_preset()
        toRemove = None
        for widget in self._widgetCache:
            if widget.nickname == nickname:
                toRemove = widget
                break
        self._existingNicknames.remove(nickname)
        self._mainLayout.removeWidget(toRemove)
        self._widgetCache.remove(toRemove)
        toRemove.deleteLater()
        self.reorder()
        cfg.remove_command(preset=preset, nickname=nickname, cmd_type=self._cmdType)

    def fill(self, preset: str) -> None:
        self.clear()
        if preset and preset in list(PRESETS.keys()):
            allCmds = PRESETS[preset][self._cmdType]
            for cmd in allCmds:
                match self._cmdType:
                    case 'single':
                        newCmd = SingleCommand(cmd=cmd)
                    case 'combo':
                        newCmd = ComboCommand(cmd=cmd)
                self.add(newCmd)
            
    def reorder(self) -> None:
        self._nextColumn = 0
        self._nextRow = 0
        for widget in self._widgetCache:
            self._mainLayout.removeWidget(widget)
            
        for widget in self._widgetCache:
            self._mainLayout.addWidget(widget, self._nextRow, self._nextColumn)
            if self._nextColumn == 3:
                self._nextColumn = 0
                self._nextRow += 1
            else:
                self._nextColumn += 1
                self._mainLayout.setColumnStretch(self._nextColumn, 1)
    
    def clear(self) -> None:
        self._nextColumn = 0
        self._nextRow = 0
        while self._mainLayout.count():
            item = self._mainLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self._widgetCache.clear()
        self._existingNicknames.clear()

# Signals 
class ManagerSignals(QObject):
    fillContainer = Signal(str)
    clearContainer = Signal()

class CommandSignals(QObject):
    deleteCommand = Signal(object)

class InputSignals(QObject):
    addCommand = Signal(object)

class DropwdownSignals(QObject):
    textChanged = Signal(str)
   
class ContainerSignals(QObject):
    clearContainer = Signal()      
        
