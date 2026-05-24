import sys
from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox, QInputDialog, QGridLayout, QFileDialog, QStyle, QMessageBox
from PySide6.QtGui import QPalette, QFont, QIcon
from constants import *
from typing import Literal, Any
from configurations import PRESETS, SETTINGS
import configurations as cfg
import shutil
import json
import subprocess
import popups

# General 
class TitledDropdown(QFrame):
    def __init__(self, *, title: str, titlePlacement: Literal['top', 'side'], titleFont: QFont = const.gui.DEFAULT_FONT):
        super().__init__()
        self.signals = DropwdownSignals()
        self._values: list[str] = []
        
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
        self._dropdown.setFixedWidth(200)
        self._dropdown.setContentsMargins(0,0,0,0)
        
        mainLayout.addWidget(titleLabel, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addWidget(self._dropdown)
        
        self._dropdown.currentTextChanged.connect(self.signals.textChanged.emit)
        
    def addItem(self, item: str) -> None:
        self._dropdown.addItem(item)
        self._values.append(item)
        
    def setCurrentText(self, text: str|int) -> None:
        self._dropdown.setCurrentText(text)
        
    def setCurrentIndex(self, index: int) -> None:
        self._dropdown.setCurrentIndex(index)
        
    def getCurrentText(self) -> str:
        return self._dropdown.currentText().strip()
        
    def setPlaceholderText(self, text: str|int) -> None:
        self._dropdown.setPlaceholderText(text)
        
    def removeItem(self, item: str) -> None:
        self._values.remove(item)
        self._dropdown.clear()
        for value in self._values:
            self._dropdown.addItem(value)
            
class TitledLineEdit(QFrame):
    def __init__(self, *, title: str, titlePlacement: Literal['top', 'side'], 
                 titleFont: QFont = const.gui.DEFAULT_FONT,
                 titleAlignment: Literal['left', 'right', 'center'] = 'left',
                 spacing: int = 10, width: int = 100,):
        super().__init__()
        match titlePlacement:
            case 'top':
                mainLayout = NoPadVBoxLayout()
                mainLayout.setDirection(const.gui.TOP_TO_BOTTOM)
                alignment = const.gui.ALIGN_CENTER
            case 'side':
                mainLayout = NoPadHBoxLayout()
                mainLayout.setDirection(const.gui.LEFT_TO_RIGHT)
                alignment = const.gui.ALIGN_LEFT
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
        self._entry.setFixedWidth(width)
        self._entry.setFont(const.gui.DEFAULT_FONT)

        mainLayout.addWidget(titleLabel, alignment=titleAlignment)
        mainLayout.addSpacing(spacing)
        if titlePlacement == 'side':
            mainLayout.addStretch()
        mainLayout.addWidget(self._entry, alignment=alignment)
        
    def getText(self) -> str:
        return self._entry.text().strip()
    
    def setText(self, text: str) -> None:
        self._entry.setText(text)

    def clear(self) -> None:
        self._entry.setText("")

class TitledLabel(QFrame):
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(const.gui.ALIGN_TOP|const.gui.ALIGN_CENTER)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        
class NoPadVBoxLayout(QVBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setAlignment(const.gui.ALIGN_TOP|const.gui.ALIGN_CENTER)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

# Inputs
class SingleCommandInputs(QFrame):
    def __init__(self, preset_manager: PresetManager, parent=None):
        super().__init__(parent)
        self.signals = InputSignals()
        self._presetManager = preset_manager
        
        margin = 8
        rootLayout = NoPadHBoxLayout()
        rootLayout.setContentsMargins(margin,margin,margin,margin)
        self.setLayout(rootLayout)
        
        # ACTUAL WIDGET STARTS HERE
        mainFrame = QFrame() # idk why i put a frame in a frame, but i dont wanna fix it right now. maybe later.
        
        mainLayout = NoPadVBoxLayout()
        mainFrame.setLayout(mainLayout)
        
        # Title
        titleFont = QFont()
        titleFont.setPointSize(const.gui.DEFAULT_FONT.pointSize()+5)
        title = QLabel(text="New Command")
        title.setAlignment(const.gui.ALIGN_CENTER)
        title.setFont(titleFont)
        
        # Inputs
        self._nicknameInput = TitledLineEdit(title="Nickname", titlePlacement='side')
        self._keyInput = TitledLineEdit(title="Key", titlePlacement='side')
        self._pressCmdInput = TitledLineEdit(title="Press Cmd", titlePlacement='side')
        self._holdCmdInput = TitledLineEdit(title="Hold Cmd", titlePlacement='side')
        self._probInput = TitledLineEdit(title="Probability (0-100)", titlePlacement='side')
        
        # Buttons
        buttonLayout = NoPadHBoxLayout()
        self._clearButton = QPushButton(text="Clear")
        self._clearButton.setStyleSheet("font-size: 15px;")
        self._addButton = QPushButton(text="Add")
        self._addButton.setStyleSheet("font-size: 15px;")
        buttonLayout.addWidget(self._clearButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._addButton)
        
        spacing = 10
        mainLayout.addWidget(title)
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
        rootLayout.addWidget(mainFrame)
        rootLayout.addStretch()
        
        self._addButton.clicked.connect(self.add)
        self._clearButton.clicked.connect(self.clear_inputs)
        
    def get_inputs(self) -> dict:
        if self._probInput.getText():
            try:
                prob = int(self._probInput.getText())
            except ValueError:
                # JUST DEV STUFF RN
                print("not a valid value dude")
                prob = 0
        else:
            prob = 100
                
        return {
            NICKNAME: self._nicknameInput.getText().lower(),
            KEY: self._keyInput.getText().lower(),
            PRESS: self._pressCmdInput.getText().lower(),
            HOLD: self._holdCmdInput.getText().lower(),
            PROBABILITY: prob
        }
    
    def clear_inputs(self) -> None:
        self._nicknameInput.clear()
        self._keyInput.clear()
        self._pressCmdInput.clear()
        self._holdCmdInput.clear()
        self._probInput.clear()

    def add(self) -> None:
        # TODO: check for valid inputs
        inputs = self.get_inputs()
        cmd = {
            inputs[NICKNAME]: {
                KEY: inputs[KEY],
                PRESS: inputs[PRESS],
                HOLD: inputs[HOLD],
                PROBABILITY: inputs[PROBABILITY]
            }
        }
        
        presetName = self._presetManager.get_preset()
        if not presetName:
            name, ok = QInputDialog.getText(self, "New Preset Name",'Give preset name. If not, no save.', QLineEdit.Normal, "")
            if ok and name:
                cfg.create_preset(preset_name=name, cmd=cmd, cmd_type=SINGLE)
                self._presetManager.add_preset(name)
        else:
            cfg.update_preset(preset=presetName, cmd=cmd, cmd_type=SINGLE)
        
        newCmd = SingleCommand(cmd=cmd)
        self.signals.addCommand.emit(newCmd)
        self.clear_inputs()
            
class ComboCommandInputs(QFrame):
    def __init__(self, preset_manager: PresetManager, parent=None):
        super().__init__(parent)
        self._presetManager = preset_manager
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        self.signals = InputSignals()
        
        titleFont = QFont()
        titleFont.setPointSize(const.gui.DEFAULT_FONT.pointSize()+5)
        title = QLabel("New Combo Command")
        title.setAlignment(const.gui.ALIGN_CENTER)
        title.setFont(titleFont)
        
        self._nicknameInput = TitledLineEdit(title='Nickname', titlePlacement='side', spacing=22)
        
        keyLayout = NoPadHBoxLayout()
        self._key1Input = TitledLineEdit(title="Key 1", titlePlacement='side')
        self._key2Input = TitledLineEdit(title="Key 2", titlePlacement='side')
        keyLayout.addStretch()
        keyLayout.addWidget(self._key1Input)
        keyLayout.addSpacing(10)
        keyLayout.addWidget(self._key2Input)
        keyLayout.addStretch()
        
        self._pressInput = TitledLineEdit(title='Press Cmd', titlePlacement='side', spacing=15, titleAlignment='right')
        self._holdInput = TitledLineEdit(title='Hold Cmd', titlePlacement='side', spacing=22, titleAlignment='right')
        self._probInput = TitledLineEdit(title='Probability', titlePlacement='side', spacing=14, titleAlignment='right')
        
        # Buttons
        buttonLayout = NoPadHBoxLayout()
        self._clearButton = QPushButton(text="Clear")
        self._clearButton.setStyleSheet("font-size: 15px;")
        self._addButton = QPushButton(text="Add")
        self._addButton.setStyleSheet("font-size: 15px;")
        buttonLayout.addWidget(self._clearButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._addButton)
        
        spacing = 10
        mainLayout.addWidget(title)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(self._nicknameInput, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addLayout(keyLayout)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._pressInput, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._holdInput, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._probInput, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addStretch()
        
        self._clearButton.clicked.connect(self.clear_inputs)
        self._addButton.clicked.connect(self.add)

    def clear_inputs(self) -> None:
        self._nicknameInput.clear()
        self._key1Input.clear()
        self._key2Input.clear()
        self._pressInput.clear()
        self._holdInput.clear()
        self._probInput.clear()
    
    def get_inputs(self) -> dict:
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
            NICKNAME: self._nicknameInput.getText().lower(),
            KEY1: self._key1Input.getText().lower(),
            KEY2: self._key2Input.getText().lower(),
            PRESS: self._pressInput.getText().lower(),
            HOLD: self._holdInput.getText().lower(),
            PROBABILITY: prob
        }
    
    def add(self) -> None:
        inputs = self.get_inputs()
        cmd = {
            inputs[NICKNAME]: {
                KEY1: inputs[KEY1],
                KEY2: inputs[KEY2],
                PRESS: inputs[PRESS],
                HOLD: inputs[HOLD],
                PROBABILITY: inputs[PROBABILITY]
            }
        }
        
        presetName = self._presetManager.get_preset()
        if not presetName:
            name, ok = QInputDialog.getText(self, "New Preset Name",'Give preset name. If not, no save.', QLineEdit.Normal, "")
            if ok and name:
                cfg.create_preset(preset_name=name, cmd=cmd, cmd_type=COMBO)
                self._presetManager.add_preset(name)
        else:
            cfg.update_preset(preset=presetName, cmd=cmd, cmd_type=COMBO)
        
        newCmd = ComboCommand(cmd=cmd)
        self.signals.addCommand.emit(newCmd)
        self.clear_inputs()

class SingleCommand(QFrame):
    def __init__(self, cmd: dict, parent=None):
        super().__init__(parent)
        self.signals = CommandSignals()
        
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        self.nickname = list(cmd.keys())[0]
        key = cmd[self.nickname][KEY]
        pressCmd = cmd[self.nickname][PRESS]
        holdCmd = cmd[self.nickname][HOLD]
        prob = cmd[self.nickname][PROBABILITY]
        
        # Nickname
        nicknameLayout = NoPadHBoxLayout()
        nicknameLabel = QLabel(self.nickname)
        nicknameFont = QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=15)
        nicknameFont.setUnderline(True)
        nicknameLabel.setFont(nicknameFont)
        
        trashIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)
        self.trashButton = QPushButton(flat=True)
        self.trashButton.setStyleSheet(f"background-color: {const.colors.TWITCH_PURPLE}")
        self.trashButton.setIcon(QIcon(trashIcon))
        
        nicknameLayout.addWidget(nicknameLabel)
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
        self.signals.deleteCommand.emit(self.nickname)

