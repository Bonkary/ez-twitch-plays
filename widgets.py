import sys
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton
from PySide6.QtGui import QPalette, QFont
from constants import *
from typing import Literal, Any

class NamedDropdown(QFrame):
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
        
    def setPlaceholderText(self, text: str|int) -> None:
        self._dropdown.setPlaceholderText(text)
            
class NamedLineEdit(QFrame):
    def __init__(self, name: str, namePlacement: Literal['top', 'side'], titleFont: QFont = const.gui.DEFAULT_FONT, width: int = 100):
        super().__init__()
        match namePlacement:
            case 'top':
                mainLayout = NoPadVBoxLayout()
                mainLayout.setDirection(const.gui.TOP_TO_BOTTOM)
                alignment = const.gui.ALIGN_CENTER
            case 'side':
                mainLayout = NoPadHBoxLayout()
                mainLayout.setDirection(const.gui.LEFT_TO_RIGHT)
                alignment = const.gui.ALIGN_LEFT
            case _: 
                raise ValueError(f"{namePlacement} is not a valid value (must be 'top' or 'side')")
        self.setLayout(mainLayout)
        
        titleLabel = QLabel(text=name)
        titleLabel.setFont(const.gui.DEFAULT_FONT)
        
        self.entry = QLineEdit()
        self.entry.setFixedWidth(width)
        self.entry.setFont(const.gui.DEFAULT_FONT)
        
        mainLayout.addWidget(titleLabel, alignment=alignment)
        mainLayout.addSpacing(7)
        mainLayout.addWidget(self.entry, alignment)
        
    def getText(self) -> str:
        return self.entry.text().strip()
    
    def setText(self, text: str) -> None:
        self.entry.setText(text)

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

class VerticalCommandInputs(QFrame):
    def __init__(self, *, name: str):
        super().__init__()
        
        margin = 8
        rootLayout = NoPadVBoxLayout()
        rootLayout.setContentsMargins(margin,margin,margin,margin)
        self.setLayout(rootLayout)
        
        # ACTUAL WIDGET STARTS HERE
        mainFrame = QFrame() # idk why i put a frame in a frame, but i dont wanna fix it right now. maybe later.
        
        mainLayout = NoPadVBoxLayout()
        mainFrame.setLayout(mainLayout)
        
        titleFont = QFont()
        titleFont.setUnderline(True)
        titleFont.setPointSize(const.gui.DEFAULT_FONT.pointSize()+5)
        title = QLabel(text=name)
        title.setAlignment(const.gui.ALIGN_CENTER)
        title.setFont(titleFont)
        
        self._buttonInput = NamedLineEdit(name="Button", namePlacement='side')
        self._keyboardInput = NamedLineEdit(name="Keyboard", namePlacement='side')
        self._pressCmdInput = NamedLineEdit(name="Press Command", namePlacement='side')
        self._holdCmdInput = NamedLineEdit(name="Hold Command", namePlacement='side')
        self._probInput = NamedLineEdit(name="Probability (0-100)", namePlacement='side')
        
        spacing = 10
        mainLayout.addWidget(title)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(self._buttonInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._keyboardInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._pressCmdInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._holdCmdInput)
        mainLayout.addSpacing(spacing)
        mainLayout.addWidget(self._probInput)
        
        rootLayout.addWidget(mainFrame, alignment=const.gui.ALIGN_CENTER)
        rootLayout.addStretch(True)
        
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
            KEY: self._keyboardInput.getText().lower(),
            PRESS: self._pressCmdInput.getText().lower(),
            HOLD: self._holdCmdInput.getText().lower(),
            PROBABILITY: probInput
        }

    def load_inputs(self, inputs: dict):
        self._keyboardInput.setText(inputs[KEY])
        self._pressCmdInput.setText(inputs[PRESS])
        self._holdCmdInput.setText(inputs[HOLD])
        self._probInput.setText(str(inputs[PROBABILITY]))
    
    def clear_inputs(self) -> None:
        self._keyboardInput.setText("")
        self._pressCmdInput.setText("")
        self._holdCmdInput.setText("")
         
class HorizontalCommandInputs(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        mainLayout = NoPadHBoxLayout()
        self.setLayout(mainLayout)
        
        self._nicknameInput = NamedLineEdit(name='Nickname', namePlacement='top')
        self._keyInput = NamedLineEdit(name='Key', namePlacement='top')
        self._pressInput = NamedLineEdit(name='Press Cmd', namePlacement='top')




class ComboButtonInputs(QFrame):
    def __init__(self, *, configManager=None):
        super().__init__()

        mainLayout = NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        


   
        
        
        
        
        
