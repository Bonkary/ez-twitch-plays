from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import widgets as wdgts
from constants import *
import sys
import os
import time
import popups

# NOTE: anywhere you see '# DEV' that just means its for development reasons only. It's not intended to stay forever.

class MainWindow(wdgts.CustomQMainWindow):
    '''Main Window to hold everything'''
    def __init__(self):
        super().__init__()

        self.setStyleSheet(styles.MAIN_WINDOW)
        self.setFixedSize(gui.sizes.MAIN_WINDOW)
        self.setWindowTitle("Ez Twitch Plays")
        self.setWindowIcon(QIcon(os.path.join('.', 'exe', 'EzTP.ico')))
        
        self.setBackgroundColor(colors.PURPLE)
        
        rootLayout = wdgts.NoPadHBoxLayout()
        self.setLayout(rootLayout)
        
        self._twitchPlays = TwitchPlays()
        
        rootLayout.addWidget(self._twitchPlays)
        self.setCentralWidget(self._twitchPlays)

    def exit(self) -> None:
        self._twitchPlays._controlManager._twitchManager.close()
        KILL_THREADS_FLAG.set()
        time.sleep(1) # Allow some time fo
        EXEC_THREAD.requestInterruption()
        EXEC_THREAD.quit()
        if THREAD_POOL.activeThreadCount() > 0:
            THREAD_POOL.waitForDone()

class TwitchPlays(wdgts.CustomQWidget):
    '''Primary widget for the app'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setBackgroundColor(colors.PURPLE)
        
        mainLayout = wdgts.NoPadVBoxLayout()
        mainLayout.setAlignment(gui.format.ALIGN_CENTER)
        self.setLayout(mainLayout)
        
        helpWindow = popups.Help(self)
        validKeysWindow = popups.ValidKeys(self)
        
        titleLabel = wdgts.BasicLabel(text="Ez Twitch Plays", alignment=gui.format.ALIGN_CENTER, font=fonts.TITLE, underline=True)
        self._controlManager = wdgts.ControlManager()
        self._singleInputs = wdgts.SingleCommandInputs(control_manager=self._controlManager)
        self._comboInputs = wdgts.ComboCommandInputs(control_manager=self._controlManager)
        self._singleCommandContainer = wdgts.CommandContainer(cmd_type=strs.SINGLE, control_manager=self._controlManager)
        self._comboCommandContainer = wdgts.CommandContainer(cmd_type=strs.COMBO, control_manager=self._controlManager)
        self._helpButton = wdgts.BasicPushButton(text="Help")
        self._validKeysButton = wdgts.BasicPushButton(text="Valid Keys")
        
        #  Header Layout
        headerButtonLayout = wdgts.NoPadHBoxLayout()
        headerButtonLayout.addWidget(self._validKeysButton)
        headerButtonLayout.addSpacing(30)
        headerButtonLayout.addWidget(self._helpButton)
        
        headerLayout = wdgts.NoPadHBoxLayout()
        headerLayout.addStretch()
        headerLayout.addSpacing(620)
        headerLayout.addWidget(titleLabel, alignment=gui.format.ALIGN_CENTER)
        headerLayout.addSpacing(390)
        headerLayout.addLayout(headerButtonLayout)
        headerLayout.addStretch()
        
        #   Inputs Layout
        inputsLayout = wdgts.NoPadHBoxLayout()
        inputsLayout.addWidget(self._singleInputs)
        inputsLayout.addWidget(self._controlManager)
        inputsLayout.addWidget(self._comboInputs)
        
        
        #   Containers Layout
        containerLayout = wdgts.NoPadHBoxLayout()
        containerLayout.addSpacing(20)
        containerLayout.addWidget(self._singleCommandContainer)
        containerLayout.addStretch()
        containerLayout.addWidget(self._comboCommandContainer)
        containerLayout.addSpacing(20)
        
        #   Main Layout
        mainLayout.addSpacing(10)
        mainLayout.addLayout(headerLayout)
        mainLayout.addSpacing(30)
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
        self._helpButton.clicked.connect(helpWindow.exec)
        self._validKeysButton.clicked.connect(validKeysWindow.show)

if __name__ == "__main__":
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(window.exit)
    
    sys.exit(app.exec())