class ComboCommand(QFrame):
    def __init__(self, cmd: dict, parent=None):
        super().__init__(parent)
        self.signals = CommandSignals()
        
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        self.nickname = list(cmd.keys())[0]
        key1 = cmd[self.nickname][KEY1]
        key2 = cmd[self.nickname][KEY2]
        pressCmd = cmd[self.nickname][PRESS]
        holdCmd = cmd[self.nickname][HOLD]
        prob = cmd[self.nickname][PROBABILITY]
        
        # Nickname
        nicknameLayout = NoPadHBoxLayout()
        nicknameLabel = QLabel(self.nickname)
        nicknameFont = QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=15)
        nicknameFont.setUnderline(True)
        nicknameLabel.setFont(nicknameFont)
        
        trashIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)
        self.trashButton = QPushButton(flat=True)
        self.trashButton.setStyleSheet(f"background-color: {const.colors.TWITCH_PURPLE}")
        self.trashButton.setIcon(QIcon(trashIcon))
        
        nicknameLayout.addWidget(nicknameLabel)
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
        self.signals.deleteCommand.emit(self.nickname)

# Managers
class PresetManager(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = ManagerSignals()
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        self._presetDropdown = TitledDropdown(title='Preset', titlePlacement='top')
        for name in PRESETS:
            self._presetDropdown.addItem(name)
        self._presetDropdown.setCurrentIndex(-1)
        
        self._newButton = QPushButton(text='New')
        self._deleteButton = QPushButton(text='Delete')
        self._autosave = QCheckBox(text='Autosave')
        self._importButton = QPushButton(text='Import')
        self._exportButton = QPushButton(text='Export')
        
        # New/Delete Layout
        buttonLayout = NoPadHBoxLayout()
        buttonLayout.addWidget(self._newButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._deleteButton)
        
        # Import/Export Layout
        importLayout = NoPadVBoxLayout()
        importLayout.addWidget(self._importButton)
        importLayout.addSpacing(5)
        importLayout.addWidget(self._exportButton)
        
        # Main Layout
        mainLayout.addSpacing(50)
        mainLayout.addWidget(self._presetDropdown)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(5)
        mainLayout.addLayout(importLayout)
        
        self._newButton.clicked.connect(self.new_preset)
        self._exportButton.clicked.connect(self.export)
        self._presetDropdown.signals.textChanged.connect(lambda: self.signals.fillContainer.emit(self._presetDropdown.getCurrentText()))
        self._deleteButton.clicked.connect(self.delete)
        
        
    def get_preset(self) -> str:
        return self._presetDropdown.getCurrentText().strip()

    def add_preset(self, name: str) -> None:
        self._presetDropdown.addItem(name)
        self._presetDropdown.setCurrentText(name)
        self.signals.clearContainer.emit()
        
    def new_preset(self) -> None:
        name, ok = QInputDialog.getText(self, "New Preset Name", "Give name for preset.", QLineEdit.Normal, "")
        if name and ok:
            cfg.create_preset(preset_name=name)
            self.add_preset(name)
            
    def import_presets(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select Preset file", "", "JSON files (*.json)")
        if path:
            with open(path, 'r') as file:
                newPresets = json.loads(file.read())
            
            presetList = []
            for preset in newPresets:
                presetList.append(newPresets[preset])
                self._presetDropdown.addItem(preset)
            cfg.add_imports(presetList)
            
    def export(self) -> None:
        popup = popups.Export()
        popup.exec()

    def delete(self) -> None:
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

# Containers
# TODO: figure out handling duplicate nicknames 
class CommandContainer(QFrame):
    def __init__(self, preset_manager: PresetManager, cmd_type: Literal['single', 'combo'], parent=None):
        super().__init__(parent)
        self._presetManager = preset_manager
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
        print("tu")
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
        if preset:
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
        
