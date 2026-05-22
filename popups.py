import sys
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtWidgets import *
from constants import *
import widgets as wdgts
from configurations import add_new_preset
from typing import Literal

class Keymappings(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.resize(gui.KEYMAP_WINDOW_WIDTH, gui.KEYMAP_WINDOW_HEIGHT)
        
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), '#353836')
        self.setPalette(bg)

        mainLayout = wdgts.NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        # Title
        titleFont = QFont()
        titleFont.setWeight(QFont.Weight.Bold)
        titleFont.setPixelSize(40)
        title = QLabel("Keymappings")
        title.setStyleSheet(f"color: white")
        title.setFont(titleFont)
        
        mainLayout.addSpacing(40)
        mainLayout.addWidget(title, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(50)
        
        # Mappings
        mappingsLayout = wdgts.NoPadHBoxLayout()
        mappingsLayout.setAlignment(gui.ALIGN_CENTER)
        col1 = wdgts.NoPadVBoxLayout()
        col2 = wdgts.NoPadVBoxLayout()
        mapFont = QFont()
        mapFont.setPixelSize(20)
        
        # Left Col
        colCount = len(keys.USER_FRIENDLY_KEYBOARD_MAPPINGS) // 2
        for key in keys.USER_FRIENDLY_KEYBOARD_MAPPINGS[:colCount]:
            newMapping = QLabel(key)
            newMapping.setFont(mapFont)
            col1.addWidget(newMapping)
            col1.addSpacing(20)
        
        # Right Col
        for key in keys.USER_FRIENDLY_KEYBOARD_MAPPINGS[colCount:]:
            newMapping = QLabel(key)
            newMapping.setFont(mapFont)
            col2.addWidget(newMapping)
            col2.addSpacing(20)
            
        mappingsLayout.addLayout(col1)
        mappingsLayout.addSpacing(200)
        mappingsLayout.addLayout(col2)
        
        mainLayout.addLayout(mappingsLayout)

class PresetSignals(QObject):
    addPreset = Signal(tuple)

class PresetNamePrompt(QDialog):
    def __init__(self, command: dict, parent=None):
        super().__init__(parent)
        self._command = command
        self.signals = PresetSignals()
        
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), '#353836')
        self.setPalette(bg)
        
        self.setFixedSize(const.gui.PROMPT_WINDOW_SIZE)

        mainLayout = wdgts.NoPadVBoxLayout()
        self.setLayout(mainLayout)
        
        promptFont = QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=15)
        self._presetName = wdgts.TitledLineEdit(title="I need a preset name.", titlePlacement='top', titleAlignment='center', titleFont=promptFont, width=200)
        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        
        buttonLayout = wdgts.NoPadHBoxLayout()
        buttonLayout.addWidget(saveButton)
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(cancelButton)
        
        mainLayout.addStretch()
        mainLayout.addWidget(self._presetName)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addStretch()
        
        saveButton.clicked.connect(self.save)
        cancelButton.clicked.connect(self.close)
        
    def save(self):
        name = self._presetName.getText()
        add_new_preset(name, self._command)
        self.signals.addPreset.emit((name))
        self.close()



       