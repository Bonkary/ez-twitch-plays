from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot, Signal, QThread, QThreadPool
from PySide6.QtWidgets import QFrame, QApplication, QMainWindow, QLabel, QWidget
import widgets as wdgts
from constants import *
import sys
from configurations import update_preset, create_preset
from typing import Literal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(const.gui.MAIN_WINDOW_SIZE)
        self.setWindowTitle("Ez Twitch Plays")
        
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), const.colors.TWITCH_PURPLE)
        self.setPalette(bg)
        
        rootLayout = wdgts.NoPadHBoxLayout()
        self.setLayout(rootLayout)
        
        twitchPlays = TwitchPlays()
        
        rootLayout.addWidget(twitchPlays)
        self.setCentralWidget(twitchPlays)
        

class TwitchPlays(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), const.colors.TWITCH_PURPLE)
        self.setPalette(bg)
        
        mainLayout = wdgts.NoPadVBoxLayout()
        mainLayout.setAlignment(const.gui.ALIGN_CENTER)
        self.setLayout(mainLayout)
        
        titleLabel = QLabel("Ez Twitch Plays", alignment=const.gui.ALIGN_CENTER)
        titleLabel.setFont(const.gui.TITLE_FONT)
        
        inputsLayout = wdgts.NoPadHBoxLayout()
        
        self._presetManager = wdgts.PresetManager()
        self._singleInputs = wdgts.SingleCommandInputs(preset_manager=self._presetManager)
        self._singleInputs.signals.addCommand.connect(self.add_single_cmd)
        self._comboInputs = wdgts.ComboCommandInputs(preset_manager=self._presetManager)
        self._comboInputs.signals.addCommand.connect(self.add_combo_cmd)
        
        self._singleCommandContainer = wdgts.CommandContainer(cmd_type=SINGLE, preset_manager=self._presetManager)
        self._comboCommandContainer = wdgts.CommandContainer(cmd_type=COMBO, preset_manager=self._presetManager)
        
        # Inputs
        inputsLayout.addSpacing(0)
        inputsLayout.addWidget(self._singleInputs)
        inputsLayout.addWidget(self._presetManager)
        inputsLayout.addWidget(self._comboInputs)
        inputsLayout.addSpacing(0)
        
        # Containers
        containerLayout = wdgts.NoPadHBoxLayout()
        containerLayout.addSpacing(20)
        containerLayout.addWidget(self._singleCommandContainer)
        containerLayout.addStretch()
        containerLayout.addWidget(self._comboCommandContainer)
        containerLayout.addSpacing(20)
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(inputsLayout)
        mainLayout.addLayout(containerLayout)
        mainLayout.addStretch()
        
        self._singleInputs.signals.addCommand.connect(self._singleCommandContainer.add)
        self._comboInputs.signals.addCommand.connect(self._comboCommandContainer.add)
        self._presetManager.signals.fillContainer.connect(self._singleCommandContainer.fill)
        self._presetManager.signals.fillContainer.connect(self._comboCommandContainer.fill)
        self._presetManager.signals.clearContainer.connect(self._comboCommandContainer.clear)
        self._presetManager.signals.clearContainer.connect(self._singleCommandContainer.clear)
    
    def add_single_cmd(self, cmd: dict) -> None:
        pass
    
    def add_combo_cmd(self, cmd: dict) -> None:
        pass
    
    def add_command(self, cmd: tuple) -> None:
        pass
    
    def add_preset(self, preset: tuple) -> None:
        pass
        









if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    
    sys.exit(app.exec())
