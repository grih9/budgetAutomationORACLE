import sql
import re
import start_menu
import properties
import matplotlib.pyplot as plt
from datetime import datetime
from menu_window import Ui_MainWindow as menu_window
from PyQt5 import QtWidgets, QtCore

month_mapping = {"01": "Январь",
                 "02": "Февраль",
                 "03": "Март",
                 "04": "Апрель",
                 "05": "Май",
                 "06": "Июнь",
                 "07": "Июль",
                 "08": "Август",
                 "09": "Сентябрь",
                 "10": "Октябрь",
                 "11": "Ноябрь",
                 "12": "Декабрь",
                 "Январь": "01",
                 "Февраль": "02",
                 "Март": "03",
                 "Апрель": "04",
                 "Май": "05",
                 "Июнь": "06",
                 "Июль": "07",
                 "Август": "08",
                 "Сентябрь": "09",
                 "Октябрь": "10",
                 "Ноябрь": "11",
                 "Декабрь": "12"
                 }

class Menu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = menu_window()
        self.ui.setupUi(self)
        self.setWindowTitle("Меню")
        self.ui.exit_button.clicked.connect(self.exit_button_clicked)
        self.ui.tabWidget.currentChanged.connect(self.tab_changed_handler)
        self.ui.radio_dates.clicked.connect(self.dates_radio_clicked)
        self.ui.radio_monthes.clicked.connect(self.monthes_radio_clicked)
        self.ui.from_line.dateChanged.connect(self.from_date_changed)
        self.ui.to_line.dateChanged.connect(self.to_date_changed)
        self.ui.left_arrow.clicked.connect(self.left_arrow_clicked)
        self.ui.right_arrow.clicked.connect(self.right_arrow_clicked)
        self.ui.monthes_combo.currentIndexChanged.connect(self.monthes_combo_handler)
        self.ui.articles_combo.currentIndexChanged.connect(self.articles_combo_handler)
        self.ui.article_oper_add_combo.currentIndexChanged.connect(self.article_oper_add_combo_handler)
        self.ui.oper_edit_combo.currentIndexChanged.connect(self.oper_edit_combo_handler)
        self.ui.add_operation_button.clicked.connect(self.oper_add_button_clicked)
        self.ui.delete_oper_button.clicked.connect(self.delete_oper_button_clicked)
        self.ui.edit_oper_button.clicked.connect(self.edit_oper_button_clicked)
        self.ui.reset_time.clicked.connect(self.reset_time)
        self.ui.reset_edit.clicked.connect(self.reset_edit)
        self.ui.reset_search.clicked.connect(self.reset_search)
        self.ui.articles_combo_edit.currentIndexChanged.connect(self.articles_combo_edit_handler)
        self.ui.add_article_line.textChanged.connect(self.add_article_line_handler)
        self.ui.add_article_button.clicked.connect(self.add_article_button_clicked)
        self.ui.delete_article_button.clicked.connect(self.delete_article_button_clicked)
        self.ui.edit_article_button.clicked.connect(self.edit_article_button_clicked)
        self.ui.reset_article.clicked.connect(self.reset_article_clicked)
        self.ui.delete_balance_combo.currentIndexChanged.connect(self.delete_balance_combo_handler)
        self.ui.create_balance_combo.currentIndexChanged.connect(self.create_balance_combo_handler)
        self.ui.delete_balance_button.clicked.connect(self.delete_balance_button_clicked)
        self.ui.create_balance_button.clicked.connect(self.create_balance_button_clicked)
        self.ui.analyze_button.clicked.connect(self.analyze_button_clicked)
        self.db = sql.Sql()
        self.ui.entry_message.setText(f"Привет, {properties.current_login}!")
        header = self.ui.operations_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.operations_table.verticalHeader().hide()
        header = self.ui.articles_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ui.articles_table.verticalHeader().hide()
        header = self.ui.balances_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.balances_table.verticalHeader().hide()
        self.ui.article_oper_add_combo.clear()
        self.ui.oper_edit_combo.clear()
        self.ui.oper_edit_combo.addItem("")
        self.ui.article_oper_add_combo.addItem("")
        self.ui.monthes_combo.clear()
        self.ui.from_line.setEnabled(False)
        self.ui.to_line.setEnabled(False)
        self.disable_button(self.ui.add_operation_button)
        self.disable_button(self.ui.delete_oper_button)
        self.disable_button(self.ui.edit_oper_button)
        self.disable_button(self.ui.right_arrow)
        date = datetime.now()
        self.ui.from_line.setDate(date)
        self.ui.from_line.setMaximumDate(date)
        self.ui.date_add_combo.setDate(date)
        self.ui.date_add_combo.setMaximumDate(date)
        self.ui.to_line.setMinimumDate(date)
        self.ui.to_line.setDate(date)
        self.ui.no_items_label.hide()
        self.ui.operations_table.show()
        self.ui.operations_table.setRowCount(0)
        self.db.cursor.execute("SELECT op.create_date FROM operations op order by op.create_date")
        row = self.db.cursor.fetchone()
        set_months = set()
        while (row is not None):
            year = str(row[0])[:4]
            month = month_mapping[str(str(row[0])[5:7])]
            month_string = f"{month} {year}"
            if month_string not in set_months:
                set_months.add(month_string)
                self.ui.monthes_combo.addItem(month_string)
            row = self.db.cursor.fetchone()
        size = self.ui.monthes_combo.count()
        self.ui.articles_combo.clear()
        self.ui.articles_combo.addItem("Все статьи")
        if size == 1:
            self.disable_button(self.ui.left_arrow)
        if size > 0:
            self.ui.monthes_combo.setCurrentIndex(int(size) - 1)
        else:
            self.ui.no_items_label.show()
            self.ui.operations_table.hide()
        query = "SELECT a.name from articles a order by name"
        self.db.cursor.execute(query)
        row = self.db.cursor.fetchone()
        while (row is not None):
            self.ui.article_oper_add_combo.addItem(str(row[0]))
            self.ui.articles_combo.addItem(str(row[0]))
            row = self.db.cursor.fetchone()

    def exit_button_clicked(self):
        message = 'Вы уверены, что хотите выйти?'
        reply = QtWidgets.QMessageBox.question(self, 'Выход из базы данных', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            properties.current_userID = 0
            properties.current_login = ""
            self.menu = start_menu.StartMenu()
            self.menu.show()
            self.close()


    def disable_button(self, button):
        button.setEnabled(False)
        button.setStyleSheet("background-color: rgb(13, 243, 255)")

    def reset_time(self):
        self.ui.date_add_combo.setDate(datetime.now())
        self.ui.oper_edit_combo.setCurrentIndex(0)

    def reset_search(self):
        self.ui.radio_monthes.setChecked(True)
        self.to_date_changed(datetime.now())
        self.from_date_changed(datetime.now())
        self.ui.monthes_combo.setCurrentIndex(self.ui.monthes_combo.count() - 1)
        self.ui.articles_combo.setCurrentIndex(0)
        self.monthes_radio_clicked()

    def reset_edit(self):
        self.ui.debit_spin.setValue(0.0)
        self.ui.credit_spin.setValue(0.0)
        self.ui.article_oper_add_combo.setCurrentIndex(0)
        self.reset_time()
        self.ui.oper_edit_combo.setCurrentIndex(0)

    def reset_article_clicked(self):
        self.ui.add_article_line.setText("")
        self.ui.articles_combo_edit.setCurrentIndex(0)

    def enable_button(self, button):
        button.setEnabled(True)
        button.setStyleSheet("background-color: rgb(13, 134, 255)")

    def dates_radio_clicked(self):
        self.ui.from_line.setEnabled(True)
        self.ui.to_line.setEnabled(True)
        self.ui.monthes_combo.setEnabled(False)
        self.disable_button(self.ui.right_arrow)
        self.disable_button(self.ui.left_arrow)
        self.ui.operations_table.setRowCount(0)
        db_from = self.ui.from_line.date()
        db_to = self.ui.to_line.date()
        db_from = f"{db_from.year()}-{db_from.month()}-{db_from.day()}"
        db_to = f"{db_to.year()}-{db_to.month()}-{db_to.day()}"
        db = sql.Sql()
        article = str(self.ui.articles_combo.currentText())
        if article == "Все статьи":
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
        else:
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article}' order by op.create_date"
        db.cursor.execute(query)
        self.ui.oper_edit_combo.clear()
        self.ui.oper_edit_combo.addItem("")
        row = db.cursor.fetchone()
        self.oper_list = list()
        if (row is not None):
            i = 0
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            while (row is not None):
                self.oper_list.append(str(row[0]))
                text_combo = f"{i + 1}. {str(row[1])[:10]}. {str(row[2])} +{str(row[3])} -{str(row[4])}"
                self.ui.oper_edit_combo.addItem(text_combo)
                self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                item = QtWidgets.QTableWidgetItem()
                self.ui.operations_table.setVerticalHeaderItem(i, item)
                self.ui.operations_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                self.ui.operations_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                for j in range(1, 6):
                    elem = str(row[j])
                    if j == 1:
                        elem = elem[:10]
                    elif j == 5 and elem == "None":
                        elem = "-"
                    self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                    self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                row = db.cursor.fetchone()
                i += 1
        else:
            self.ui.no_items_label.show()
            self.ui.operations_table.hide()

    def monthes_radio_clicked(self):
        self.ui.from_line.setEnabled(False)
        self.ui.to_line.setEnabled(False)
        self.ui.monthes_combo.setEnabled(True)
        c = self.ui.monthes_combo.count()
        index = self.ui.monthes_combo.currentIndex()
        if c == 1:
            self.disable_button(self.ui.right_arrow)
            self.disable_button(self.ui.left_arrow)
        elif index == 0:
            self.enable_button(self.ui.right_arrow)
            self.disable_button(self.ui.left_arrow)
        elif index == c - 1:
            self.disable_button(self.ui.right_arrow)
            self.enable_button(self.ui.left_arrow)
        else:
            self.enable_button(self.ui.right_arrow)
            self.enable_button(self.ui.left_arrow)
        text = str(self.ui.monthes_combo.currentText())
        year = text[-4:]
        month = month_mapping[text[:-5]]
        db_from = f"{year}-{month}-01"
        if month != "12":
            month = int(month) + 1
            month = f"0{month}" if month < 10 else f"{month}"
            db_to = f"{year}-{month}-01"
        else:
            db_to = f"{str(int(year) + 1)}-01-01"
        db = sql.Sql()
        article = str(self.ui.articles_combo.currentText())
        if article == "Все статьи":
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
        else:
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article}' order by op.create_date"
        db.cursor.execute(query)
        row = db.cursor.fetchone()
        self.oper_list = list()
        self.ui.operations_table.setRowCount(0)
        self.ui.oper_edit_combo.clear()
        self.ui.oper_edit_combo.addItem("")
        if (row is not None):
            i = 0
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            while (row is not None):
                self.oper_list.append(str(row[0]))
                text_combo = f"{i + 1}. {str(row[1])[:10]}. {str(row[2])} +{str(row[3])} -{str(row[4])}"
                self.ui.oper_edit_combo.addItem(text_combo)
                self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                item = QtWidgets.QTableWidgetItem()
                self.ui.operations_table.setVerticalHeaderItem(i, item)
                self.ui.operations_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                self.ui.operations_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                for j in range(1, 6):
                    elem = str(row[j])
                    if j == 1:
                        elem = elem[:10]
                    elif j == 5 and elem == "None":
                        elem = "-"
                    self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                    self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                row = db.cursor.fetchone()
                i += 1
        else:
            self.ui.no_items_label.show()
            self.ui.operations_table.hide()

    def left_arrow_clicked(self):
        self.arrow_clicked(offset=-1)

    def right_arrow_clicked(self):
        self.arrow_clicked(offset=1)

    def arrow_clicked(self, offset):
        c = self.ui.monthes_combo.count()
        index = self.ui.monthes_combo.currentIndex()
        self.ui.monthes_combo.setCurrentIndex(index + offset)
        index = self.ui.monthes_combo.currentIndex()
        if c == 1:
            self.disable_button(self.ui.left_arrow)
            self.disable_button(self.ui.right_arrow)
        elif index == 0:
            self.enable_button(self.ui.right_arrow)
            self.disable_button(self.ui.left_arrow)
        elif index == c - 1:
            self.disable_button(self.ui.right_arrow)
            self.enable_button(self.ui.left_arrow)
        else:
            self.enable_button(self.ui.right_arrow)
            self.enable_button(self.ui.left_arrow)
        text = str(self.ui.monthes_combo.currentText())
        year = text[-4:]
        month = month_mapping[text[:-5]]
        db_from = f"{year}-{month}-01"
        if month != "12":
            month = int(month) + 1
            month = f"0{month}" if month < 10 else f"{month}"
            db_to = f"{year}-{month}-01"
        else:
            db_to = f"{str(int(year) + 1)}-01-01"
        db = sql.Sql()
        article = str(self.ui.articles_combo.currentText())
        if article == "Все статьи":
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
        else:
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article}' order by op.create_date"
        db.cursor.execute(query)
        row = db.cursor.fetchone()
        self.oper_list = list()
        self.ui.operations_table.setRowCount(0)
        self.ui.oper_edit_combo.clear()
        self.ui.oper_edit_combo.addItem("")
        if (row is not None):
            i = 0
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            while (row is not None):
                self.oper_list.append(str(row[0]))
                text_combo = f"{i + 1}. {str(row[1])[:10]}. {str(row[2])} +{str(row[3])} -{str(row[4])}"
                self.ui.oper_edit_combo.addItem(text_combo)
                self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                item = QtWidgets.QTableWidgetItem()
                self.ui.operations_table.setVerticalHeaderItem(i, item)
                self.ui.operations_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                self.ui.operations_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                for j in range(1, 6):
                    elem = str(row[j])
                    if j == 1:
                        elem = elem[:10]
                    elif j == 5 and elem == "None":
                        elem = "-"
                    self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                    self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                row = db.cursor.fetchone()
                i += 1
        else:
            self.ui.no_items_label.show()
            self.ui.operations_table.hide()

    def from_date_changed(self, date):
        self.ui.from_line.setDate(date)
        self.from_to_date_changed("from", date)

    def to_date_changed(self, date):
        self.ui.to_line.setDate(date)
        self.from_to_date_changed("to", date)

    def from_to_date_changed(self, type, date):
        if type == "from":
            self.ui.to_line.setMinimumDate(self.ui.from_line.date())
        elif type == "to":
            self.ui.from_line.setMaximumDate(self.ui.to_line.date())
        else:
            raise Exception()
        self.ui.operations_table.setRowCount(0)
        db_from = self.ui.from_line.date()
        db_to = self.ui.to_line.date()
        db_from = f"{db_from.year()}-{db_from.month()}-{db_from.day()}"
        db_to = f"{db_to.year()}-{db_to.month()}-{db_to.day()}"
        db = sql.Sql()
        article = str(self.ui.articles_combo.currentText())
        if article == "Все статьи":
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
        else:
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article}' order by op.create_date"
        db.cursor.execute(query)
        self.ui.oper_edit_combo.clear()
        self.ui.oper_edit_combo.addItem("")
        row = db.cursor.fetchone()
        self.oper_list = list()
        if (row is not None):
            i = 0
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            while (row is not None):
                self.oper_list.append(str(row[0]))
                text_combo = f"{i + 1}. {str(row[1])[:10]}. {str(row[2])} +{str(row[3])} -{str(row[4])}"
                self.ui.oper_edit_combo.addItem(text_combo)
                self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                item = QtWidgets.QTableWidgetItem()
                self.ui.operations_table.setVerticalHeaderItem(i, item)
                self.ui.operations_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                self.ui.operations_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                for j in range(1, 6):
                    elem = str(row[j])
                    if j == 1:
                        elem = elem[:10]
                    elif j == 5 and elem == "None":
                        elem = "-"
                    self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                    self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                row = db.cursor.fetchone()
                i += 1
        else:
            self.ui.no_items_label.show()
            self.ui.operations_table.hide()

    def monthes_combo_handler(self, index):
        c = self.ui.monthes_combo.count()
        if index == -1 or c == 0:
            return
        if c == 1:
            self.disable_button(self.ui.left_arrow)
            self.disable_button(self.ui.right_arrow)
        elif index == 0:
            self.enable_button(self.ui.right_arrow)
            self.disable_button(self.ui.left_arrow)
        elif index == c - 1:
            self.disable_button(self.ui.right_arrow)
            self.enable_button(self.ui.left_arrow)
        else:
            self.enable_button(self.ui.right_arrow)
            self.enable_button(self.ui.left_arrow)
        text = str(self.ui.monthes_combo.currentText())
        year = text[-4:]
        month = month_mapping[text[:-5]]
        db_from = f"{year}-{month}-01"
        if month != "12":
            month = int(month) + 1
            month = f"0{month}" if month < 10 else f"{month}"
            db_to = f"{year}-{month}-01"
        else:
            db_to = f"{str(int(year) + 1)}-01-01"

        article = str(self.ui.articles_combo.currentText())
        if article == "Все статьи":
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
        else:
            query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article}' order by op.create_date"

        db = sql.Sql()
        db.cursor.execute(query)
        row = db.cursor.fetchone()
        self.oper_list = list()
        self.ui.operations_table.setRowCount(0)
        self.ui.oper_edit_combo.clear()
        self.ui.oper_edit_combo.addItem("")
        if (row is not None):
            i = 0
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            while (row is not None):
                self.oper_list.append(str(row[0]))
                text_combo = f"{i + 1}. {str(row[1])[:10]}. {str(row[2])} +{str(row[3])} -{str(row[4])}"
                self.ui.oper_edit_combo.addItem(text_combo)
                self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                item = QtWidgets.QTableWidgetItem()
                self.ui.operations_table.setVerticalHeaderItem(i, item)
                self.ui.operations_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                self.ui.operations_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                for j in range(1, 6):
                    elem = str(row[j])
                    if j == 1:
                        elem = elem[:10]
                    elif j == 5 and elem == "None":
                        elem = "-"
                    self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                    self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                row = db.cursor.fetchone()
                i += 1
        else:
            self.ui.no_items_label.show()
            self.ui.operations_table.hide()

    def articles_combo_handler(self, index):
        if self.ui.monthes_combo.count() == 0:
            return
        if index == -1:
            return
        if self.ui.radio_monthes.isChecked():
            text = str(self.ui.monthes_combo.currentText())
            year = text[-4:]
            month = month_mapping[text[:-5]]
            print(month)
            db_from = f"{year}-{month}-01"
            if month != "12":
                month = int(month) + 1
                month = f"0{month}" if month < 10 else f"{month}"
                db_to = f"{year}-{month}-01"
            else:
                db_to = f"{str(int(year) + 1)}-01-01"
        else:
            db_from = self.ui.from_line.date()
            db_to = self.ui.to_line.date()
            db_from = f"{db_from.year()}-{db_from.month()}-{db_from.day()}"
            db_to = f"{db_to.year()}-{db_to.month()}-{db_to.day()}"
        article = str(self.ui.articles_combo.currentText())
        if self.ui.radio_monthes.isChecked():
            if article == "Все статьи":
                query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                        f"join articles a on op.article_id=a.id " \
                        f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                        f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
            else:
                query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                        f"join articles a on op.article_id=a.id " \
                        f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                        f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article}' order by op.create_date"
        else:
            if article == "Все статьи":
                query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                        f"join articles a on op.article_id=a.id " \
                        f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                        f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
            else:
                query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                        f"join articles a on op.article_id=a.id " \
                        f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                        f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article}' order by op.create_date"
        db = sql.Sql()
        db.cursor.execute(query)
        row = db.cursor.fetchone()
        self.oper_list = list()
        self.ui.operations_table.setRowCount(0)
        self.ui.oper_edit_combo.clear()
        self.ui.oper_edit_combo.addItem("")
        if (row is not None):
            i = 0
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            while (row is not None):
                self.oper_list.append(str(row[0]))
                text_combo = f"{i + 1}. {str(row[1])[:10]}. {str(row[2])} +{str(row[3])} -{str(row[4])}"
                self.ui.oper_edit_combo.addItem(text_combo)
                self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                item = QtWidgets.QTableWidgetItem()
                self.ui.operations_table.setVerticalHeaderItem(i, item)
                self.ui.operations_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                self.ui.operations_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                for j in range(1, 6):
                    elem = str(row[j])
                    print(elem)
                    if j == 1:
                        elem = elem[:10]
                    elif j == 5 and elem == "None":
                        elem = "-"
                    self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                    self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                row = db.cursor.fetchone()
                i += 1
        else:
            self.ui.no_items_label.show()
            self.ui.operations_table.hide()

    def article_oper_add_combo_handler(self, index):
        if self.ui.oper_edit_combo.currentIndex() == 0 and index != 0:
            self.enable_button(self.ui.add_operation_button)
            self.disable_button(self.ui.edit_oper_button)
            self.disable_button(self.ui.delete_oper_button)
            self.ui.date_add_combo.setEnabled(True)
        elif self.ui.oper_edit_combo.currentIndex() != 0 and index != 0:
            self.disable_button(self.ui.add_operation_button)
            self.enable_button(self.ui.edit_oper_button)
            self.enable_button(self.ui.delete_oper_button)
            self.ui.date_add_combo.setEnabled(False)
        elif self.ui.oper_edit_combo.currentIndex() != 0 and index == 0:
            self.disable_button(self.ui.add_operation_button)
            self.disable_button(self.ui.edit_oper_button)
            self.enable_button(self.ui.delete_oper_button)
            self.ui.date_add_combo.setEnabled(False)
        else:
            self.disable_button(self.ui.add_operation_button)
            self.disable_button(self.ui.edit_oper_button)
            self.disable_button(self.ui.delete_oper_button)
            self.ui.date_add_combo.setEnabled(True)

    def oper_add_button_clicked(self):
        date = self.ui.date_add_combo.date()
        credit = self.ui.credit_spin.value()
        debit = self.ui.debit_spin.value()
        article = self.ui.article_oper_add_combo.currentText()
        if int(credit) == 0 and int(debit) == 0:
            message = "Необходимо ввести приход или расход."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка добавления")
            error_message.showMessage(message)
        else:
            db = sql.Sql()
            db.cursor.execute("SELECT b.create_date FROM balance b order by b.create_date")
            row = db.cursor.fetchone()
            set_months = set()
            while (row is not None):
                year = str(row[0])[:4]
                month = month_mapping[str(str(row[0])[5:7])]
                month_string = f"{month} {year}"
                if month_string not in set_months:
                    set_months.add(month_string)
                row = db.cursor.fetchone()
            month = date.month()
            year = date.year()
            day = date.day()
            date = f"{year}-{month}-{day}"
            if month != "12":
                month = int(month) + 1
                month = f"0{month}" if month < 10 else f"{month}"
                d = f"{month_mapping[str(month)]} {year}"
            else:
                d = f"{month_mapping['01']} {str(int(year) + 1)}"
            print(d)
            print(set_months)
            if d in set_months:
                message = f"Данный период времени уже закрыт балансом от 1 {d}. " \
                          f"Для добавления, изменения и удаления операций необходимо расформировать баланс."
                error_message = QtWidgets.QErrorMessage(self)
                error_message.setModal(True)
                error_message.setWindowTitle("Ошибка добавления")
                error_message.showMessage(message)
            else:
                db.cursor.execute(f"SELECT id from articles where name='{article}'")
                row = db.cursor.fetchone()
                id = row[0]
                db.cursor.execute(f"INSERT INTO OPERATIONS (article_id, debit, credit, create_date)"
                                  f"VALUES ({id}, {debit}, {credit}, to_timestamp('{date}', 'YYYY-MM-DD'))")
                db.cnxn.commit()
                message = "Операция успешно добавлена."
                reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
                self.ui.debit_spin.setValue(0.0)
                self.ui.credit_spin.setValue(0.0)
                self.ui.article_oper_add_combo.setCurrentIndex(0)
                self.reset_time()
                self.ui.operations_table.setRowCount(0)
                name = self.ui.monthes_combo.currentText()
                self.ui.monthes_combo.clear()
                self.db.cursor.execute("SELECT op.create_date FROM operations op order by op.create_date")
                row = self.db.cursor.fetchone()
                set_months = set()
                while (row is not None):
                    year = str(row[0])[:4]
                    month = month_mapping[str(str(row[0])[5:7])]
                    month_string = f"{month} {year}"
                    if month_string not in set_months:
                        set_months.add(month_string)
                        self.ui.monthes_combo.addItem(month_string)
                    row = self.db.cursor.fetchone()
                for i in range(self.ui.monthes_combo.count()):
                    self.ui.monthes_combo.setCurrentIndex(i)
                    if self.ui.monthes_combo.currentText() == name:
                        break
                if self.ui.radio_dates.isChecked():
                    self.disable_button(self.ui.left_arrow)
                    self.disable_button(self.ui.right_arrow)
                index = self.ui.articles_combo.currentIndex()
                if index > 0:
                    self.ui.articles_combo.setCurrentIndex(index - 1)
                else:
                    self.ui.articles_combo.setCurrentIndex(index + 1)
                self.ui.articles_combo.setCurrentIndex(index)

    def delete_oper_button_clicked(self):
        message = "Вы уверены, что хотите удалить операцию?"
        reply = QtWidgets.QMessageBox.question(self, "Удаление операции", message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            index = self.ui.oper_edit_combo.currentIndex()
            id = self.oper_list[index - 1]
            db = sql.Sql()
            db.cursor.execute(
                f"SELECT op.balance_id, b.create_date FROM operations op join balance b on b.id=op.balance_id where op.id={id}")
            row = db.cursor.fetchone()
            if row is not None:
                b_id = row[0]
                date = row[1]
            else:
                b_id = None
                date = None
            if b_id is not None:
                self.ui.oper_edit_combo.setCurrentIndex(0)
                self.reset_time()
                self.ui.debit_spin.setValue(0)
                self.ui.credit_spin.setValue(0)
                self.ui.article_oper_add_combo.setCurrentIndex(0)
                message = f"Данная операция уже включена в баланс от 1 {month_mapping[str(date)[5:7]]} {str(date)[:4]}. " \
                          f"Для удаления операции необходимо расформировать баланс."
                error_message = QtWidgets.QErrorMessage(self)
                error_message.setModal(True)
                error_message.setWindowTitle("Ошибка удаления")
                error_message.showMessage(message)
            else:
                db = sql.Sql()
                db.cursor.execute(f"DELETE operations where id={id}")
                db.cnxn.commit()
                message = "Операция успешно удалена."
                reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
                self.ui.debit_spin.setValue(0.0)
                self.ui.credit_spin.setValue(0.0)
                self.ui.article_oper_add_combo.setCurrentIndex(0)
                self.reset_time()
                self.ui.operations_table.setRowCount(0)
                name = self.ui.monthes_combo.currentText()
                self.ui.monthes_combo.clear()
                self.db.cursor.execute("SELECT op.create_date FROM operations op order by op.create_date")
                row = self.db.cursor.fetchone()
                set_months = set()
                while (row is not None):
                    year = str(row[0])[:4]
                    month = month_mapping[str(str(row[0])[5:7])]
                    month_string = f"{month} {year}"
                    if month_string not in set_months:
                        set_months.add(month_string)
                        self.ui.monthes_combo.addItem(month_string)
                    row = self.db.cursor.fetchone()
                for i in range(self.ui.monthes_combo.count()):
                    self.ui.monthes_combo.setCurrentIndex(i)
                    if self.ui.monthes_combo.currentText() == name:
                        break
                if self.ui.radio_dates.isChecked():
                    self.disable_button(self.ui.left_arrow)
                    self.disable_button(self.ui.right_arrow)
                index = self.ui.articles_combo.currentIndex()
                if index > 0:
                    self.ui.articles_combo.setCurrentIndex(index - 1)
                else:
                    self.ui.articles_combo.setCurrentIndex(index + 1)
                self.ui.articles_combo.setCurrentIndex(index)

    def edit_oper_button_clicked(self):
        message = "Вы уверены, что хотите изменить операцию?"
        reply = QtWidgets.QMessageBox.question(self, "Изменение операции", message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            index = self.ui.oper_edit_combo.currentIndex()
            id = self.oper_list[index - 1]
            db = sql.Sql()
            db.cursor.execute(
                f"SELECT op.balance_id, b.create_date FROM operations op join balance b on b.id=op.balance_id where op.id={id}")
            row = db.cursor.fetchone()
            if row is not None:
                b_id = row[0]
                date = row[1]
            else:
                b_id = None
                date = None
            if b_id is not None:
                self.ui.oper_edit_combo.setCurrentIndex(0)
                self.reset_time()
                self.ui.debit_spin.setValue(0)
                self.ui.credit_spin.setValue(0)
                self.ui.article_oper_add_combo.setCurrentIndex(0)
                message = f"Данная операция уже включена в баланс от 1 {month_mapping[str(date)[5:7]]} {str(date)[:4]}. " \
                          f"Для изменения операции необходимо расформировать баланс."
                error_message = QtWidgets.QErrorMessage(self)
                error_message.setModal(True)
                error_message.setWindowTitle("Ошибка изменения")
                error_message.showMessage(message)
            else:
                credit = self.ui.credit_spin.value()
                debit = self.ui.debit_spin.value()
                article = self.ui.article_oper_add_combo.currentText()
                if int(credit) == 0 and int(debit) == 0:
                    message = "Необходимо ввести приход или расход."
                    error_message = QtWidgets.QErrorMessage(self)
                    error_message.setModal(True)
                    error_message.setWindowTitle("Ошибка изменения")
                    error_message.showMessage(message)
                else:
                    db = sql.Sql()
                    db.cursor.execute(f"SELECT id from articles where name='{article}'")
                    row = db.cursor.fetchone()
                    article_id = row[0]
                    db.cursor.execute(f"UPDATE OPERATIONS set article_id={article_id} where id={id}")
                    db.cursor.execute(f"UPDATE OPERATIONS set debit={debit} where id={id}")
                    db.cursor.execute(f"UPDATE OPERATIONS set credit={credit} where id={id}")
                    db.cnxn.commit()
                    message = "Операция успешно изменена."
                    reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
                    self.ui.debit_spin.setValue(0.0)
                    self.ui.credit_spin.setValue(0.0)
                    self.ui.article_oper_add_combo.setCurrentIndex(0)
                    self.reset_time()
                    index = self.ui.articles_combo.currentIndex()
                    if index > 0:
                        self.ui.articles_combo.setCurrentIndex(index - 1)
                    else:
                        self.ui.articles_combo.setCurrentIndex(index + 1)
                    self.ui.articles_combo.setCurrentIndex(index)

    def oper_edit_combo_handler(self, index):
        if index == -1:
            return
        if index == 0 and self.ui.article_oper_add_combo.currentIndex() != 0:
            self.enable_button(self.ui.add_operation_button)
            self.disable_button(self.ui.delete_oper_button)
            self.disable_button(self.ui.edit_oper_button)
            self.ui.date_add_combo.setEnabled(True)
        elif index == 0 and self.ui.article_oper_add_combo.currentIndex() == 0:
            self.disable_button(self.ui.add_operation_button)
            self.disable_button(self.ui.delete_oper_button)
            self.disable_button(self.ui.edit_oper_button)
            self.ui.date_add_combo.setEnabled(True)
        else:
            self.disable_button(self.ui.add_operation_button)
            self.enable_button(self.ui.delete_oper_button)
            self.enable_button(self.ui.edit_oper_button)
            self.ui.date_add_combo.setEnabled(False)
            id = self.oper_list[index - 1]
            db = sql.Sql()
            query = f"SELECT op.create_date, a.name, op.credit, op.debit FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.id={id}"
            db.cursor.execute(query)
            row = db.cursor.fetchone()
            date = row[0]
            name = row[1]
            credit = row[2]
            debit = row[3]
            print(date, name, credit, debit)
            self.ui.date_add_combo.setDate(date)
            self.ui.credit_spin.setValue(float(credit))
            self.ui.debit_spin.setValue(float(debit))
            for i in range(1, self.ui.article_oper_add_combo.count()):
                self.ui.article_oper_add_combo.setCurrentIndex(i)
                if self.ui.article_oper_add_combo.currentText() == name:
                    break

    def articles_combo_edit_handler(self, index):
        if index == -1:
            return
        if index == 0:
            self.disable_button(self.ui.delete_article_button)
            self.disable_button(self.ui.edit_article_button)
            self.disable_button(self.ui.add_article_button)
            self.ui.add_article_line.setText("")
        else:
            text = str(self.ui.articles_combo_edit.currentText())
            index = text.find(" ")
            self.ui.add_article_line.setText(text[index + 1:])
            self.enable_button(self.ui.delete_article_button)
            self.enable_button(self.ui.edit_article_button)
            self.disable_button(self.ui.add_article_button)

    def add_article_line_handler(self):
        text = str(self.ui.add_article_line.text())
        if len(text) == 0 or len(text.lstrip(" ")) == 0:
            if self.ui.articles_combo_edit.currentIndex() != 0:
                self.enable_button(self.ui.delete_article_button)
            else:
                self.disable_button(self.ui.delete_article_button)
            self.disable_button(self.ui.edit_article_button)
            self.disable_button(self.ui.add_article_button)
        elif self.ui.articles_combo_edit.currentIndex() != 0:
            self.enable_button(self.ui.delete_article_button)
            self.enable_button(self.ui.edit_article_button)
            self.disable_button(self.ui.add_article_button)
        else:
            self.disable_button(self.ui.delete_article_button)
            self.disable_button(self.ui.edit_article_button)
            self.enable_button(self.ui.add_article_button)

    def add_article_button_clicked(self):
        db = sql.Sql()
        article = str(self.ui.add_article_line.text()).strip()
        if re.search(r"[a-zA-Zа-яА-Я]", article) is None or re.search(r"[a-zA-Zа-яА-Я0-9]", article[0]) is None:
            message = "Название статьи должно содержать хотя бы одну букву и начинаться с буквы или цифры."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка добавления")
            error_message.showMessage(message)
            return
        try:
            db.cursor.execute(f"INSERT into articles (name) values ('{article}')")
            db.cnxn.commit()
            message = "Статья успешно добавлена."
            reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
            self.ui.add_article_line.setText("")
            self.ui.articles_table.setRowCount(0)
            db.cursor.execute("SELECT id, name from articles order by name")
            self.ui.articles_combo_edit.clear()
            self.ui.articles_combo_edit.addItem("")
            row = db.cursor.fetchone()
            self.articles_list = list()
            if (row is not None):
                i = 0
                self.ui.no_articles_label.hide()
                self.ui.articles_table.show()
                while (row is not None):
                    self.articles_list.append(str(row[0]))
                    text_combo = f"{i + 1}. {str(row[1])}"
                    self.ui.articles_combo_edit.addItem(text_combo)
                    self.ui.articles_table.setRowCount(self.ui.articles_table.rowCount() + 1)
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.articles_table.setVerticalHeaderItem(i, item)
                    self.ui.articles_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                    self.ui.articles_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.ui.articles_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                    self.ui.articles_table.item(i, 1).setFlags(QtCore.Qt.NoItemFlags)
                    self.ui.articles_table.item(i, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                    row = db.cursor.fetchone()
                    i += 1
            else:
                self.ui.no_articles_label.show()
                self.ui.articles_table.hide()
        except:
            message = "Статья с таким названием уже есть в базе данных. Введите другое название."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка добавления")
            error_message.showMessage(message)

    def delete_article_button_clicked(self):
        db = sql.Sql()
        id = self.articles_list[self.ui.articles_combo_edit.currentIndex() - 1]
        db.cursor.execute(f"SELECT id, create_date from operations where article_id={id} order by create_date")
        row = db.cursor.fetchone()
        if row is not None:
            message = f"Нельзя удалить используемую статью. Данная статья используется в операции от {str(row[1])[:10]}. " \
                      f"Измените статью, используемую в операции, или удалите операцию."
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setModal(True)
            error_message.setWindowTitle("Ошибка удаления")
            error_message.showMessage(message)
            db.cursor.execute(f"SELECT name from articles where id={id}")
            row = db.cursor.fetchone()
            name = row[0]
            self.ui.add_article_line.setText(name)
        else:
            db.cursor.execute(f"DELETE articles where id={id}")
            db.cnxn.commit()
            message = "Статья успешно удалена."
            reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
            self.ui.add_article_line.setText("")
            self.ui.articles_table.setRowCount(0)
            db.cursor.execute("SELECT id, name from articles order by name")
            self.ui.articles_combo_edit.clear()
            self.ui.articles_combo_edit.addItem("")
            row = db.cursor.fetchone()
            self.articles_list = list()
            if (row is not None):
                i = 0
                self.ui.no_articles_label.hide()
                self.ui.articles_table.show()
                while (row is not None):
                    self.articles_list.append(str(row[0]))
                    text_combo = f"{i + 1}. {str(row[1])}"
                    self.ui.articles_combo_edit.addItem(text_combo)
                    self.ui.articles_table.setRowCount(self.ui.articles_table.rowCount() + 1)
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.articles_table.setVerticalHeaderItem(i, item)
                    self.ui.articles_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                    self.ui.articles_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.ui.articles_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                    self.ui.articles_table.item(i, 1).setFlags(QtCore.Qt.NoItemFlags)
                    self.ui.articles_table.item(i, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                    row = db.cursor.fetchone()
                    i += 1
            else:
                self.ui.no_articles_label.show()
                self.ui.articles_table.hide()

    def edit_article_button_clicked(self):
        message = "Вы уверены, что хотите изменить название статьи?"
        reply = QtWidgets.QMessageBox.question(self, "Изменение статьи", message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            db = sql.Sql()
            id = self.articles_list[self.ui.articles_combo_edit.currentIndex() - 1]
            new_name = self.ui.add_article_line.text().strip()
            db.cursor.execute(f"SELECT balance_id, create_date from operations where article_id={id} and balance_id>0 order by balance_id")
            row = db.cursor.fetchone()
            if row is not None:
                message = f"Нельзя изменить используемую статью. Данная статья используется в операции от {str(row[1])[:10]}. " \
                          f"Измените статью, используемую в операции, или удалите операцию."
                error_message = QtWidgets.QErrorMessage(self)
                error_message.setModal(True)
                error_message.setWindowTitle("Ошибка изменения")
                error_message.showMessage(message)
            else:
                if re.search(r"[a-zA-Zа-яА-Я]", new_name) is None or re.search(r"[a-zA-Zа-яА-Я0-9]", new_name[0]) is None:
                    message = "Название статьи должно содержать хотя бы одну букву и начинаться с буквы или цифры."
                    error_message = QtWidgets.QErrorMessage(self)
                    error_message.setModal(True)
                    error_message.setWindowTitle("Ошибка изменения")
                    error_message.showMessage(message)
                    return
                try:
                    db.cursor.execute(f"UPDATE articles set name='{new_name}' where id={id}")
                    db.cnxn.commit()
                    message = "Статья успешно изменена."
                    reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
                    self.ui.add_article_line.setText("")
                    self.ui.articles_table.setRowCount(0)
                    db.cursor.execute("SELECT id, name from articles order by name")
                    self.ui.articles_combo_edit.clear()
                    self.ui.articles_combo_edit.addItem("")
                    row = db.cursor.fetchone()
                    self.articles_list = list()
                    if (row is not None):
                        i = 0
                        self.ui.no_articles_label.hide()
                        self.ui.articles_table.show()
                        while (row is not None):
                            self.articles_list.append(str(row[0]))
                            text_combo = f"{i + 1}. {str(row[1])}"
                            self.ui.articles_combo_edit.addItem(text_combo)
                            self.ui.articles_table.setRowCount(self.ui.articles_table.rowCount() + 1)
                            item = QtWidgets.QTableWidgetItem()
                            self.ui.articles_table.setVerticalHeaderItem(i, item)
                            self.ui.articles_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                            self.ui.articles_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                            self.ui.articles_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                            self.ui.articles_table.item(i, 1).setFlags(QtCore.Qt.NoItemFlags)
                            self.ui.articles_table.item(i, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                            row = db.cursor.fetchone()
                            i += 1
                    else:
                        self.ui.no_articles_label.show()
                        self.ui.articles_table.hide()
                except:
                    message = "Статья с таким названием уже есть в базе данных. Введите другое название."
                    error_message = QtWidgets.QErrorMessage(self)
                    error_message.setModal(True)
                    error_message.setWindowTitle("Ошибка изменения")
                    error_message.showMessage(message)

    def delete_balance_combo_handler(self, index):
        if index == -1:
            return
        if index == 0:
            self.disable_button(self.ui.delete_balance_button)
        else:
            self.enable_button(self.ui.delete_balance_button)

    def create_balance_combo_handler(self, index):
        if index == -1:
            return
        if index == 0:
            self.disable_button(self.ui.create_balance_button)
        else:
            self.enable_button(self.ui.create_balance_button)

    def delete_balance_button_clicked(self):
        balance = self.balances_list[self.ui.delete_balance_combo.currentIndex() - 1]
        db = sql.Sql()
        db.cursor.execute(f"SELECT create_date from balance where id={balance}")
        item = str(db.cursor.fetchone()[0])
        message = f"Вы уверены, что хотите расформировать баланс от {item[:10]}? Все операции, принадлежащие данному балансу, " \
                  f"станут доступны для изменения и удаления. Если нормальный срок формирования баланса (1 число следующего месяца) " \
                  f"для данного периода времени уже наступил, то баланс будет автоматически сформирован заново при следующем " \
                  f"входе в базу данных или же Вы сами сможете сформировать его заново."
        reply = QtWidgets.QMessageBox.question(self, "Расформирование баланса", message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            db.cursor.execute(f"UPDATE operations set balance_id=NULL where balance_id={balance}")
            db.cursor.execute(f"DELETE from balance where id={balance}")
            db.cnxn.commit()
            message = "Баланс расформирован."
            reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.tabWidget.setCurrentIndex(2)

    def create_balance_button_clicked(self):
        month_year = self.ui.create_balance_combo.currentText()
        message = f"Вы уверены, что хотите сформировать баланс для {month_year}? " \
                  f"Данный период времени будет закрыт для добавления новых операций, а все старый операции, " \
                  f"попавшие в данный период времени станут не доступны для изменения или удаления."
        reply = QtWidgets.QMessageBox.question(self, "Расформирование баланса", message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            db = sql.Sql()
            text = str(self.ui.create_balance_combo.currentText())
            year = text[-4:]
            month = month_mapping[text[:-5]]
            from_date = f"{year}-{month}-01"
            if month != "12":
                month = int(month) + 1
                month = f"0{month}" if month < 10 else f"{month}"
                to_date = f"{year}-{month}-01"
            else:
                to_date = f"{str(int(year) + 1)}-01-01"
            create_date = to_date
            db.cursor.execute(
                f"SELECT SUM(debit) from OPERATIONS where operations.create_date>=to_timestamp('{from_date}', 'YYYY-MM-DD') "
                f"and operations.create_date<to_timestamp('{to_date}', 'YYYY-MM-DD')")
            debit = str(db.cursor.fetchone()[0])
            db.cursor.execute(
                f"SELECT SUM(credit) from OPERATIONS where operations.create_date>=to_timestamp('{from_date}', 'YYYY-MM-DD') "
                f"and operations.create_date<to_timestamp('{to_date}', 'YYYY-MM-DD')")
            credit = str(db.cursor.fetchone()[0])
            amount = str(float(credit) - float(debit))
            try:
                db.cursor.execute(f"INSERT INTO BALANCE (create_date, debit, credit, amount) "
                                  f"VALUES(to_timestamp('{create_date}', 'YYYY-MM-DD'), {debit}, {credit}, {amount})")

                db.cursor.execute(f"UPDATE OPERATIONS SET balance_id = (select max(id) from balance) where "
                                  f"operations.create_date>=to_timestamp('{from_date}', 'YYYY-MM-DD') and "
                                  f"operations.create_date<to_timestamp('{to_date}', 'YYYY-MM-DD')")
                db.cnxn.commit()
                message = "Баланс сформирован."
                reply = QtWidgets.QMessageBox.question(self, "Успех", message, QtWidgets.QMessageBox.Ok)
                self.ui.tabWidget.setCurrentIndex(1)
                self.ui.tabWidget.setCurrentIndex(2)
            except:
                message = "Нельзя сформировать баланс с пустым приходом или расходом."
                error_message = QtWidgets.QErrorMessage(self)
                error_message.setModal(True)
                error_message.setWindowTitle("Ошибка формирования баланса")
                error_message.showMessage(message)

    def tab_changed_handler(self, index):
        if index == 0:
            self.disable_button(self.ui.delete_article_button)
            self.disable_button(self.ui.edit_article_button)
            self.disable_button(self.ui.add_article_button)
            self.ui.articles_table.setRowCount(0)
            self.db = sql.Sql()
            self.db.cursor.execute("SELECT id, name from articles order by name")
            self.ui.articles_combo_edit.clear()
            self.ui.articles_combo_edit.addItem("")
            row = self.db.cursor.fetchone()
            self.articles_list = list()
            if (row is not None):
                i = 0
                self.ui.no_articles_label.hide()
                self.ui.articles_table.show()
                while (row is not None):
                    print(row)
                    self.articles_list.append(str(row[0]))
                    text_combo = f"{i + 1}. {str(row[1])}"
                    self.ui.articles_combo_edit.addItem(text_combo)
                    self.ui.articles_table.setRowCount(self.ui.articles_table.rowCount() + 1)
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.articles_table.setVerticalHeaderItem(i, item)
                    self.ui.articles_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                    self.ui.articles_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.ui.articles_table.item(i, 1).setFlags(QtCore.Qt.NoItemFlags)
                    self.ui.articles_table.item(i, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.articles_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                    row = self.db.cursor.fetchone()
                    i += 1
            else:
                self.ui.no_articles_label.show()
                self.ui.articles_table.hide()
        elif (index == 1):
            print(1)
            self.reset_search()
            self.reset_time()
            self.reset_edit()
        elif (index == 2):
            self.disable_button(self.ui.create_balance_button)
            self.disable_button(self.ui.delete_balance_button)
            self.ui.balances_table.setRowCount(0)
            self.db = sql.Sql()
            self.ui.no_items_label_2.hide()
            self.ui.balances_table.show()
            self.db.cursor.execute("SELECT b.id, b.create_date, b.credit, b.debit, b.amount, oper_count "
                                   "from balances_with_count b order by b.create_date")
            self.ui.delete_balance_combo.clear()
            self.ui.delete_balance_combo.addItem("")
            row = self.db.cursor.fetchone()
            self.balances_list = list()
            if (row is not None):
                i = 0
                while (row is not None):
                    self.balances_list.append(str(row[0]))
                    text_combo = f"{i + 1}. {str(row[1])[:10]}: {str(row[5])[:-2]} opers, amount={str(row[4])}"
                    self.ui.delete_balance_combo.addItem(text_combo)
                    self.ui.balances_table.setRowCount(self.ui.balances_table.rowCount() + 1)
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.balances_table.setVerticalHeaderItem(i, item)
                    self.ui.balances_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
                    self.ui.balances_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                    for j in range(1, 6):
                        elem = str(row[j])
                        if j == 1:
                            elem = elem[:10]
                        if j == 5:
                            elem = elem[:-2]
                        self.ui.balances_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                        self.ui.balances_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                    row = self.db.cursor.fetchone()
                    i += 1
            else:
                self.ui.no_items_label_2.show()
                self.ui.balances_table.hide()
            self.ui.create_balance_combo.clear()
            self.ui.create_balance_combo.addItem("")
            self.db.cursor.execute("SELECT op.create_date FROM operations op where op.balance_id is NULL order by op.create_date")
            row = self.db.cursor.fetchone()
            set_months = set()
            while (row is not None):
                year = str(row[0])[:4]
                month = month_mapping[str(str(row[0])[5:7])]
                month_string = f"{month} {year}"
                if month_string not in set_months:
                    set_months.add(month_string)
                    self.ui.create_balance_combo.addItem(month_string)
                row = self.db.cursor.fetchone()

    def analyze_button_clicked(self):
        db = sql.Sql()
        if self.ui.radio_monthes.isChecked():
            text = str(self.ui.monthes_combo.currentText())
            year = text[-4:]
            month = month_mapping[text[:-5]]
            db_from = f"{year}-{month}-01"
            if month != "12":
                month = int(month) + 1
                month = f"0{month}" if month < 10 else f"{month}"
                db_to = f"{year}-{month}-01"
            else:
                db_to = f"{str(int(year) + 1)}-01-01"
        else:
            db_from = self.ui.from_line.date()
            db_to = self.ui.to_line.date()
            db_from = f"{db_from.year()}-{db_from.month()}-{db_from.day()}"
            db_to = f"{db_to.year()}-{db_to.month()}-{db_to.day()}"
        article_name = str(self.ui.articles_combo.currentText())
        if article_name == "Все статьи":
            query = f"SELECT op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
        else:
            query = f"SELECT op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                    f"join articles a on op.article_id=a.id " \
                    f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                    f"and op.create_date<=to_timestamp('{db_to}', 'YYYY-MM-DD') and a.name='{article_name}' order by op.create_date"
        db.cursor.execute(query)
        row = db.cursor.fetchone()
        debits = dict()
        credits = dict()
        while (row is not None):
            article = str(row[1])
            if article not in list(debits.keys()):
                debits[article] = []
            if article not in list(credits.keys()):
                credits[article] = []
            debit = float(str(row[3]))
            credit = float(str(row[2]))
            date = row[0]
            debits[article].append((date, debit))
            credits[article].append((date, credit))
            row = db.cursor.fetchone()
        if len(debits) == 0 and len(credits) == 0:
            print("Nothing to show")
            return
        if len(debits) != 0:
            for article in list(debits.keys()):
                x = [elem[0] for elem in debits[article]]
                y_tmp = [elem[1] for elem in debits[article]]
                y = [sum(y_tmp[:i + 1]) for i in range(len(y_tmp))]
                plt.plot(x, y, label=article)
            plt.title("debit")
            plt.legend(loc="best")
            plt.xticks(rotation=90)
            plt.show()
        if len(credits) != 0:
            for article in list(credits.keys()):
                x = [elem[0] for elem in credits[article]]
                y_tmp = [elem[1] for elem in credits[article]]
                y = [sum(y_tmp[:i + 1]) for i in range(len(y_tmp))]
                plt.plot(x, y, label=article)
            plt.title("credit")
            plt.legend(loc="best")
            plt.xticks(rotation=90)
            plt.show()
        if article_name == "Все статьи":
            db.cursor.execute(query)
            row = db.cursor.fetchone()
            debits = list()
            credits = list()
            while (row is not None):
                debit = float(str(row[3]))
                credit = float(str(row[2]))
                date = row[0]
                debits.append((date, debit))
                credits.append((date, credit))
                row = db.cursor.fetchone()
            if len(debits) == 0 and len(credits) == 0:
                print("Nothing to show")
                return

            x = [elem[0] for elem in debits]
            y_tmp = [elem[1] for elem in debits]
            y = [sum(y_tmp[:i + 1]) for i in range(len(y_tmp))]
            plt.plot(x, y, label="Все статьи")
            plt.title("debit sum")
            plt.legend(loc="best")
            plt.xticks(rotation=90)
            plt.show()

            x = [elem[0] for elem in credits]
            y_tmp = [elem[1] for elem in credits]
            y = [sum(y_tmp[:i + 1]) for i in range(len(y_tmp))]
            plt.plot(x, y, label="Все статьи")
            plt.title("credit sum")
            plt.legend(loc="best")
            plt.xticks(rotation=90)
            plt.show()


