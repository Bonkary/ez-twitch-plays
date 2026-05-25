from PySide6.QtWidgets import QFrame, QApplication, QMainWindow, QLabel, QWidget, QPushButton
import widgets as wdgts
from constants import *
import sys
from thread_objects import EXEC_THREAD
from platform_connections import KILLER
import time
import faulthandler
# faulthandler.enable()

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
                background: %s;
            }
            QLabel {
                color: %s;
            }
        """ % (colors.DARK_PURPLE, colors.PURPLE, colors.DARK_PURPLE, colors.DEFAULT_TEXT))
        
        self.setFixedSize(gui.MAIN_WINDOW_SIZE)
        self.setWindowTitle("Ez Twitch Plays")
        
        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), colors.PURPLE)
        self.setPalette(bg)
        
        rootLayout = wdgts.NoPadHBoxLayout()
        self.setLayout(rootLayout)
        
        self._twitchPlays = TwitchPlays()
        
        rootLayout.addWidget(self._twitchPlays)
        self.setCentralWidget(self._twitchPlays)

    def exit(self) -> None:
        self._twitchPlays._controlManager._twitchManager.close()
        KILLER.kill()
        time.sleep(1)
        EXEC_THREAD.terminate()
        sys.exit(0)

class TwitchPlays(QWidget):
    '''Primary widget for the app'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAutoFillBackground(True)
        bg = self.palette()
        bg.setColor(self.backgroundRole(), colors.PURPLE)
        self.setPalette(bg)
        
        mainLayout = wdgts.NoPadVBoxLayout()
        mainLayout.setAlignment(gui.ALIGN_CENTER)
        self.setLayout(mainLayout)
        
        titleLabel = wdgts.BasicLabel(text="Ez Twitch Plays", alignment=gui.ALIGN_CENTER, font=fonts.TITLE_FONT)
        
        self._controlManager = wdgts.ControlManager()
        self._singleInputs = wdgts.SingleCommandInputs(control_manager=self._controlManager)
        self._comboInputs = wdgts.ComboCommandInputs(control_manager=self._controlManager)
        self._singleCommandContainer = wdgts.CommandContainer(cmd_type=strs.SINGLE, control_manager=self._controlManager)
        self._comboCommandContainer = wdgts.CommandContainer(cmd_type=strs.COMBO, control_manager=self._controlManager)
        self._tutorialButton = QPushButton("Tutorial")
        self._validKeysButton = QPushButton("Valid Keys")
        
        # Header Layout
        headerLayout = wdgts.NoPadHBoxLayout()
        
        #  Buttons Layout
        headerButtonLayout = wdgts.NoPadHBoxLayout()
        headerButtonLayout.addWidget(self._tutorialButton)
        headerButtonLayout.addSpacing(10)
        headerButtonLayout.addWidget(self._validKeysButton)
        
        # Inputs
        inputsLayout = wdgts.NoPadHBoxLayout()
        inputsLayout.addWidget(self._singleInputs)
        inputsLayout.addWidget(self._controlManager)
        inputsLayout.addWidget(self._comboInputs)
        
        # Containers
        containerLayout = wdgts.NoPadHBoxLayout()
        containerLayout.addSpacing(20)
        containerLayout.addWidget(self._singleCommandContainer)
        containerLayout.addStretch()
        containerLayout.addWidget(self._comboCommandContainer)
        containerLayout.addSpacing(20)
        
        mainLayout.addSpacing(20)
        mainLayout.addWidget(titleLabel, alignment=gui.ALIGN_CENTER)
        mainLayout.addSpacing(10)
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
    app.aboutToQuit.connect(window.exit)
    
    sys.exit(app.exec())
