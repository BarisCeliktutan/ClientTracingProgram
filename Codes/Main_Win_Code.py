# -*- coding: iso-8859-9 -*-

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDate
from Designs.Main_Win_Ui import Ui_winMain
from Codes import Users_Code, Detailed_Search_Code, Clients_Code, DLD_Code, Currency_Code, Send_SMS_Code, SMS_Report_Code,  Money_Movements_Code, Remindings_Code
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Common_Codes import Common


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_win = Ui_winMain()
        self.main_win.setupUi(self)
        date = datetime.today()
        first_dt = datetime(date.year, date.month, 1)
        last_dt = first_dt + relativedelta(months=1, days=-1)
        self.lang_flag = 0

        self.main_win.dtFirst.setDate(QDate(first_dt.year, first_dt.month, first_dt.day))
        self.main_win.dtLast.setDate(QDate(last_dt.year, last_dt.month, last_dt.day))

        self.users_win = Users_Code.Users()
        self.detailed_search_win = Detailed_Search_Code.DetailedSearch()
        self.clients_win = Clients_Code.Clients()
        self.dld_win = DLD_Code.DLD()
        self.currency_win = Currency_Code.Currency()
        self.send_sms_win = Send_SMS_Code.SendSMS()
        self.sms_report_win = SMS_Report_Code.SMSReport()
        self.money_win = Money_Movements_Code.MoneyMovements()
        self.remindings_win = Remindings_Code.Remindings()
        self.common = Common()

        self.main_win.tbwTabs.setColumnHidden(0, True)  # id
        self.main_win.tbwProcesses.setColumnHidden(0, True)
        self.main_win.tbwProcesses.setColumnHidden(16, True)
        self.main_win.tbwProcesses.setColumnHidden(17, True)
        self.main_win.tbwProcesses.setColumnHidden(18, True)
        self.main_win.tbwProcesses.setColumnHidden(19, True)

        self.main_win.tbwTabs.setColumnWidth(1, 239)

        branches_query = "SELECT SUBE_ADI FROM subeler"
        self.branch_list = Common().server(branches_query, "all")
        for i in range(len(self.branch_list)):
            self.main_win.cbBranches.setItemText(i, self.branch_list[i]["SUBE_ADI"])

        self.main_win.frmProcesses.hide()
        self.main_win.frmCitizenship.hide()
        self.main_win.frmVisa.hide()
        self.main_win.frmHolidaySells.hide()
        self.radio_buttons = [self.main_win.rbSchengen,self.main_win.rbBGVisa, self.main_win.rbDVisa,
                              self.main_win.rbInProcess, self.main_win.rbProcessFinished, self.main_win.rbThoseProcFinish,
                              self.main_win.rbThoseProcFinish, self.main_win.rbAll]
        self.main_win.rbSchengen.clicked.connect(lambda: self.change_color(self.main_win.rbSchengen))
        self.main_win.rbBGVisa.clicked.connect(lambda: self.change_color(self.main_win.rbBGVisa))
        self.main_win.rbDVisa.clicked.connect(lambda: self.change_color(self.main_win.rbDVisa))
        self.main_win.rbInProcess.clicked.connect(lambda: self.change_color(self.main_win.rbInProcess))
        self.main_win.rbProcessFinished.clicked.connect(lambda: self.change_color(self.main_win.rbProcessFinished))
        self.main_win.rbCouldNotReach.clicked.connect(lambda: self.change_color(self.main_win.rbCouldNotReach))
        self.main_win.rbThoseProcFinish.clicked.connect(lambda: self.change_color(self.main_win.rbThoseProcFinish))
        self.main_win.rbAll.clicked.connect(lambda: self.change_color(self.main_win.rbAll))

        self.main_win.tbwTabs.clicked.connect(self.tab)
        self.check_boxes = [self.main_win.chFirst, self.main_win.chLast]
        self.dates = [self.main_win.dtFirst, self.main_win.dtLast]
        self.main_win.chFirst.stateChanged.connect(lambda: self.common.date(self.main_win.chFirst, self.dates, self.check_boxes, self.main_win.chFirst.checkState()))
        self.main_win.chLast.stateChanged.connect(lambda: self.common.date(self.main_win.chLast, self.dates, self.check_boxes, self.main_win.chLast.checkState()))

        self.main_win.tbwTabs.setColumnWidth(0, 231)

        self.main_win.btnDetailed.clicked.connect(self.detailed_search)
        self.main_win.btnShowAll.clicked.connect(self.show_all)
        self.main_win.btnMoney.clicked.connect(self.money)
        self.main_win.btnRemindings.clicked.connect(self.remindings)
        self.main_win.btnAppointments.clicked.connect(self.appointments)

        self.main_win.menuClients.aboutToShow.connect(self.clients)
        self.main_win.menuDLD.aboutToShow.connect(self.dld)
        self.main_win.menuUsers.aboutToShow.connect(self.users)
        self.main_win.menuCurrency.aboutToShow.connect(self.currency)
        self.main_win.menuAuthorities.aboutToShow.connect(self.authorities)
        self.main_win.actionSendSMS.triggered.connect(self.send_sms)
        self.main_win.actionSMSReport.triggered.connect(self.sms_report)
        self.main_win.menuExit.aboutToShow.connect(self.exit)

    def fetch_processes(self):
        # if self.user['YETKILI'] == 1:
        #     authority =
        process_type_id = " "
        dt_first = ""
        dt_last = ""
        try:
            print(type(self.main_win.tbwTabs.item(self.main_win.tbwTabs.currentRow(), 1).text()))
            if self.main_win.tbwTabs.item(self.main_win.tbwTabs.currentRow(), 0).text() > 0:
                process_type_id = f"AND ISLEM_TURU_ID = {self.user['ISLEM_TURU_ID']} "
        except:
            pass
        if self.main_win.chFirst.isChecked() == True:
            first = f"\'{self.main_win.dtFirst.date().toString('yyyy-MM-dd')}\'"
            dt_first = f"AND ISLEM_GORDUGU_TARIH >= {first}"

        if self.main_win.chLast.isChecked() == True:
            last = f"\'{self.main_win.dtLast.date().toString('yyyy-MM-dd')}\'"
            dt_last = f"AND ISLEM_GORDUGU_TARIH <= {last}"
        try:
            if self.main_win.tbwTabs.item(self.main_win.tbwTabs.currentRow(), 1).text() == "TATİL SATIŞ":
                order_by = "VOUCHER DESC"
        except:
            order_by = "ISLEM_GORDUGU_TARIH DESC, DOSYA_KAYIT_TAR DESC"

        query = f"SELECT * FROM view_hareketler WHERE SILINDI = 0 AND (ALINAN_NOTLAR_SILINDI <> 1 OR ALINAN_NOTLAR_SILINDI IS NULL) {process_type_id} {dt_first} {dt_last} ORDER BY {order_by}"
        return Common().server(query, "all")

    def fill_processes(self):
        process = self.fetch_processes()
        self.main_win.tbwProcesses.setRowCount(len(process))
        for i in range(len(process)):
            self.main_win.tbwProcesses.setItem(i, 0, QTableWidgetItem(str(process[i]["ID"])))
            self.main_win.tbwProcesses.setItem(i, 1, QTableWidgetItem(self.common.date_format(str(process[i]["ISLEM_GORDUGU_TARIH"]).split("-"))))
            self.main_win.tbwProcesses.setItem(i, 2, QTableWidgetItem(self.common.date_format(str(process[i]["DOSYA_KAYIT_TAR"]).split("-"))))
            self.main_win.tbwProcesses.setItem(i, 3, QTableWidgetItem(process[i]["GORUNEN_AD"]))
            self.main_win.tbwProcesses.setItem(i, 4, QTableWidgetItem(process[i]["DOSYA_NO"]))
            self.main_win.tbwProcesses.setItem(i, 5, QTableWidgetItem(process[i]["ISLEM_TURU"]))
            self.main_win.tbwProcesses.setItem(i, 6, QTableWidgetItem(str(process[i]["BASLIK"])))
            self.main_win.tbwProcesses.setItem(i, 7, QTableWidgetItem(str(process[i]["ISLEM_TIPI"])))
            self.main_win.tbwProcesses.setItem(i, 8, QTableWidgetItem(str(process[i]["VIZE_TURU"])))
            self.main_win.tbwProcesses.setItem(i, 9, QTableWidgetItem(str(process[i]["NOT_GORUNEN_AD"])))
            self.main_win.tbwProcesses.setItem(i, 10, QTableWidgetItem(str(process[i]["VOUCHER"])))
            self.main_win.tbwProcesses.setItem(i, 11, QTableWidgetItem(str(process[i]["ALINAN_NOT"])))
            self.main_win.tbwProcesses.setItem(i, 12, QTableWidgetItem(str(process[i]["ADI"])))
            self.main_win.tbwProcesses.setItem(i, 13, QTableWidgetItem(str(process[i]["SOYADI"])))
            self.main_win.tbwProcesses.setItem(i, 14, QTableWidgetItem(str(process[i]["GSM"])))
            self.main_win.tbwProcesses.setItem(i, 15, QTableWidgetItem(str(process[i]["E_MAIL"])))
            self.main_win.tbwProcesses.setItem(i, 16, QTableWidgetItem(str(process[i]["MUSTERI_ID"])))
            self.main_win.tbwProcesses.setItem(i, 17, QTableWidgetItem(str(process[i]["ISLEM_TURU_ID"])))
            self.main_win.tbwProcesses.setItem(i, 18, QTableWidgetItem(str(process[i]["ISLEM_TIPI_ID"])))
            self.main_win.tbwProcesses.setItem(i, 19, QTableWidgetItem(str(process[i]["ISLEM"])))

    def settings(self):
        self.user = self.common.fetch_user()
        self.setWindowTitle(f"CLIENT TRACING PROGRAM - {self.user['ADI_SOYADI']}")
        self.main_win.cbBranches.setCurrentText(self.user["SUBE_ADI"])
        if self.user["KULLANICI_ADI"] != "B":
            self.main_win.frmBranch_ADMIN.hide()
        else:
            self.main_win.cbBranches_ADMIN.setCurrentText(self.user["SUBE_ADI"])
        processes_query = "SELECT * FROM islem_turleri;"
        processes = Common().server(processes_query, "all")
        self.main_win.tbwTabs.setRowCount(len(processes))
        for i in range(len(processes)):
            item = QTableWidgetItem(processes[i]["ISLEM_TURU"])
            self.main_win.tbwTabs.setItem(i, 1, item)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def detailed_search(self):
        self.detailed_search_win.show()

    def clients(self):
        self.clients_win.musteri_listele()
        self.clients_win.islem_turleri()
        self.clients_win.show()

    def dld(self):
        self.dld_win.show()

    def users(self):
        self.users_win.who(self.user["ID"])
        self.users_win.fill_users_tbw()
        self.users_win.show()

    def currency(self):
        self.currency_win.show()

    def authorities(self):
        print("Pressed to Authorities.")

    def send_sms(self):
        query = f"SELECT * FROM view_sms_tablosu ORDER BY ADI_SOYADI;"
        clients = Common().server(query, "all")
        self.send_sms_win.fill_clients(clients)
        self.send_sms_win.show()

    def sms_report(self):
        self.sms_report_win.show()

    def exit(self):
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if self.lang_flag == 1:
            msg.setWindowTitle("Warning!")
            msg.setText("Are you sure you want to quit?")
        else:
            msg.setWindowTitle("Uyarı!")
            msg.setText("Çıkmak istediğinden emin misin?")
            msg.button(QMessageBox.Yes).setText("Evet")
            msg.button(QMessageBox.No).setText("Hayır")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon.fromTheme("C:/Users/baris/Desktop/Projects/Balkan_Travel_Py/Icons/balkan-travel-logo.ico"))
        sure = msg.exec_()
        if sure == QMessageBox.Yes:
            self.close()

    def tab(self):
        tab = self.main_win.tbwTabs.item(self.main_win.tbwTabs.currentRow(), 1).text()
        if tab in "VATANDAŞLIK CITIZENSHIP":
            if self.lang_flag == 0:
                self.main_win.lblProcesses.setText("VATANDAŞLIK İŞLEMLERİ")
            else:
                self.main_win.lblProcesses.setText("CITIZENSHIP PROCESSES")

            self.main_win.frmProcesses.show()
            self.main_win.frmCitizenship.show()
            self.main_win.frmVisa.hide()
            self.main_win.frmHolidaySells.hide()

        elif tab in "VİZE VISA":
            if self.lang_flag == 0:
                self.main_win.lblProcesses.setText("VİZE İŞLEMLERİ")
            else:
                self.main_win.lblProcesses.setText("CITIZENSHIP PROCESSES")
            self.main_win.frmProcesses.show()
            self.main_win.frmVisa.show()
            self.main_win.frmCitizenship.show()
            self.main_win.frmHolidaySells.hide()

        elif tab in "TATİL SATIŞ HOLIDAY SELLINGS":
            if self.lang_flag == 0:
                self.main_win.lblProcesses.setText("TATİL SATIŞ")
            else:
                self.main_win.lblProcesses.setText("CITIZENSHIP PROCESSES")
            self.main_win.frmProcesses.show()
            self.main_win.frmVisa.hide()
            self.main_win.frmCitizenship.hide()
            self.main_win.frmHolidaySells.show()

        else:
            self.main_win.frmProcesses.hide()
            self.main_win.frmVisa.hide()

    def change_color(self, rb):
        if rb in self.radio_buttons[:3]:
            for i in self.radio_buttons[:3]:
                i.setStyleSheet("color: rgb(171, 157, 156);")
            rb.setStyleSheet("color: rgb(253, 3, 2);")
        else:
            for i in self.radio_buttons[3:]:
                i.setStyleSheet("color: rgb(171, 157, 156);")
            rb.setStyleSheet("color: rgb(253, 128, 28);")

    def show_all(self):
        print("Pressed to Show All.")

    def money(self):
        self.money_win.show()

    def remindings(self):
        self.remindings_win.show()

    def appointments(self):
        print("Pressed to Appointments.")

    def set_language(self):
        self.main_win.menuClients.setTitle("CLIENTS")
        self.main_win.menuDLD.setTitle("DOCUMENT LIST DEFINITION")
        self.main_win.menuUsers.setTitle("USERS")
        self.main_win.menuCurrency.setTitle("CURRENCY")
        self.main_win.menuAuthorities.setTitle("AUTHORITIES")
        self.main_win.menuExit.setTitle("EXIT")

        self.main_win.tbwProcesses.horizontalHeaderItem(1).setText("Date of Process")
        self.main_win.tbwProcesses.horizontalHeaderItem(2).setText("Date of File Entry")
        self.main_win.tbwProcesses.horizontalHeaderItem(3).setText("User")
        self.main_win.tbwProcesses.horizontalHeaderItem(4).setText("File Number")
        self.main_win.tbwProcesses.horizontalHeaderItem(5).setText("Process Kind")
        self.main_win.tbwProcesses.horizontalHeaderItem(6).setText("Process")
        self.main_win.tbwProcesses.horizontalHeaderItem(7).setText("Process Type")
        self.main_win.tbwProcesses.horizontalHeaderItem(8).setText("Type of Visa")
        self.main_win.tbwProcesses.horizontalHeaderItem(9).setText("User's Note")
        self.main_win.tbwProcesses.horizontalHeaderItem(10).setText("Voucher")
        self.main_win.tbwProcesses.horizontalHeaderItem(11).setText("Taken Note")
        self.main_win.tbwProcesses.horizontalHeaderItem(12).setText("Name")
        self.main_win.tbwProcesses.horizontalHeaderItem(13).setText("Surname")
        self.main_win.tbwProcesses.horizontalHeaderItem(14).setText("GSM")
        self.main_win.tbwProcesses.horizontalHeaderItem(15).setText("E-Mail")

        self.main_win.tbwTabs.item(0, 1).setText("CITIZENSHIP")
        self.main_win.tbwTabs.item(1, 1).setText("VISA")
        self.main_win.tbwTabs.item(2, 1).setText("BOOKING")
        self.main_win.tbwTabs.item(3, 1).setText("HOLIDAY SELLINGS")
        self.main_win.tbwTabs.item(4, 1).setText("VEHICLE INSURANCE")
        self.main_win.tbwTabs.item(5, 1).setText("TRANSLATION")
        self.main_win.tbwTabs.item(6, 1).setText("DIVERSITY")

        self.main_win.lblFirst.setText("First :")
        self.main_win.lblLast.setText("Last :")
        self.main_win.lblNumOfProcesses.setText("Number of Process Type = 0")
        self.main_win.btnDetailed.setText("Detailed Search")
        self.main_win.btnShowAll.setText("Show All")
        self.main_win.lblBranch.setText("Branch :")
        self.main_win.lblBranch_ADMIN.setText("Branch :")

        self.main_win.btnMoney.setText("Money Movements")
        self.main_win.btnRemindings.setText("Reminders")
        self.main_win.btnAppointments.setText("Bookings")

        self.main_win.rbInProcess.setText("In Process")
        self.main_win.rbProcessFinished.setText("Process Done But Not Handed Over")
        self.main_win.rbCouldNotReach.setText("Could Not Reach")
        self.main_win.rbThoseProcFinish.setText("Process Finished")
        self.main_win.rbAll.setText("All")

        self.main_win.lblSellType.setText("Selling Type:")

        self.main_win.rbBGVisa.setText("BG VISA")
        self.main_win.rbDVisa.setText("D VISA")

        self.lang_flag = 1
        self.users_win.set_language()
