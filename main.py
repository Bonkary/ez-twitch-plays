from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot, Signal, QThread, QThreadPool
from PySide6.QtWidgets import QFrame, QApplication, QMainWindow, QLabel, QWidget
import widgets as wdgts
from constants import *
import sys
from configurations import update_preset, create_preset
from typing import Literal

class MainWindow(QMainWindow):
    '''Main Window to hold everything'''
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                border: 2px solid black;
                width: 100px;
                height: 20px;
                background: %s;
            }
            QPushButton:hover {
                background: %s;
            }
            QComboBox {
                border: 2px solid black;
                background: %s
            }
        """ % (const.colors.DARK_PURPLE, const.colors.TWITCH_PURPLE, const.colors.DARK_PURPLE))
        
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
    '''Primary widget for the app'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), const.colors.TWITCH_PURPLE)
        self.setPalette(bg)
        
        mainLayout = wdgts.NoPadVBoxLayout()
        mainLayout.setAlignment(const.gui.ALIGN_CENTER)
        self.setLayout(mainLayout)
        
        titleLabel = QLabel("Chat Plays", alignment=const.gui.ALIGN_CENTER)
        titleLabel.setFont(const.gui.TITLE_FONT)
        
        self._controlManager = wdgts.ControlManager()
        self._singleInputs = wdgts.SingleCommandInputs(control_manager=self._controlManager)
        self._comboInputs = wdgts.ComboCommandInputs(control_manager=self._controlManager)
        self._singleCommandContainer = wdgts.CommandContainer(cmd_type=SINGLE, control_manager=self._controlManager)
        self._comboCommandContainer = wdgts.CommandContainer(cmd_type=COMBO, control_manager=self._controlManager)
        
        # Inputs
        inputsLayout = wdgts.NoPadHBoxLayout()
        inputsLayout.addStretch()
        inputsLayout.addWidget(self._singleInputs)
        inputsLayout.addStretch()
        inputsLayout.addWidget(self._controlManager)
        inputsLayout.addStretch()
        inputsLayout.addWidget(self._comboInputs)
        inputsLayout.addStretch()
        
        # Containers
        containerLayout = wdgts.NoPadHBoxLayout()
        containerLayout.addSpacing(20)
        containerLayout.addWidget(self._singleCommandContainer)
        containerLayout.addStretch()
        containerLayout.addWidget(self._comboCommandContainer)
        containerLayout.addSpacing(20)
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(titleLabel, alignment=const.gui.ALIGN_CENTER)
        mainLayout.addLayout(inputsLayout)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(containerLayout)
        mainLayout.addStretch()
        
        self._singleInputs.signals.addCommand.connect(self._singleCommandContainer.add)
        self._comboInputs.signals.addCommand.connect(self._comboCommandContainer.add)
        self._controlManager.signals.fillContainer.connect(self._singleCommandContainer.fill)
        self._controlManager.signals.fillContainer.connect(self._comboCommandContainer.fill)
        self._controlManager.signals.clearContainer.connect(self._comboCommandContainer.clear)
        self._controlManager.signals.clearContainer.connect(self._singleCommandContainer.clear)
        









if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    
    sys.exit(app.exec())
