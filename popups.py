import sys
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot, Signal, QObject, QMargins
from PySide6.QtWidgets import *
from constants import *
import widgets as wdgts
from configurations import PRESETS, SETTINGS
import configurations as cfg
from typing import Literal
import json
import subprocess

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
        
        self._selectAllCheckbox = QCheckBox("Select all")
        self._selectAllCheckbox.setFont(const.gui.DEFAULT_FONT)
        self._clipboardCheckbox = QCheckBox("Copy file to clipboard")
        self._clipboardCheckbox.setFont(const.gui.DEFAULT_FONT)
        if SETTINGS[EXPORT][CLIPBOARD]:
            self._clipboardCheckbox.setCheckState(Qt.CheckState.Checked)
        exportButton = QPushButton("Export")
        exportButton.setStyleSheet("font-size: 15px;")
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(title, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(selectTitle, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(5)
        mainLayout.addLayout(presetsLayout)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self._selectAllCheckbox, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addStretch()
        mainLayout.addWidget(self._clipboardCheckbox, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(exportButton)
        mainLayout.addSpacing(50)
        
        
        exportButton.clicked.connect(self.export)
        self._clipboardCheckbox.stateChanged.connect(self.update_clipboard_setting)
        self._selectAllCheckbox.stateChanged.connect(self.select_all)
    
    def select_all(self) -> None:
        state = self._selectAllCheckbox.checkState()
        for checkbox in self._checkboxes:
            checkbox.setCheckState(state)
    
    def update_clipboard_setting(self) -> None:
        state = self._clipboardCheckbox.checkState()
        if state == Qt.CheckState.Checked:
            cfg.update_settings(setting='clipboard', value=True)
        else:
            cfg.update_settings(setting='clipboard', value=False)
    
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

        if SETTINGS[EXPORT]['clipboard']:
            path = os.path.abspath(exportPath)
            subprocess.run(['powershell', 'Set-Clipboard', '-LiteralPath', path])
        
        self.close()
            



       