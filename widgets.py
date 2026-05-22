import sys
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton
from PySide6.QtGui import QPalette, QFont
from constants import *
from typing import Literal, Any

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
class VerticalCommandInputs(QFrame):
    def __init__(self):
        super().__init__()
        
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
        
    def get_inputs(self) -> dict:
        try:
            probInput = int(self._probInput.getText())
        except ValueError:
            if not probInput:
                probInput = 100
            else:
                print("prob needs to be a whole number")
                probInput = 100 # DEV STUFF
                
        return {
            KEY: self._keyInput.getText().lower(),
            PRESS: self._pressCmdInput.getText().lower(),
            HOLD: self._holdCmdInput.getText().lower(),
            PROBABILITY: probInput
        }

    def load_inputs(self, inputs: dict) -> None:
        self._keyInput.setText(inputs[KEY])
        self._pressCmdInput.setText(inputs[PRESS])
        self._holdCmdInput.setText(inputs[HOLD])
        self._probInput.setText(str(inputs[PROBABILITY]))
    
    def clear_inputs(self) -> None:
        self._keyInput.setText("")
        self._pressCmdInput.setText("")
        self._holdCmdInput.setText("")
         
class HorizontalCommandInputs(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        mainLayout = NoPadHBoxLayout()
        self.setLayout(mainLayout)
        
        self._nicknameInput = TitledLineEdit(title='Nickname', titlePlacement='top')
        self._keyInput = TitledLineEdit(title='Key', titlePlacement='top')
        self._pressInput = TitledLineEdit(title='Press Cmd', titlePlacement='top')

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
        
        

   
        
        
        
        
        
