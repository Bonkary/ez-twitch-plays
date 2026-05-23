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
        self._singleInputs = wdgts.SingleButtonInputs(preset_manager=self._presetManager)
        self._singleInputs.signals.add.connect(self.add_single_cmd)
        self._comboInputs = wdgts.ComboButtonInputs(preset_manager=self._presetManager)
        self._comboInputs.signals.add.connect(self.add_combo_cmd)
         
        inputsLayout.addSpacing(100)
        inputsLayout.addWidget(self._singleInputs)
        inputsLayout.addWidget(self._presetManager)
        inputsLayout.addWidget(self._comboInputs)
        inputsLayout.addSpacing(100)
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(inputsLayout)
        mainLayout.addStretch()
    
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
