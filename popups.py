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
            if nextCol == 1:
                nextCol = 0
                nextRow += 1
            else:
                nextCol += 1
        
        self._selectAllCheckbox = QCheckBox("Select all")
        self._selectAllCheckbox.setFont(const.gui.DEFAULT_FONT)
        self._clipboardCheckbox = QCheckBox("Copy file to clipboard")
        self._clipboardCheckbox.setFont(const.gui.DEFAULT_FONT)
        self._saveCheckbox = QCheckBox("Save the actual file")
        self._saveCheckbox.setFont(const.gui.DEFAULT_FONT)
        if SETTINGS[EXPORT][CLIPBOARD]:
            self._clipboardCheckbox.setCheckState(Qt.CheckState.Checked)
        if SETTINGS[EXPORT][SAVE]:
            self._saveCheckbox.setCheckState(Qt.CheckState.Checked)
        exportButton = QPushButton("Export")
        exportButton.setStyleSheet("font-size: 15px;")
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(title, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(selectTitle, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(15)
        mainLayout.addLayout(presetsLayout)
        mainLayout.addStretch()
        mainLayout.addWidget(self._selectAllCheckbox, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self._saveCheckbox, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self._clipboardCheckbox, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addSpacing(10)
        
        mainLayout.addWidget(exportButton)
        mainLayout.addSpacing(15)
        
        
        exportButton.clicked.connect(self.export)
        self._clipboardCheckbox.stateChanged.connect(self.update_clipboard_setting)
        self._selectAllCheckbox.stateChanged.connect(self.select_all)
        self._saveCheckbox.stateChanged.connect(self.update_save_setting)
    
    def select_all(self) -> None:
        state = self._selectAllCheckbox.checkState()
        for checkbox in self._checkboxes:
            checkbox.setCheckState(state)
    
    def update_save_setting(self) -> None:
        saveState = self._saveCheckbox.checkState()
        if saveState == Qt.CheckState.Checked and not SETTINGS[EXPORT][SAVE] == True:
            cfg.update_setting(setting=SAVE, value=True)
        elif saveState == Qt.CheckState.Unchecked and not SETTINGS[EXPORT][SAVE] == False:
            cfg.update_setting(setting=SAVE, value=True)
    
    def update_clipboard_setting(self) -> None:
        clipboardState = self._clipboardCheckbox.checkState()
        if clipboardState == Qt.CheckState.Checked and not SETTINGS[EXPORT][CLIPBOARD] == True:
            cfg.update_setting(setting=CLIPBOARD, value=True)
        elif clipboardState == Qt.CheckState.Unchecked and not SETTINGS[EXPORT][CLIPBOARD] == False:
            cfg.update_setting(setting=CLIPBOARD, value=False)
    
    def export(self) -> None:        
        toExport = []
        for checkbox in self._checkboxes:
            isChecked = checkbox.checkState()
            if isChecked == Qt.CheckState.Checked:
                toExport.append(checkbox.text())
        
        if not toExport:
            QMessageBox.about(None, "Uhhhhh", "You didn't select any presets...")
            return
        
        presetExports = {}
        for preset in toExport:
            presetExports.update({preset: PRESETS[preset]})
        
        tempPath = os.path.join(dirs.TEMP, 'preset_export.json')
        if not os.path.exists(dirs.TEMP):
            os.makedirs(dirs.TEMP, exist_ok=True)
        with open(tempPath, 'w') as file:
            file.write(json.dumps(presetExports))
        
        path = ''
        savePath = ''
        if SETTINGS[EXPORT][SAVE]:
            path = QFileDialog.getExistingDirectory(parent=None, caption="Select Preset file", dir=SETTINGS[EXPORT][PREV_SAVE_PATH], options=QFileDialog.ShowDirsOnly)
            if path:
                savePath = os.path.join(SETTINGS[EXPORT][PREV_SAVE_PATH], 'preset_export.json')
                cfg.update_setting(setting=PREV_SAVE_PATH, value=path)
                with open(savePath, 'w') as file:
                    file.write(json.dumps(presetExports))

        if SETTINGS[EXPORT]['clipboard']:
            copyPath = os.path.abspath(tempPath)
            subprocess.run(['powershell', 'Set-Clipboard', '-LiteralPath', copyPath])
        
        self.close()
            



       