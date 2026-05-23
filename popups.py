import sys
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot, Signal, QObject, QMargins
from PySide6.QtWidgets import *
from constants import *
import widgets as wdgts
from configurations import PRESETS, SETTINGS
from typing import Literal
import json

class Export(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._checkboxes: list[QCheckBox] = []
        
        self.setFixedSize(const.gui.EXPORT_WINDOW_SIZE)
        
        mainLayout = wdgts.NoPadVBoxLayout()
        mainLayout.setAlignment(const.gui.ALIGN_CENTER)
        self.setLayout(mainLayout)

        title = QLabel("Export")
        title.setFont(QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=20))
        
        # Preset Layout
        margin = 20
        selectFont = QFont(const.gui.DEFAULT_FONT_FAMILY, pointSize=15)
        selectFont.setUnderline(True)
        selectTitle = QLabel("Select presets")
        selectTitle.setFont(selectFont)
        presetsLayout = QGridLayout()
        presetsLayout.setSpacing(10)
        nextRow = 0
        nextCol = 0
        for preset in PRESETS:
            checkbox = QCheckBox(text=preset)
            checkbox.setFont(const.gui.DEFAULT_FONT)
            self._checkboxes.append(checkbox)
            presetsLayout.addWidget(checkbox, nextRow, nextCol)
            if nextCol == 3:
                nextCol += 1
                nextRow = 0
            else:
                nextCol += 1
        
        selectAllCheckbox = QCheckBox("Select all")
        selectAllCheckbox.setFont(const.gui.DEFAULT_FONT)
        clipboardCheckbox = QCheckBox("Copy file to clipboard")
        clipboardCheckbox.setFont(const.gui.DEFAULT_FONT)
        exportButton = QPushButton("Export")
        exportButton.setStyleSheet("font-size: 15px;")
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(title, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(selectTitle, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(5)
        mainLayout.addLayout(presetsLayout)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(selectAllCheckbox, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(clipboardCheckbox, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(exportButton)
        mainLayout.addStretch()
        
        exportButton.clicked.connect(self.export)
    
    def export(self) -> None:
        toExport = []
        for checkbox in self._checkboxes:
            isChecked = checkbox.checkState()
            if isChecked == Qt.CheckState.Checked:
                toExport.append(checkbox.text())
        
        presetExports = {}
        for preset in toExport:
            presetExports.update({preset: PRESETS[preset]})
        
        exportPath = os.path.join(dirs.DOWNLOADS, 'preset_export.json')
        with open(exportPath, 'w') as file:
            file.write(json.dumps(presetExports))
            
        self.close()
            



       