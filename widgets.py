from PySide6.QtCore import Qt, Slot, Signal, QObject, QTimer
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QCheckBox,
    QInputDialog, QGridLayout, QFileDialog, QStyle,
    QMessageBox, QStackedLayout, QWidget, QMainWindow)
from PySide6.QtGui import QFont, QIcon
from constants import *
from typing import Literal, Any
from configurations import PRESETS, SETTINGS
import configurations as cfg
import json
import popups
from thread_objects import TwitchPlaysManager

# TODO: Slots and Signals decorating type shit. Gotta get that marginal performance boost that absolutely no one will ever notice.

class CustomQWidget(QWidget):
    '''This is just to get the background color set to a single line of code rather than 4 lol'''
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def setBackgroundColor(self, color: str):
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), color)
        self.setPalette(bg)

class CustomQMainWindow(QMainWindow):
    '''This is just to get the background color set to a single line of code rather than 4 lol'''
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def setBackgroundColor(self, color: str) -> None:
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), color)
        self.setPalette(bg)

# General
class TitledDropdown(QFrame):
    '''
    General Combobox that has a label to 'ID' it, I guess?
    
    Arguments:
        title - Text above the dropdown
        titleFont - Font of the title
        titlePlacement - Where to place the title
    '''
    def __init__(self, *, title: str, title_placement: Literal['top', 'side'], font: QFont = fonts.DEFAULT, values: list = None):
        super().__init__()
        self.signals = DropwdownSignals()
        self._values: list[str] = []
        self.alertActive = False
        
         # Widgets
        titleLabel = BasicLabel(text=title)
        self._dropdown = BasicComboBox(width=200, stylesheet=styles.DROPDOWN)
        if values:
            for value in values:
                self._dropdown.addItem(value)
            self.setCurrentIndex(-1)
        
        # Layouts
        match title_placement:
            case 'top':
                mainLayout = NoPadVBoxLayout()
                mainLayout.setDirection(gui.TOP_TO_BOTTOM)
            case 'side':
                mainLayout = NoPadHBoxLayout()
                mainLayout.setDirection(gui.LEFT_TO_RIGHT)
            case _: 
                raise ValueError(f"{title_placement} is not a valid value (must be 'top' or 'side')")
        
        #   Main Layout
        mainLayout.addWidget(titleLabel, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(3)
        mainLayout.addWidget(self._dropdown)
        
        self.setLayout(mainLayout)
        
        # Connections
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
        self._dropdown.setStyleSheet(styles.DROPDOWN_ALERT)
    
    def clearAlert(self) -> None:
        self.alertActive = False
        self._dropdown.setStyleSheet(styles.DROPDOWN)

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
    def __init__(self, *, title: str, title_placement: Literal['top', 'side'], 
                 title_font: QFont = fonts.DEFAULT,
                 title_alignment: Literal['left', 'right', 'center'] = 'left',
                 spacing: int = 10, width: int = 100, center_stretch: bool = False,
                 padding: tuple[int:int] = (0,0), center_padding: int = 0, placeholder: str = ''):
        super().__init__()
        self.signals = WidgetSignals()
        self.alertActive = False
        
        # Widgets
        titleLabel = BasicLabel(text=title, font=title_font)
        self._entry = BasicLineEdit(width=width, stylesheet=styles.LINE_EDIT, placeholder=placeholder)
        
        # Layouts
        match title_placement:
            case 'top':
                mainLayout = NoPadVBoxLayout()
                alignment = gui.ALIGN_CENTER
            case 'side':
                mainLayout = NoPadHBoxLayout()
                alignment = gui.ALIGN_CENTER
            case _: 
                raise ValueError(f"{title_placement} is not a valid value")
        
        match title_alignment:
            case 'left':
                title_alignment = gui.ALIGN_LEFT
            case 'right':
                title_alignment = gui.ALIGN_RIGHT
            case 'center':
                title_alignment = gui.ALIGN_CENTER
        
        #   Main Layout
        mainLayout.addSpacing(padding[0])
        mainLayout.addWidget(titleLabel, alignment=title_alignment)
        mainLayout.addSpacing(spacing)
        if title_placement == 'side' and center_stretch:
            mainLayout.addStretch()
        if center_padding:
            mainLayout.addSpacing(center_padding)
        mainLayout.addWidget(self._entry, alignment=alignment)
        mainLayout.addSpacing(padding[1])
        
        self.setLayout(mainLayout)
        
        # Connections
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
        self.clearAlert()

    def alert(self) -> None:
        '''Highlight the border red'''
        self.alertActive = True
        self._entry.setStyleSheet(styles.LINE_EDIT_ALERT)
        
    def clearAlert(self) -> None:
        '''Remove the red border'''
        self.alertActive = False
        self._entry.setStyleSheet(styles.LINE_EDIT)

class TitledLabel(QFrame):
    '''
    Label that has a title.
    
    Arguments: 
        title - 
    '''
    def __init__(self, title: str, text: str, title_font: QFont = fonts.DEFAULT, 
                 text_font: QFont = fonts.DEFAULT, spacing: int = 3, underline: bool = True):
        super().__init__()
        
        text_font.setUnderline(underline)
        # Widgets
        titleLabel = BasicLabel(text=title, underline=True, font=title_font)
        textLabel = BasicLabel(text=text, font=text_font)
        
        # Layouts
        mainLayout = NoPadVBoxLayout()
        mainLayout.setAlignment(gui.ALIGN_CENTER)
        
        #   Main Layout
        mainLayout.addWidget(titleLabel, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(textLabel, alignment=gui.ALIGN_CENTER)
        
        self.setLayout(mainLayout)

class BasicLabel(QLabel):
    def __init__(self, text: str = None, *, font: QFont = fonts.DEFAULT, alignment = gui.ALIGN_CENTER, underline: bool = False, stylesheet: str = None, width: int = None):
        super().__init__(parent=None, text=text)
        font.setUnderline(underline)
        self.setFont(font)
        self.setAlignment(alignment)
        if width:
            self.setFixedWidth(width)
        if stylesheet:
            self.setStyleSheet(stylesheet)

class BasicPushButton(QPushButton):
    def __init__(self, *, text: str = None, font: QFont = fonts.DEFAULT, width: int = 100, height: int = 25, stylesheet: str = None, icon: QIcon = None, flat: bool = False):
        super().__init__(parent=None, text=text)    
        self.setFont(font)
        self.setFixedHeight(height)
        self.setFixedWidth(width)
        self.setFlat(flat)
        self.setText(text)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        if icon:
            self.setIcon(icon)

class BasicComboBox(QComboBox):
    def __init__(self, *, font: QFont = fonts.DEFAULT, width: int = None, stylesheet: str = None):
        super().__init__(parent=None)
        self.setFont(font)
        if width:
            self.setFixedWidth(width)
        if stylesheet:
            self.setStyleSheet(stylesheet)
            
class BasicLineEdit(QLineEdit):
    def __init__(self, *, font: QFont = fonts.DEFAULT, width: int = None, stylesheet: str = None, placeholder: str = None):
        super().__init__(parent=None)
        self.setFont(font)
        if width:
            self.setFixedWidth(width)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        if placeholder:
            self.setText(placeholder)
        
class BasicCheckbox(QCheckBox):
    def __init__(self, text: str, *, font: QFont = fonts.DEFAULT, checked: bool = False):
        super().__init__(parent=None, text=text)
        self.setFont(font)
        if checked:
            self.setCheckState(Qt.CheckState.Checked)

# Layouts
class NoPadHBoxLayout(QHBoxLayout):
    '''QHBoxLayout that has no padding around it.'''
    def __init__(self, alignment: Qt.AlignmentFlag = gui.ALIGN_CENTER, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(alignment)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        
class NoPadVBoxLayout(QVBoxLayout):
    '''QVBoxLayout that has no padding around it.'''
    def __init__(self, alignment: Qt.AlignmentFlag = gui.ALIGN_CENTER, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(alignment)
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
        
        centerStretch = True
        
        # Widgets
        title = BasicLabel(text="New Command", font=fonts.TITLE)
        self._nicknameInput = TitledLineEdit(title="Nickname", title_placement='side', center_stretch=centerStretch)
        self._keyInput = TitledLineEdit(title="Key", title_placement='side', center_stretch=centerStretch)
        self._pressCmdInput = TitledLineEdit(title="Press Cmd", title_placement='side', center_stretch=centerStretch)
        self._holdCmdInput = TitledLineEdit(title="Hold Cmd", title_placement='side', center_stretch=centerStretch)
        self._probInput = TitledLineEdit(title="Probability (0-100)", title_placement='side', center_stretch=centerStretch)
        
        # Layouts
        rootLayout = NoPadHBoxLayout() # Squishes it all together
        mainLayout = NoPadVBoxLayout()
        
        #   Button Layout
        buttonLayout = NoPadHBoxLayout()
        self._clearButton = QPushButton(text="Clear")
        self._addButton = QPushButton(text="Add")
        buttonLayout.addWidget(self._clearButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._addButton)
        
        #   Main Layout
        spacing = 10
        mainLayout.addWidget(title, alignment=gui.ALIGN_CENTER)
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
        self.setLayout(rootLayout)
        
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
        
        nickname = self._nicknameInput.getText()
        key = self._keyInput.getText().lower()
        press = self._pressCmdInput.getText().lower()
        hold = self._holdCmdInput.getText().lower()
        
        if not nickname:
            self._nicknameInput.alert()
        else:
            self._nicknameInput.clearAlert()
            
        if not key:
            self._keyInput.alert()
        else:
            self._keyInput.clearAlert()
            
        if not press and not hold:
            self._pressCmdInput.alert()
            self._holdCmdInput.alert()
        elif press and not hold:
            hold = "---"
            self._pressCmdInput.clearAlert()
            self._holdCmdInput.clearAlert()
        elif not press and hold:
            press = "---"
            self._pressCmdInput.clearAlert()
            self._holdCmdInput.clearAlert()
        else:
            self._pressCmdInput.clearAlert()
            self._holdCmdInput.clearAlert()
        
        if not nickname or not key or (not press and not hold):
            return None
        
        return {
            strs.NICKNAME: nickname,
            strs.KEY: key,
            strs.PRESS: press,
            strs.HOLD: hold,
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
            cfg.update_preset(preset_name=presetName, cmd=cmd, cmd_type=strs.SINGLE)
        
        newCmd = Command(cmd=cmd, type=strs.SINGLE)
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
        
        # Widgets
        title = BasicLabel("New Combo Command", font=fonts.TITLE)
        self._nicknameInput = TitledLineEdit(title='Nickname', title_placement='side', spacing=22, padding=(88,0), center_padding=30)
        self._pressCmdInput = TitledLineEdit(title='Press Cmd', title_placement='side', spacing=22, padding=(81,3), center_padding=30)
        self._holdCmdInput = TitledLineEdit(title='Hold Cmd', title_placement='side', spacing=22, padding=(88,0), center_padding=30)
        self._probCmdInput = TitledLineEdit(title='Probability (0-100)', title_placement='side', spacing=22, padding=(70,15), center_padding=0)
        self._key1Input = TitledLineEdit(title="Key 1", title_placement='side')
        self._key2Input = TitledLineEdit(title="Key 2", title_placement='side', padding=(0,3))
        self._clearButton = BasicPushButton(text="Clear", stylesheet="font-size: 15px;")
        self._addButton = BasicPushButton(text="Add", stylesheet="font-size: 15px;")
        
        # Layouts
        mainLayout = NoPadVBoxLayout()
        
        #   Key1/Key2 Layout
        keyLayout = NoPadHBoxLayout()
        keyLayout.addStretch()
        keyLayout.addWidget(self._key1Input)
        keyLayout.addSpacing(10)
        keyLayout.addWidget(self._key2Input)
        keyLayout.addStretch()
        
        #   Buttons Layout
        buttonLayout = NoPadHBoxLayout()
        buttonLayout.addWidget(self._clearButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._addButton)
        
        #   Main Layout
        spacing = 10
        mainLayout.addWidget(title, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(self._nicknameInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addLayout(keyLayout)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._pressCmdInput, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._holdCmdInput, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._probCmdInput, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)
        
        self._clearButton.clicked.connect(self.clear_inputs)
        self._addButton.clicked.connect(self.add)

    def clear_inputs(self) -> None:
        """Clear all the inputs"""
        self._nicknameInput.clear()
        self._key1Input.clear()
        self._key2Input.clear()
        self._pressCmdInput.clear()
        self._holdCmdInput.clear()
        self._probCmdInput.clear()
    
    def get_inputs(self) -> dict:
        '''Get all the inputs'''
        if self._probCmdInput.getText():
            try:
                prob = int(self._probCmdInput.getText())
            except ValueError:
                # JUST DEV STUFF RN
                print("not a valid value dude")
                prob = 0
        else:
            prob = 100
        
        nickname = self._nicknameInput.getText()
        key1 = self._key1Input.getText().lower()
        key2 = self._key2Input.getText().lower()
        press = self._pressCmdInput.getText().lower()
        hold = self._holdCmdInput.getText().lower()
        
        if not nickname:
            self._nicknameInput.alert()
        else:
            self._nicknameInput.clearAlert()
            
        if not key1:
            self._key1Input.alert()
        else:
            self._key1Input.clearAlert()
            
        if not key2:
            self._key2Input.alert()
        else:
            self._key2Input.clearAlert()
            
        if not press and not hold:
            self._pressCmdInput.alert()
            self._holdCmdInput.alert()
        elif press and not hold:
            hold = "N/A"
            self._pressCmdInput.clearAlert()
            self._holdCmdInput.clearAlert()
        elif not press and hold:
            press = "N/A"
            self._pressCmdInput.clearAlert()
            self._holdCmdInput.clearAlert()
        else:
            self._pressCmdInput.clearAlert()
            self._holdCmdInput.clearAlert()
        
        if not nickname or (not key1 and not key2) or (not press and not hold):
            return None
        
        return {
            strs.NICKNAME: nickname,
            strs.KEY1: key1,
            strs.KEY2: key2,
            strs.PRESS: press,
            strs.HOLD: hold,
            strs.PROBABILITY: prob
        }
    
    def add(self) -> None:
        '''This prepares the command to be added by creating the widget'''
        inputs = self.get_inputs()
        if not inputs:
            return
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
            cfg.update_preset(preset_name=presetName, cmd=cmd, cmd_type=strs.COMBO)
        
        newCmd = Command(cmd=cmd, type='combo')
        self.signals.addCommand.emit(newCmd)
        self.clear_inputs()

class Command(QFrame):
    '''
    This widget is a container for the info about the command
    
    Arguments:
        cmd - The command to add
    '''
    def __init__(self, *, cmd: dict, type: Literal['single', 'combo'], parent=None):
        super().__init__(parent)
        self.signals = CommandSignals()
        self.nickname = list(cmd.keys())[0]
        
        pressCmd = cmd[self.nickname][strs.PRESS]
        holdCmd = cmd[self.nickname][strs.HOLD]
        prob = cmd[self.nickname][strs.PROBABILITY]
        trashIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)
        key1: str = None
        key2: str = None
        match type:
            case 'single':
                key1 = cmd[self.nickname][strs.KEY]
                keyLabelText = f"Key: {key1}"
            case 'combo':
                key1 = cmd[self.nickname][strs.KEY1]
                key2 = cmd[self.nickname][strs.KEY2]
                keyLabelText = f"Keys: {key1} + {key2}"
        
        # Widgets
        nicknameLabel = BasicLabel(text=self.nickname, font=fonts.NICKNAME, underline=True, width=200, alignment=gui.ALIGN_LEFT)
        self.trashButton = BasicPushButton(flat=True, icon=QIcon(trashIcon), stylesheet=styles.TRASH_BUTTON, width=20, height=20)
        pressLabel = BasicLabel(f"Press: {pressCmd}", alignment=gui.ALIGN_LEFT)
        holdLabel = BasicLabel(f"Hold: {holdCmd}")
        keyLabel = BasicLabel(keyLabelText)
        probLabel = BasicLabel(f"Probability: {prob}", alignment=gui.ALIGN_LEFT)
        
        # Layouts
        mainLayout = NoPadVBoxLayout()
        
        #   Nickname Layout
        nicknameLayout = NoPadHBoxLayout()
        nicknameLayout.addWidget(nicknameLabel)
        nicknameLayout.addStretch()
        nicknameLayout.addWidget(self.trashButton, alignment=gui.ALIGN_RIGHT)
        # nicknameLayout.addSpacing(50)
        
        #   Main Layout
        mainLayout.addLayout(nicknameLayout)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(pressLabel, alignment=gui.ALIGN_LEFT)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(holdLabel, alignment=gui.ALIGN_LEFT)
        mainLayout.addSpacing(5)
        mainLayout.addWidget(keyLabel, alignment=gui.ALIGN_LEFT)
        mainLayout.addSpacing(3)
        mainLayout.addWidget(probLabel, alignment=gui.ALIGN_LEFT)
        
        self.setLayout(mainLayout)
        
        # Connections
        self.trashButton.clicked.connect(self.delete)

    def delete(self) -> None:
        '''This is kinda a middleman to delete a command'''
        self.signals.deleteCommand.emit(self.nickname)


# Managers
class ControlManager(QFrame):
    '''This is where all the preset controls, import/export and start/stop'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = ManagerSignals()
        self._twitchManager = TwitchPlaysManager(channel_name=SETTINGS[strs.CHANNEL_NAME])
        QTimer.singleShot(1000, EXEC_THREAD.start)
        
        self._twitchManager.moveToThread(EXEC_THREAD)
        EXEC_THREAD.started.connect(self._twitchManager.start_listening)
        
        # Widgets
        self._newButton = BasicPushButton(text='New')
        self._deleteButton = BasicPushButton(text='Delete')
        self._importButton = BasicPushButton(text='Import')
        self._exportButton = BasicPushButton(text='Export')
        self._playButton = BasicPushButton(text="Start Playing", width=600, height=50, stylesheet=styles.PLAY_BUTTON)
        self._stopButton = BasicPushButton(text="Stop Playing", width=600, height=50, stylesheet=styles.STOP_BUTTON)
        self._presetDropdown = TitledDropdown(title='Preset', title_placement='top', values=PRESETS)
        self._channelInput = TitledLineEdit(title="Twitch Channel", title_placement='side',
                                            title_alignment=gui.ALIGN_CENTER,
                                            title_font=fonts.CHANNEL,
                                            placeholder=SETTINGS[strs.CHANNEL_NAME])
        
        # Layouts
        mainLayout = NoPadVBoxLayout()
        
        #   New/Delete Layout
        buttonLayout = NoPadHBoxLayout()
        buttonLayout.addWidget(self._newButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._deleteButton)
        
        #   Import/Export Layout
        importLayout = NoPadVBoxLayout()
        importLayout.addWidget(self._importButton)
        importLayout.addSpacing(10)
        importLayout.addWidget(self._exportButton)
        
        #   Play/Stop
        self._playLayout = QStackedLayout()
        self._playLayout.insertWidget(gui.index.PLAY_BUTTON, self._playButton)
        self._playLayout.insertWidget(gui.index.STOP_BUTTON, self._stopButton)
        self._playLayout.setCurrentIndex(gui.index.PLAY_BUTTON)
        
        #   Main Layout
        # mainLayout.addSpacing(10)
        mainLayout.addWidget(self._channelInput)
        mainLayout.addSpacing(40)
        mainLayout.addWidget(self._presetDropdown)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(importLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(self._playLayout)
        
        self.setLayout(mainLayout)
        
        # Connections
        self._newButton.clicked.connect(self.new_preset)
        self._exportButton.clicked.connect(self.create_export_window)
        self._presetDropdown.signals.textChanged.connect(lambda: self.signals.fillContainer.emit(self._presetDropdown.getCurrentText()))
        self._presetDropdown.signals.textChanged.connect(self._presetDropdown.clearAlert)
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
            
            msg.setFont(fonts.DEFAULT)
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
                cfg.delete_preset(preset)
            else:
                return

    @Slot()
    def play(self) -> None:
        '''Start the thread for listening and sending commands'''
        if not self._twitchManager.channelName:
            self._twitchManager.set_channel_name(self._channelInput.getText())
        if not self._twitchManager.channelName == SETTINGS[strs.CHANNEL_NAME]:
            cfg.update_setting(setting=strs.CHANNEL_NAME, value=self._twitchManager.channelName)
        
        if self._presetDropdown.alertActive:
            self._presetDropdown.clearAlert()
        if self._channelInput.alertActive:
            self._channelInput.clearAlert()
        
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
        self._nextRow = 0
        self._nextColumn = 0
        self._widgetCache: list[SingleCommandInputs | ComboCommandInputs] = []
        self.signals = ContainerSignals()
        
        self.setFixedSize(gui.COMMAND_CONTAINER_QSIZE)     
        
        rootLayout = NoPadVBoxLayout()
        rootLayout.setAlignment(gui.ALIGN_CENTER)
        
        margin = 15
        self._mainLayout = QGridLayout()
        self._mainLayout.setContentsMargins(margin, margin, margin, margin)
        self._mainLayout.setHorizontalSpacing(20)
        self._mainLayout.setVerticalSpacing(30)
        
        rootLayout.addLayout(self._mainLayout)
        rootLayout.addStretch()
        self.setLayout(rootLayout)
    
    @Slot(object)
    def add(self, cmd: Command) -> None:
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
        cfg.remove_command(preset_name=preset, nickname=nickname, cmd_type=self._cmdType)

    def fill(self, preset: str) -> None:
        self.clear()
        if preset and preset in list(PRESETS.keys()):
            allCmds = PRESETS[preset][self._cmdType]
            for cmd in allCmds:
                match self._cmdType:
                    case 'single':
                        newCmd = Command(cmd=cmd, type='single')
                    case 'combo':
                        newCmd = Command(cmd=cmd, type='combo')
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
        
class WidgetSignals(QObject):
    textChanged = Signal()
