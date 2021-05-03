from PyQt5 import QtWidgets

import properties
from register_window import Ui_MainWindow as register_window
import start_menu
import sql

class RegisterMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = register_window()
        self.ui.setupUi(self)
        self.setWindowTitle("Регистрация пользователя")
        self.ui.backButton.clicked.connect(self.back_button_clicked)
        self.ui.passwod_checkbox.stateChanged.connect(self.checkbox_handler)
        self.ui.create_account_button.clicked.connect(self.create_button_clicked)

    def back_button_clicked(self):
        self.main = start_menu.StartMenu()
        self.main.show()
        self.close()

    def checkbox_handler(self, state):
        if self.ui.passwod_checkbox.isChecked():
            self.ui.password_line_confirm.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ui.password_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.password_line_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.password_line.setEchoMode(QtWidgets.QLineEdit.Password)

    def create_button_clicked(self):
        l = self.ui.login_line.text()
        p = self.ui.password_line.text()
        pp = self.ui.password_line_confirm.text()
        if ((l.strip() == '') or (p.strip() == '') or (pp.strip() == '')):
            message = "Необходимо заполнить каждое поле"
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Пустое поле")
            error_message.showMessage(message)
            if len(l) != 0 and (l.strip() == ''):
                self.ui.login_line.clear()
            if len(p) != 0 and (p.strip() == ''):
                self.ui.password_line.clear()
            self.ui.password_line_confirm.clear()
        elif " " in l:
            message = "Недопустимый символ в поле логина - пробел. Проверьте правильность введенных данных."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Ошибка ввода")
            error_message.setModal(True)
            error_message.showMessage(message)
            self.ui.login_line.clear()
            self.ui.password_line_confirm.clear()
            self.ui.password_line.clear()
        elif " " in p:
            message = "Недопустимый символ в поле пароля - пробел. Проверьте правильность введенных данных."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка ввода")
            error_message.showMessage(message)
            self.ui.password_line_confirm.clear()
            self.ui.password_line.clear()
        elif len(l) < 2:
            message = "Слишком короткий логин, необходимо минимум 2 символа"
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Короткий логин")
            error_message.showMessage(message)
            self.ui.password_line.clear()
            self.ui.password_line_confirm.clear()
        elif (p != pp):
            message = "Введенные пароли не совпадают. Проверьте правильность введенных данных."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка ввода")
            error_message.showMessage(message)
            self.ui.password_line_confirm.clear()
            self.ui.password_line.clear()
        else:
            self.db = sql.Sql()
            status, id, login = self.db.add_user(l, p)
            if (status is False):
                message = "Введенный логин занят. Повторите ввод."
                error_message = QtWidgets.QErrorMessage(self)
                error_message.setModal(True)
                error_message.setWindowTitle("Ошибка ввода")
                error_message.showMessage(message)
                self.ui.login_line.clear()
                self.ui.password_line.clear()
                self.ui.password_line_confirm.clear()
                self.db.cnxn.close()
            else:
                message = 'Аккаунт успешно создан!'
                properties.current_userID = id
                properties.current_login = login
                reply = QtWidgets.QMessageBox.question(self, 'Успех', message,
                                                        QtWidgets.QMessageBox.Ok)
                if reply == QtWidgets.QMessageBox.Ok:
                    self.main = start_menu.StartMenu()
                    self.main.show()
                    self.db.cnxn.close()
                    self.close()


