import sys
from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox
from PySide6.QtGui import QPalette, QFont
from constants import *
from typing import Literal, Any
from configurations import PRESETS, update_preset

# General
class TitledDropdown(QFrame):
    def __init__(self, *, title: str, titlePlacement: Literal['top', 'side'], titleFont: QFont = const.gui.DEFAULT_FONT):
        super().__init__()
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
        
    def addItem(self, item: str) -> None:
        self._dropdown.addItem(item)
        
    def setCurrentText(self, text: str|int) -> None:
        self._dropdown.setCurrentText(text)
        
    def setCurrentIndex(self, index: int) -> None:
        self._dropdown.setCurrentIndex(index)
        
    def getCurrentText(self) -> str:
        return self._dropdown.currentText()
        
    def setPlaceholderText(self, text: str|int) -> None:
        self._dropdown.setPlaceholderText(text)
            
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
        mainLayout.addWidget(self._entry, alignment=const.gui.ALIGN_RIGHT)
        
    def getText(self) -> str:
        return self._entry.text().strip()
    
    def setText(self, text: str) -> None:
        self._entry.setText(text)

    def clear(self) -> None:
        self._entry.setText("")

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
class InputSignals(QObject):
    addCommand = Signal(dict)

class VerticalCommandInputs(QFrame):
    def __init__(self):
        super().__init__()
        self.signals = InputSignals()
        
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
                probInput = int(self._probInput.getText())
            except ValueError:
                # JUST DEV STUFF RN
                print("not a valid value dude")
        else:
            probInput = 100
                
        return {
            NICKNAME: self._nicknameInput.getText().lower(),
            KEY: self._keyInput.getText().lower(),
            PRESS: self._pressCmdInput.getText().lower(),
            HOLD: self._holdCmdInput.getText().lower(),
            PROBABILITY: probInput
        }
    
    def clear_inputs(self) -> None:
        self._nicknameInput.clear()
        self._keyInput.clear()
        self._pressCmdInput.clear()
        self._holdCmdInput.clear()
        self._probInput.clear()

    def add(self) -> None:
        inputs = self.get_inputs()
        self.signals.addCommand.emit({
            inputs[NICKNAME]: {
                KEY: inputs[KEY],
                PRESS: inputs[PRESS],
                HOLD: inputs[HOLD],
                PROBABILITY: inputs[PROBABILITY]
            }
        })
        

class ComboButtonInputs(QFrame):
    def __init__(self):
        super().__init__()

        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        titleFont = QFont()
        titleFont.setPointSize(const.gui.DEFAULT_FONT.pointSize()+5)
        title = QLabel("New Button Combo")
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
        
class PresetManager(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        self._presetDropdown = TitledDropdown(title='Preset', titlePlacement='top')
        self._newButton = QPushButton(text='New')
        self._deleteButton = QPushButton(text='Delete')
        self._autosave = QCheckBox(text='Autosave')
        
        # Buttons
        buttonLayout = NoPadHBoxLayout()
        buttonLayout.addWidget(self._newButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self._deleteButton)
        
        mainLayout.addSpacing(50)
        mainLayout.addWidget(self._presetDropdown)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self._autosave, alignment=const.gui.ALIGN_CENTER)

    def get_preset(self) -> str:
        return self._presetDropdown.getCurrentText()

class BasicCommandsContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        mainLayout = None
        

        
        
        
