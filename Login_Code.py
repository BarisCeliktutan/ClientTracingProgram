from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5.QtCore import Qt
from Designs import Login_Ui
from Codes.Main_Win_Code import MainWindow
from Common_Codes import Common


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_win = Login_Ui.Ui_winLogin()
        self.login_win.setupUi(self)
        self.login_win.btnLogin.clicked.connect(self.login)
        self.main_window = MainWindow()
        self.set_language()
        self.login_win.cbLanguage.currentTextChanged.connect(self.set_language)

    def set_language(self):
        if self.login_win.cbLanguage.currentText() == "English":
            self.login_win.lblUsername.setText("Username :")
            self.login_win.lblPassword.setText("Password :")
            self.login_win.btnLogin.setText("LOGIN")
            self.msg_title = "Warning!"
            self.msg = "Wrong username or password has been entered."
        else:
            self.login_win.lblUsername.setText("Kullanıcı Adı :")
            self.login_win.lblPassword.setText("Şifre :")
            self.login_win.btnLogin.setText("GİRİŞ")
            self.msg_title = "Uyarı!"
            self.msg = "Hatalı kullanıcı adı veya şifre giridi."

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.login_win.btnLogin.click()

    def login(self):
        username = self.login_win.txtUsername.text()
        password = self.login_win.txtPassword.text()
        my_query = f"SELECT ID, ADI_SOYADI, KULLANICI_ADI, YETKILI, SUBE_ID, SUBE_ADI FROM view_kullanicilar WHERE KULLANICI_ADI = '{username}' AND PAROLA = '{password}' AND SILINDI = 0 AND AKTIF = 1"
        try:
            self.user = Common().server(my_query, "all")[0]
            Common().user_info(self.user)
            self.main_window.settings()
            if self.login_win.cbLanguage.currentText() == "English":
                self.main_window.set_language()
            self.main_window.fill_processes()
            self.main_window.showMaximized()
            self.hide()
        except:
            QMessageBox.critical(self, f"{self.msg_title}", f"{self.msg}")


app = QApplication([])
win = Login()
win.show()
app.exec_()

