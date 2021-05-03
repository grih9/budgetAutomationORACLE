from PyQt5 import QtWidgets


from start_menu_window import Ui_MainWindow as start_window
import sql
import properties
import menu
import register_menu


class StartMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = start_window()
        self.ui.setupUi(self)
        self.setWindowTitle("Добро пожаловать!")
        self.ui.enter_button.clicked.connect(self.enter_button_clicked)
        self.ui.register_button.clicked.connect(self.register_button_clicked)

    def enter_button_clicked(self):
        l = self.ui.login_line.text()
        p = self.ui.password_line.text()
        if (l.strip() == ''):
            message = "Поле логина пустое! Введите логин!"
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка входа")
            error_message.showMessage(message)
            if len(l) != 0:
                self.ui.login_line.clear()
                self.ui.password_line.clear()
        elif (p.strip() == ''):
            message = "Поле пароля пустое! Введите пароль!"
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка входа")
            error_message.showMessage(message)
            if len(p) != 0:
                self.ui.password_line.clear()
        elif (l.find(' ') != -1):
            message = "Недопустимый символ в поле логина. Проверьте правильность данных и повторите вход."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка входа")
            error_message.showMessage(message)
            self.ui.login_line.clear()
            self.ui.password_line.clear()
        elif (p.find(' ') != -1):
            message = "Данного пользователя не существует или введен неверный пароль! " \
                      "Проверьте правильность данных и повторите вход."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка входа")
            error_message.showMessage(message)
            self.ui.password_line.clear()
        else:
            self.db = sql.Sql()
            status, id, login = self.db.check_password(l, p)
            self.db.cnxn.close()
            if (status == False):
                message = "Данного пользователя не существует или введен неверный пароль! Проверьте правильность данных и повторите вход."
                error_message = QtWidgets.QErrorMessage(self)
                error_message.setModal(True)
                error_message.setWindowTitle("Ошибка входа")
                error_message.showMessage(message)
                self.ui.password_line.clear()
            else:
                properties.current_userID = id
                properties.current_login = login
                self.menu = menu.Menu()
                self.menu.show()
                self.close()

    def register_button_clicked(self):
        self.reg = register_menu.RegisterMenu()
        self.reg.show()
        self.close()
