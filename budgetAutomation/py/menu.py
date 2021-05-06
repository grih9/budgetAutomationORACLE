import sql
import start_menu
import properties
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
        self.ui.tabWidget.setCurrentIndex(1)
        self.db = sql.Sql()
        self.ui.entry_message.setText(f"Привет, {properties.current_login}!")
        header = self.ui.operations_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header = self.ui.articles_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header = self.ui.balances_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
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
        query = "SELECT a.name from articles a"
        self.db.cursor.execute(query)
        row = self.db.cursor.fetchone()
        while (row is not None):
            self.ui.article_oper_add_combo.addItem(str(row[0]))
            self.ui.articles_combo.addItem(str(row[0]))
            row = self.db.cursor.fetchone()

    def exit_button_clicked(self):
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
                for j in range(5):
                    elem = str(row[j + 1])
                    if j == 0:
                        elem = elem[:10]
                    elif j == 4 and elem == "None":
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
                for j in range(5):
                    elem = str(row[j + 1])
                    if j == 0:
                        elem = elem[:10]
                    elif j == 4 and elem == "None":
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
                for j in range(5):
                    elem = str(row[j + 1])
                    if j == 0:
                        elem = elem[:10]
                    elif j == 4 and elem == "None":
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
                for j in range(5):
                    elem = str(row[j + 1])
                    if j == 0:
                        elem = elem[:10]
                    elif j == 4 and elem == "None":
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
                for j in range(5):
                    elem = str(row[j + 1])
                    if j == 0:
                        elem = elem[:10]
                    elif j == 4 and elem == "None":
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
                for j in range(5):
                    elem = str(row[j + 1])
                    print(elem)
                    if j == 0:
                        elem = elem[:10]
                    elif j == 4 and elem == "None":
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
                self.disable_button(self.ui.edit_article_button)
                self.disable_button(self.ui.add_article_button)
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
                    self.ui.articles_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.ui.articles_table.item(i, 0).setFlags(QtCore.Qt.NoItemFlags)
                    self.ui.articles_table.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    row = self.db.cursor.fetchone()
                    i += 1
            else:
                self.ui.no_articles_label.show()
                self.ui.articles_table.hide()

        elif (index == 1):
            self.ui.radio_monthes.setChecked(True)
            self.ui.radio_dates.setChecked(False)
            self.ui.monthes_combo.clear()
            self.ui.article_oper_add_combo.clear()
            self.ui.articles_combo.clear()
            self.ui.oper_edit_combo.clear()
            self.ui.articles_combo.addItem("Все статьи")
            self.ui.oper_edit_combo.addItem("")
            self.ui.article_oper_add_combo.addItem("")
            self.ui.articles_combo.setCurrentIndex(0)
            self.ui.add_operation_button.setEnabled(False)
            self.ui.delete_oper_button.setEnabled(False)
            self.ui.edit_oper_button.setEnabled(False)
            self.ui.right_arrow.setEnabled(False)
            self.ui.from_line.setEnabled(False)
            self.ui.to_line.setEnabled(False)
            self.ui.add_operation_button.setStyleSheet("background-color: rgb(13, 243, 255)")
            self.ui.delete_oper_button.setStyleSheet("background-color: rgb(13, 243, 255)")
            self.ui.edit_oper_button.setStyleSheet("background-color: rgb(13, 243, 255)")
            self.ui.right_arrow.setStyleSheet("background-color: rgb(13, 243, 255)")
            date = datetime.now()
            self.ui.from_line.setDate(date)
            self.ui.from_line.setMaximumDate(date)
            self.ui.to_line.setMinimumDate(date)
            self.ui.to_line.setDate(date)
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            self.ui.operations_table.setRowCount(0)
            db = sql.Sql()
            db.cursor.execute("SELECT op.create_date FROM operations op order by op.create_date")
            row = db.cursor.fetchone()
            set_months = set()
            while (row is not None):
                year = str(row[0])[:4]
                month = month_mapping[str(str(row[0])[5:7])]
                month_string = f"{month} {year}"
                if month_string not in set_months:
                    set_months.add(month_string)
                    self.ui.monthes_combo.addItem(month_string)
                row = db.cursor.fetchone()
            size = self.ui.monthes_combo.count()
            if size == 1:
                self.ui.left_arrow.setEnabled(False)
                self.ui.left_arrow.setStyleSheet("background-color: rgb(13, 243, 255)")
            if size > 1:
                self.ui.monthes_combo.setCurrentIndex(int(size) - 1)
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

                query = f"SELECT op.id, op.create_date, a.name, op.credit, op.debit, b.create_date FROM operations op " \
                        f"join articles a on op.article_id=a.id " \
                        f"left join balance b on op.balance_id=b.id where op.create_date>=to_timestamp('{db_from}', 'YYYY-MM-DD') " \
                        f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD') order by op.create_date"
                db.cursor.execute(query)
                row = db.cursor.fetchone()
                self.oper_list = list()
                if (row is not None):
                    i = 0
                    while (row is not None):
                        self.oper_list.append(str(row[0]))
                        text_combo = f"{i + 1}. {str(row[1])[:10]}. {str(row[2])} +{str(row[3])} -{str(row[4])}"
                        self.ui.oper_edit_combo.addItem(text_combo)
                        self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                        item = QtWidgets.QTableWidgetItem()
                        self.ui.operations_table.setVerticalHeaderItem(i, item)
                        for j in range(5):
                            elem = str(row[j + 1])
                            if j == 0:
                                elem = elem[:10]
                            elif j == 4 and elem == "None":
                                elem = "-"
                            self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                            self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                        row = db.cursor.fetchone()
                        i += 1
                else:
                    self.ui.no_items_label.show()
                    self.ui.operations_table.hide()
            else:
                self.ui.no_items_label.show()
                self.ui.operations_table.hide()

            query = "SELECT a.name from articles a"
            db.cursor.execute(query)
            row = db.cursor.fetchone()
            while (row is not None):
                self.ui.article_oper_add_combo.addItem(str(row[0]))
                self.ui.articles_combo.addItem(str(row[0]))
                row = db.cursor.fetchone()
