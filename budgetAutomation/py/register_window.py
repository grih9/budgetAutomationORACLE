# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import eye
import home

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1016, 755)
        MainWindow.setMinimumSize(QtCore.QSize(1016, 755))
        MainWindow.setMaximumSize(QtCore.QSize(1016, 755))
        MainWindow.setStyleSheet("QWidget#centralwidget {\n"
"    background-color: rgb(57, 172, 172)\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 150, 631, 551))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(20)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("QGroupBox#groupBox {\n"
"    color: rgb(10, 110, 180);\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.create_account_button = QtWidgets.QCommandLinkButton(self.groupBox)
        self.create_account_button.setGeometry(QtCore.QRect(120, 470, 381, 91))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(23)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.create_account_button.setFont(font)
        self.create_account_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.create_account_button.setStyleSheet(" color: rgb(10,110, 210);")
        icon = QtGui.QIcon.fromTheme("NO")
        self.create_account_button.setIcon(icon)
        self.create_account_button.setIconSize(QtCore.QSize(300, 300))
        self.create_account_button.setObjectName("create_account_button")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(210, 60, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.login_line = QtWidgets.QLineEdit(self.groupBox)
        self.login_line.setGeometry(QtCore.QRect(170, 100, 275, 50))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.login_line.setFont(font)
        self.login_line.setAlignment(QtCore.Qt.AlignCenter)
        self.login_line.setObjectName("login_line")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(210, 180, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.password_line = QtWidgets.QLineEdit(self.groupBox)
        self.password_line.setGeometry(QtCore.QRect(170, 220, 275, 50))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.password_line.setFont(font)
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setAlignment(QtCore.Qt.AlignCenter)
        self.password_line.setObjectName("password_line")
        self.password_line_confirm = QtWidgets.QLineEdit(self.groupBox)
        self.password_line_confirm.setGeometry(QtCore.QRect(170, 340, 275, 50))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.password_line_confirm.setFont(font)
        self.password_line_confirm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.password_line_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_confirm.setAlignment(QtCore.Qt.AlignCenter)
        self.password_line_confirm.setObjectName("password_line_confirm")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(165, 300, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.passwod_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.passwod_checkbox.setGeometry(QtCore.QRect(487, 280, 20, 50))
        self.passwod_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.passwod_checkbox.setText("")
        self.passwod_checkbox.setObjectName("passwod_checkbox")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(480, 260, 31, 31))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/eye/eyepng.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_3.setGeometry(QtCore.QRect(710, 50, 251, 181))
        self.graphicsView_3.setMaximumSize(QtCore.QSize(499, 500))
        self.graphicsView_3.setStyleSheet("background-image: url(C:/git/budgetAuto/budgetAutomation/resources/money.jpg);")
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.backButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(750, 585, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.backButton.setFont(font)
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setStyleSheet(" color: rgb(10,110, 210);")
        icon = QtGui.QIcon.fromTheme("NO")
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(300, 300))
        self.backButton.setObjectName("backButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, -20, 481, 181))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_4.setGeometry(QtCore.QRect(690, 290, 301, 251))
        self.graphicsView_4.setMaximumSize(QtCore.QSize(499, 500))
        self.graphicsView_4.setStyleSheet("background-image: url(C:/git/budgetAuto/budgetAutomation/resources/user.png);")
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(690, 590, 61, 51))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap(":/home/home.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.graphicsView_3.raise_()
        self.groupBox.raise_()
        self.backButton.raise_()
        self.label_4.raise_()
        self.graphicsView_4.raise_()
        self.label_6.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1016, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "?????????? ????????????????????????"))
        self.create_account_button.setText(_translate("MainWindow", "?????????????? ??????????????"))
        self.label_2.setText(_translate("MainWindow", "??????????"))
        self.label_3.setText(_translate("MainWindow", "????????????"))
        self.label_5.setText(_translate("MainWindow", "??????????????????????????"))
        self.backButton.setText(_translate("MainWindow", "??????????"))
        self.label_4.setText(_translate("MainWindow", "?????????????????????????? ?????????????????? ??????????????"))

