# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_winLogin(object):
    def setupUi(self, winLogin):
        winLogin.setObjectName("winLogin")
        winLogin.resize(500, 227)
        icon = QtGui.QIcon.fromTheme("C:\\Users\\baris\\Desktop\\Projects\\Balkan_Travel_Py\\Icons\\balkan-travel-logo.ico")
        winLogin.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(winLogin)
        self.centralwidget.setObjectName("centralwidget")
        self.lblPassword = QtWidgets.QLabel(self.centralwidget)
        self.lblPassword.setGeometry(QtCore.QRect(24, 82, 125, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPassword.setFont(font)
        self.lblPassword.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPassword.setObjectName("lblPassword")
        self.lblUsername = QtWidgets.QLabel(self.centralwidget)
        self.lblUsername.setGeometry(QtCore.QRect(24, 50, 125, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblUsername.setFont(font)
        self.lblUsername.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblUsername.setObjectName("lblUsername")
        self.txtUsername = QtWidgets.QLineEdit(self.centralwidget)
        self.txtUsername.setGeometry(QtCore.QRect(152, 48, 263, 29))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.txtUsername.setFont(font)
        self.txtUsername.setText("")
        self.txtUsername.setPlaceholderText("")
        self.txtUsername.setObjectName("txtUsername")
        self.txtPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.txtPassword.setGeometry(QtCore.QRect(152, 80, 263, 29))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txtPassword.setFont(font)
        self.txtPassword.setText("")
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtPassword.setPlaceholderText("")
        self.txtPassword.setObjectName("txtPassword")
        self.btnLogin = QtWidgets.QPushButton(self.centralwidget)
        self.btnLogin.setGeometry(QtCore.QRect(186, 128, 151, 65))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btnLogin.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Balkan_Travel_Py/Balkan_Travel/iconlar/Check_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLogin.setIcon(icon)
        self.btnLogin.setIconSize(QtCore.QSize(24, 24))
        self.btnLogin.setObjectName("btnLogin")
        self.cbLanguage = QtWidgets.QComboBox(self.centralwidget)
        self.cbLanguage.setGeometry(QtCore.QRect(404, 194, 91, 29))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.cbLanguage.setFont(font)
        self.cbLanguage.setEditable(False)
        self.cbLanguage.setObjectName("cbLanguage")
        self.cbLanguage.addItem("")
        self.cbLanguage.addItem("")
        winLogin.setCentralWidget(self.centralwidget)

        self.retranslateUi(winLogin)
        QtCore.QMetaObject.connectSlotsByName(winLogin)

    def retranslateUi(self, winLogin):
        _translate = QtCore.QCoreApplication.translate
        winLogin.setWindowTitle(_translate("winLogin", "CLIENT TRACING PROGRAM"))
        self.lblPassword.setText(_translate("winLogin", "Şifre :"))
        self.lblUsername.setText(_translate("winLogin", "Kullanıcı Adı :"))
        self.btnLogin.setText(_translate("winLogin", "Giriş"))
        self.cbLanguage.setCurrentText(_translate("winLogin", "English"))
        self.cbLanguage.setItemText(0, _translate("winLogin", "English"))
        self.cbLanguage.setItemText(1, _translate("winLogin", "Türkçe"))
