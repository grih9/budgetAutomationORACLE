from PyQt5 import QtWidgets

import loginwindow
import regFanWindow
from StartMenuWindow import Ui_MainWindow as StartWindow


class StartMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = StartWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Добро пожаловать!")
        self.ui.enter_button.clicked.connect(self.enter_button_clicked)
        self.ui.register_button.clicked.connect(self.register_button_clicked)

    def enter_button_clicked(self):
        self.login = loginwindow.loginindow()
        self.login.show()
        self.close()

    def register_button_clicked(self):
        self.reg = regFanWindow.regFanWindow()
        self.reg.show()
        self.close()
