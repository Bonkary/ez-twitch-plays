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

class CustomQDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        
    def setBackgroundColor(self, color: str) -> None:
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), color)
        self.setPalette(bg)

class Export(CustomQDialog):
    '''Dialog window to choose how to export a Preset.'''
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._checkboxes: list[QCheckBox] = []
        
        # Widgets
        title = wdgts.BasicLabel("Export", font=fonts.TITLE)
        selectTitle = wdgts.BasicLabel("Select presets")
        self._selectAllCheckbox = wdgts.BasicCheckbox("Select all")
        self._clipboardCheckbox = wdgts.BasicCheckbox("Copy file to clipboard", checked=SETTINGS[strs.EXPORT][strs.CLIPBOARD])
        self._saveCheckbox = wdgts.BasicCheckbox("Save the actual file", checked=SETTINGS[strs.EXPORT][strs.SAVE])
        exportButton = wdgts.BasicPushButton(text="Export", stylesheet="font-size: 15px;", width=200, height=50)
        
        # Layouts
        self.setFixedSize(gui.EXPORT_WINDOW_SIZE)
        mainLayout = wdgts.NoPadVBoxLayout()
        mainLayout.setAlignment(gui.ALIGN_CENTER)
        
        #   Preset Layout
        presetsLayout = QGridLayout()
        presetsLayout.setSpacing(10)
        nextRow = 0
        nextCol = 0
        for preset in PRESETS:
            checkbox = wdgts.BasicCheckbox(text=preset)
            self._checkboxes.append(checkbox)
            presetsLayout.addWidget(checkbox, nextRow, nextCol)
            if nextCol == 1:
                nextCol = 0
                nextRow += 1
            else:
                nextCol += 1
        
        #   Main Layout
        mainLayout.addSpacing(20)
        mainLayout.addWidget(title, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(selectTitle, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(15)
        mainLayout.addLayout(presetsLayout)
        mainLayout.addStretch()
        mainLayout.addWidget(self._selectAllCheckbox, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self._saveCheckbox, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self._clipboardCheckbox, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(exportButton)
        mainLayout.addSpacing(15)
        
        self.setLayout(mainLayout)
        
        # Connections
        exportButton.clicked.connect(self.export)
        self._clipboardCheckbox.stateChanged.connect(self.update_clipboard_setting)
        self._selectAllCheckbox.stateChanged.connect(self.select_all_toggle)
        self._saveCheckbox.stateChanged.connect(self.update_save_setting)
    
    def select_all_toggle(self) -> None:
        '''Checks/unchecks all the checkboxes of Presets.'''
        state = self._selectAllCheckbox.checkState()
        for checkbox in self._checkboxes:
            checkbox.setCheckState(state)
    
    def update_save_setting(self) -> None:
        '''Save the last used export settings.'''
        saveState = self._saveCheckbox.checkState()
        if saveState == Qt.CheckState.Checked and not SETTINGS[strs.EXPORT][strs.SAVE] == True:
            cfg.update_setting(setting=strs.SAVE, value=True)
        elif saveState == Qt.CheckState.Unchecked and not SETTINGS[strs.EXPORT][strs.SAVE] == False:
            cfg.update_setting(setting=strs.SAVE, value=False)
    
    def update_clipboard_setting(self) -> None:
        '''Update the copy-to-clipboard setting'''
        clipboardState = self._clipboardCheckbox.checkState()
        if clipboardState == Qt.CheckState.Checked and not SETTINGS[strs.EXPORT][strs.CLIPBOARD] == True:
            cfg.update_setting(setting=strs.CLIPBOARD, value=True)
        elif clipboardState == Qt.CheckState.Unchecked and not SETTINGS[strs.EXPORT][strs.CLIPBOARD] == False:
            cfg.update_setting(setting=strs.CLIPBOARD, value=False)
    
    def export(self) -> None:
        '''
        Export the selected Presets.
        
        If the user selects to save the file, it will.
        If the user selected to copy the file to their clipboard, it will.
        If both are selected, it will.
        '''   
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
        if SETTINGS[strs.EXPORT][strs.SAVE]:
            path = QFileDialog.getExistingDirectory(parent=None, caption="Select Preset file", dir=SETTINGS[strs.EXPORT][strs.PREV_SAVE_PATH], options=QFileDialog.ShowDirsOnly)
            if path:
                savePath = os.path.join(SETTINGS[strs.EXPORT][strs.PREV_SAVE_PATH], 'preset_export.json')
                cfg.update_setting(setting=strs.PREV_SAVE_PATH, value=path)
                with open(savePath, 'w') as file:
                    file.write(json.dumps(presetExports))

        if SETTINGS[strs.EXPORT]['clipboard']:
            copyPath = os.path.abspath(tempPath)
            subprocess.run(['powershell', 'Set-Clipboard', '-LiteralPath', copyPath])
        
        self.close()
            
class Help(CustomQDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedSize(gui.HELP_WINDOW_SIZE)
        
        selector = wdgts.HelpSelection()
        self._display = wdgts.HelpDisplay()
        self._backButton = wdgts.BasicPushButton(text="Back", hide=True, width=150, height=40)
        
        self.stackedLayout = QStackedLayout()
        self.stackedLayout.insertWidget(gui.index.HELP_SELECTION, selector)
        self.stackedLayout.insertWidget(gui.index.HELP_DISPLAY, self._display)
        self.stackedLayout.setCurrentIndex(gui.index.HELP_SELECTION)
        
        mainLayout = wdgts.NoPadVBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(self.stackedLayout)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(self._backButton, alignment=gui.ALIGN_CENTER)
        mainLayout.addStretch()
        
        self.setLayout(mainLayout)
        
        selector.connectButton.clicked.connect(lambda: self.display_help('connect'))
        selector.cmdsButton.clicked.connect(lambda: self.display_help('commands'))
        selector.presetsButton.clicked.connect(lambda: self.display_help('presets'))
        selector.playButton.clicked.connect(lambda: self.display_help('play'))
        self._backButton.clicked.connect(self.back)
        
    def display_help(self, selection: str) -> None:
        match selection:
            case 'connect':
                self._display.connect_twitch()
            case 'commands':
                self._display.commands()
            case 'presets':
                self._display.presets()
            case 'play':
                self._display.play()
        self.stackedLayout.setCurrentIndex(gui.index.HELP_DISPLAY)
        self._backButton.show()
    
    def back(self) -> None:
        self.stackedLayout.setCurrentIndex(gui.index.HELP_SELECTION)
        self._backButton.hide()


class ValidKeys(CustomQDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
       