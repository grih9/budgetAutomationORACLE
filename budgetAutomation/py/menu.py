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
    # #     self.ui.injJournalButton.clicked.connect(self.injButtonHandler)
    # #     self.ui.maleRadio.clicked.connect(self.maleRadioHandler)
    # #     self.ui.femaleRadio.clicked.connect(self.femaleRadioHandler)
    # #     self.ui.youngRadio.clicked.connect(self.youngRadioHandler)
    # #     self.ui.resetButton.clicked.connect(self.resetButton_clicked)
    # #     self.ui.allPlayersRadio.clicked.connect(self.allPlayersRadioHandler)
    # #     self.ui.defRadio.clicked.connect(self.defRadioHandler)
    # #     self.ui.midRadio.clicked.connect(self.midRadioHandler)
    # #     self.ui.forwardRadio.clicked.connect(self.forwardRadioHandler)
    # #     self.ui.goalkeepersRadio.clicked.connect(self.goalkeepersRadioHandler)
    # #     self.ui.injCheckBox.stateChanged.connect(self.injCheckBoxHandler)
    # #     self.ui.expiredRadio.clicked.connect(self.expiredRadioHandler)
    # #     self.ui.allRadio.clicked.connect(self.allRadioHandler)
    # #
        self.ui.tabWidget.setCurrentIndex(1)
        self.db = sql.Sql()
        self.ui.entry_message.setText(f"Привет, {properties.current_login}!")
        header = self.ui.operations_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
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
        if size == 1:
            self.ui.left_arrow.setEnabled(False)
            self.ui.left_arrow.setStyleSheet("background-color: rgb(13, 243, 255)")
        if size != 0:
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
                    f"and op.create_date<to_timestamp('{db_to}', 'YYYY-MM-DD')"
            self.db.cursor.execute(query)
            row = self.db.cursor.fetchone()
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
                        if j == 4 and elem == "None":
                            elem = "-"
                        self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                        self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                    row = self.db.cursor.fetchone()
                    i += 1
            else:
                self.ui.no_items_label.show()
                self.ui.operations_table.hide()
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

    def tab_changed_handler(self, index):
        if (index == 0):
            # self.ui.injCheckBox.setChecked(False)
            # self.ui.defB.setChecked(True)
            # self.ui.allPlayersRadio.setChecked(True)
            # self.ui.allRadio.setChecked(True)
            # self.ui.youngRadio.setChecked(False)
            # self.ui.maleRadio.setChecked(False)
            # self.ui.femaleRadio.setChecked(False)
            # self.db.cursor.execute(
            #     "SELECT Команды.Страна, Команды.Город, Стадионы.Название, Стадионы.Вместимость, Стадионы.Город, Тренеры_и_персонал.ФИО,"
            #     "Тренеры_и_персонал.Национальность, Руководство.ФИО, Руководство.Национальность"
            #     " FROM Команды "
            #     "join Стадионы on Стадионы.ID_стадиона = Команды.ID_стадиона "
            #     "join Тренеры_и_персонал on Тренеры_и_персонал.ID_специалиста=ID_главного_тренера "
            #     "join Руководство on Руководство.ID_владельца = Команды.ID_владельца "
            #     "where  Команды.Команда ='" + str("Манчестер Юнайтед") + "'")
            # row = self.db.cursor.fetchone()
            # country = row[0]
            # city = row[1]
            # stadium = row[2]
            # capacity = row[3]
            # stadiumCity = row[4]
            # coachFIO = row[5]
            # coachCountry = row[6]
            # ownerFIO = row[7]
            # ownerCountry = row[8]
            # self.ui.countryLabel.setText(country.rstrip())
            self.ui.cityLabel.setText(city.rstrip())
            # self.ui.stadiumLabel.setText((stadium.rstrip() + " (" + stadiumCity.lstrip()).rstrip() + ")")
            # self.ui.capacityLabel.setText(str(capacity))
            # self.ui.coachLabel.setText((coachFIO.rstrip() + " (" + coachCountry.lstrip()).rstrip() + ")")
            # self.ui.ownerLabel.setText((ownerFIO.rstrip() + " (" + ownerCountry.lstrip()).rstrip() + ")")
        elif (index == 1):
            self.ui.radio_monthes.setChecked(True)
            self.ui.radio_dates.setChecked(False)
            self.ui.articles_combo.setCurrentIndex(0)
            self.ui.add_operation_buttonbutton.setEnabled(True)
            date = datetime.now()
            self.ui.from_line.setDate(date)
            self.ui.to_line.setDate(date)
            self.ui.no_items_label.hide()
            self.ui.operations_table.show()
            self.ui.operations_table.setRowCount(0)
            self.db.cursor.execute(
                "SELECT op.create_date, a.name, op.debit, op.credit, b.create_date FROM operations op "
                "join articles a on op.article_id=a.id "
                "left join balance b on op.balance_id=b.id")
            row = self.db.cursor.fetchone()
            if (row is not None):
                i = 0
                while (row is not None):
                    self.ui.operations_table.setRowCount(self.ui.operations_table.rowCount() + 1)
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.operations_table.setVerticalHeaderItem(i, item)
                    for j in range(5):
                        elem = str(row[j])
                        if j == 0:
                            elem = elem[:10]
                        self.ui.operations_table.setItem(i, j, QtWidgets.QTableWidgetItem(elem))
                        self.ui.operations_table.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                    row = self.db.cursor.fetchone()
                    i += 1
            else:
                self.ui.no_items_label.show()
                self.ui.operations_table.hide()
        elif (index == 2):
            # self.ui.injCheckBox.setChecked(False)
            # self.ui.defB.setChecked(True)
            # self.ui.noContractrsLabel.hide()
            self.ui.noPlayersLabel.hide()
            # self.ui.noFansLabel_3.hide()
            # self.ui.allPlayersRadio.setChecked(True)
            # self.ui.allRadio.setChecked(True)
            # self.ui.youngRadio.setChecked(False)
            # self.ui.maleRadio.setChecked(False)
            # self.ui.femaleRadio.setChecked(False)
            # self.ui.coachesTabel.setRowCount(0)
            # self.db.cursor.execute(
            #     "SELECT ФИО, Национальность, Дата_рождения, Должность FROM Тренеры_и_персонал "
            #     "join Команды on Команды.ID_команды=Тренеры_и_персонал.ID_команды where Команда ='" + str("Манчестер Юнайтед") + "'")
            # row = self.db.cursor.fetchone()
            # i = 0
            # while (row is not None):
            #     self.ui.coachesTabel.setRowCount(self.ui.coachesTabel.rowCount() + 1)
            #     item = QtWidgets.QTableWidgetItem()
            #     self.ui.coachesTabel.setVerticalHeaderItem(i, item)
            #     for j in range(4):
            #         self.ui.coachesTabel.setItem(i, j, QtWidgets.QTableWidgetItem(str(row[j])))
            #         self.ui.coachesTabel.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
            #     row = self.db.cursor.fetchone()
            #     i += 1
