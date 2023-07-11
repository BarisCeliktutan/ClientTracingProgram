from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from Designs import Main_Win_Ui
import pymysql


class Common(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_win = Main_Win_Ui.Ui_winMain()
        self.main_win.setupUi(self)
        self.kucukler = ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i", "j", "k", "l", "m", "n", "o", "ö", "p", "r", "s",
         "ş", "t", "u", "ü", "v", "y", "z", "q", "x", "w"]
        self.buyukler = ["A", "B", "C", "Ç", "D", "E", "F", "G", "Ğ", "H", "I", "İ", "J", "K", "L", "M", "N", "O", "Ö", "P", "R", "S",
         "Ş", "T", "U", "Ü", "V", "Y", "Z", "Q", "X", "W"]

    def server(self, query, do):
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='Justy1992',
                             db='balkantraveldb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        con = db.cursor()
        con.execute(query)
        xquery = con.fetchall()
        if do == "all":
            db.close()
            return xquery
        elif do == "commit":
            db.commit()
            db.close()

    def date(self, sender, dates, check_boxes, state):
        date_index = check_boxes.index(sender)
        if state == QtCore.Qt.Checked:
            dates[date_index].setEnabled(True)
        else:
            dates[date_index].setEnabled(False)

    def phone_format(self, sender):
        text = sender.text()
        try:
            if text[0] != "0":
                text = (f"0{text}")
        except:
            pass
        text = text.replace(" ", "")
        if len(text) > 4:
            text = text[:4] + " " + text[4:]
        if len(text) > 8:
            text = text[:8] + " " + text[8:]
        if len(text) > 11:
            text = text[:11] + " " + text[11:]
        sender.setText(text)

    def turn_to_phone_format(self, tel):
        return f"{tel[:4]} {tel[4:7]} {tel[7:9]} {tel[9:]}"

    def full_capital(self, kelimeler):
        if kelimeler == "" or kelimeler == " ":
            return ""
        cevrilen = ""
        for harf in kelimeler:
            if harf == " ":
                cevrilen += " "
                continue
            try:
                index = self.buyukler.index(harf)
            except:
                index = self.kucukler.index(harf)
            else:
                pass  # ' Şu tırnak işareti vs. geldiği takdirde hata vermesin diye else koydum.
            cevrilen += self.buyukler[index]
        return cevrilen

    def make_title(self, kelimeler):
        if kelimeler == "" or kelimeler == " ":
            return ""
        cevrilen = ""
        for k in kelimeler.split(" "):
            try:
                x = self.buyukler[self.kucukler.index(k[0])]
                cevrilen += f" {x}"
            except:
                cevrilen += f" {k[0]}"
            for harf in k[1:]:
                try:
                    index = self.buyukler.index(harf)
                except:
                    cevrilen += harf
                    continue
                cevrilen += self.kucukler[index]
        return cevrilen[1:]

    def user_info(self, kul):
        global user
        user = kul

    def fetch_user(self):
        return user

    def date_format(self, dt):
        return f"{dt[2]}.{dt[1]}.{dt[0]}"
