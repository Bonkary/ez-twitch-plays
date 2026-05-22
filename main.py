from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot, Signal, QThread, QThreadPool
from PySide6.QtWidgets import QFrame, QApplication, QMainWindow, QLabel, QWidget
import widgets as wdgts
from constants import *
import sys


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
        
        self._dropdown = wdgts.NamedDropdown(title="Console", titlePlacement='top')
        
        inputsLayout = wdgts.NoPadVBoxLayout()
        
        self._singleInputs = wdgts.VerticalCommandInputs(name="New Command")
        self._comboInputs = wdgts.ComboButtonInputs()
        
        inputsLayout.addStretch()
        inputsLayout.addWidget(self._singleInputs)
        inputsLayout.addWidget(self._comboInputs)
        inputsLayout.addStretch()
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(titleLabel)
        mainLayout.addSpacing(200)
        mainLayout.addLayout(inputsLayout)
        mainLayout.addStretch()
        
        









if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    
    sys.exit(app.exec())
