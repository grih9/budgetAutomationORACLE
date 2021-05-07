import sys

from PyQt5 import QtWidgets
from matplotlib import pyplot
from start_menu import StartMenu
from sql import Sql

if __name__ == '__main__':
    db = Sql()
    # db.cursor.execute(
    #     "select (sum(credit) - sum(debit)) as profit from operations where create_date = to_timestamp('2021-02-23', 'YYYY-MM-DD')")
    # row = db.cursor.fetchall()
    # print(row)
    app = QtWidgets.QApplication([])
    window = StartMenu()
    window.show()
    db.cnxn.close()
    sys.exit(app.exec())
