from PyQt5.QtWidgets import QWidget, QRadioButton, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui
from Designs.Clients_Ui import Ui_winClients
from Codes import Client_Entry_Code, Find_Client_Code, Tree_Code, Holiday_Sellings_Code
from Common_Codes import Common
from datetime import datetime


class Clients(QWidget):
    def __init__(self):
        super().__init__()
        self.clients_win = Ui_winClients()
        self.clients_win.setupUi(self)

        self.client_entry_win = Client_Entry_Code.ClientEntry()
        self.find_client_win = Find_Client_Code.FindClient()
        self.tree_win = Tree_Code.Tree()
        self.holiday_sellings_win = Holiday_Sellings_Code.HolidaySellings()
        self.common = Common()
        self.clients_win.tbwMusteriler.setColumnHidden(0, True)  # id
        self.clients_win.tbwMusteriler.setColumnWidth(1, 40)
        self.clients_win.tbwMusteriler.setColumnWidth(2, 80)
        self.clients_win.tbwMusteriler.setColumnWidth(3, 90)
        self.clients_win.tbwMusteriler.setColumnWidth(4, 110)
        self.clients_win.tbwMusteriler.setColumnWidth(5, 130)
        self.clients_win.tbwMusteriler.setColumnWidth(6, 130)
        self.clients_win.tbwMusteriler.setColumnWidth(7, 240)
        self.clients_win.tbwMusteriler.setColumnWidth(8, 250)
        self.clients_win.tbwMusteriler.setColumnWidth(9, 110)
        self.clients_win.tbwMusteriler.setColumnWidth(10, 110)
        self.clients_win.tbwMusteriler.setColumnWidth(11, 130)
        self.clients_win.tbwMusteriler.setColumnWidth(12, 135)
        self.clients_win.tbwMusteriler.setColumnWidth(13, 110)
        self.clients_win.tbwMusteriler.setColumnWidth(14, 130)

        self.clients_win.tbwIslemTuru.setColumnWidth(1, 239)
        self.clients_win.tbwIslemTuru.clicked.connect(self.agac)

        self.clients_win.tbwIslemTuru.setColumnHidden(0, True)

        self.clients_win.tbwHareketler.setColumnHidden(0, True)
        self.clients_win.tbwHareketler.setColumnHidden(5, True)
        self.clients_win.tbwHareketler.setColumnHidden(6, True)
        self.clients_win.tbwHareketler.setColumnHidden(7, True)


        self.clients_win.btnMusteriEkle.clicked.connect(self.ekle)
        self.clients_win.tbwMusteriler.currentCellChanged.connect(lambda x, : self.bilgileri(self.clients_win.tbwMusteriler.currentRow()))
        self.clients_win.btnMusteriDegistir.clicked.connect(self.degistir)
        self.clients_win.btnMusteriSil.clicked.connect(self.sil)
        self.clients_win.btnMusteriBul.clicked.connect(self.bul)

    def islem_turleri(self):
        self.kullanici = self.common.fetch_user()
        islemler_querry = "SELECT * FROM islem_turleri;"
        islem_turleri = self.common.server(islemler_querry, "all")
        self.clients_win.tbwIslemTuru.setRowCount(len(islem_turleri))
        for i in range(len(islem_turleri)):
            self.clients_win.tbwIslemTuru.setItem(i, 0, QTableWidgetItem(str(islem_turleri[i]["ID"])))
            item = self.clients_win.tbwIslemTuru.item(i, 1)
            item.setText(str(islem_turleri[i]["ISLEM_TURU"]))

    def agac(self):
        try:
            islem_turu_id = self.clients_win.tbwIslemTuru.item(self.clients_win.tbwIslemTuru.currentRow(), 0).text()
            if islem_turu_id in "12367":
                self.tree_win.agac_cek(islem_turu_id, self.musteri_id, self.musteri_adi, self.musteri_gsm)
                self.tree_win.setModal(True)
                self.tree_win.exec_()
                self.bilgileri(self.clients_win.tbwMusteriler.currentRow())
            elif islem_turu_id == "4":
                self.holiday_sellings_win.setModal(True)
                self.holiday_sellings_win.exec_()
        except:
            QMessageBox.information(self, "Dikkat!", "Önce müşteri seçiniz.")

    def max_id_al(self):
        max_query = "SELECT MAX(ID) AS MAX_ID FROM musteriler"
        return self.common.server(max_query, "all")[0]["MAX_ID"]

    def ekle(self):
        self.client_entry_win.who(self.kullanici["ID"])
        oldmax = self.max_id_al()
        self.client_entry_win.ekle_pen()
        self.client_entry_win.setModal(True)
        self.client_entry_win.exec_()
        newmax = self.max_id_al()
        if oldmax != newmax:
            self.musteri_listele()

    def degistir(self):
        self.client_entry_win.who(self.kullanici["ID"])
        id_ = self.clients_win.tbwMusteriler.item(self.clients_win.tbwMusteriler.currentRow(), 0).text()
        self.client_entry_win.degistir_pen(int(id_), 0)
        self.client_entry_win.setModal(True)
        self.client_entry_win.exec_()
        eger = self.client_entry_win.read()
        if eger == 1:
            self.musteri_listele()
            self.satir_bul(id_)

    def secildi(self, row):
        self.musteri_id = self.clients_win.tbwMusteriler.item(row, 0).text()
        self.musteri_adi = self.clients_win.txtAdiSoyadi.text()
        self.musteri_gsm = self.clients_win.txtGSMNo.text()
        
    def musteri_listele(self):
        self.kullanici = self.common.fetch_user()
        self.musteri_cek_query = f"SELECT * FROM view_musteriler WHERE SILINDI = 0 AND SUBE_ID = {self.kullanici['SUBE_ID']} ORDER BY ADI, SOYADI;"
        self.musteri_rowlari = self.common.server(self.musteri_cek_query, "all")
        self.clients_win.tbwMusteriler.setRowCount(len(self.musteri_rowlari))
        for i in range(len(self.musteri_rowlari)):
            self.clients_win.tbwMusteriler.setItem(i, 0, QTableWidgetItem(str(self.musteri_rowlari[i]["ID"])))
            x = QRadioButton()
            x.clicked.connect(lambda state, row=i: self.secildi(row))
            self.clients_win.tbwMusteriler.setCellWidget(i, 1, x)

            adi = self.common.make_title(self.musteri_rowlari[i]["ADI"])
            soyadi = self.common.make_title(self.musteri_rowlari[i]["SOYADI"])
            adresi = self.common.make_title(self.musteri_rowlari[i]["ADRES"])
            diger1 = self.common.make_title(self.musteri_rowlari[i]["DIGER_AD1"])
            diger2 = self.common.make_title(self.musteri_rowlari[i]["DIGER_AD2"])
            self.clients_win.tbwMusteriler.setItem(i, 2, QTableWidgetItem(str(self.musteri_rowlari[i]["GORUNEN_AD"])))
            self.clients_win.tbwMusteriler.setItem(i, 3, QTableWidgetItem(adi.replace("´", "'")))
            self.clients_win.tbwMusteriler.setItem(i, 4, QTableWidgetItem(soyadi.replace("´", "'")))
            self.clients_win.tbwMusteriler.setItem(i, 5, QTableWidgetItem(str(self.musteri_rowlari[i]["GSM"])))
            self.clients_win.tbwMusteriler.setItem(i, 6, QTableWidgetItem(str(self.musteri_rowlari[i]["TEL"])))
            self.clients_win.tbwMusteriler.setItem(i, 7, QTableWidgetItem(str(self.musteri_rowlari[i]["E_MAIL"]).replace("´", "'")))
            self.clients_win.tbwMusteriler.setItem(i, 8, QTableWidgetItem(adresi.replace("´", "'")))
            self.clients_win.tbwMusteriler.setItem(i, 9, QTableWidgetItem(diger1.replace("´", "'")))
            self.clients_win.tbwMusteriler.setItem(i, 10, QTableWidgetItem(str(diger2.replace("´", "'"))))
            self.clients_win.tbwMusteriler.setItem(i, 11, QTableWidgetItem(str(self.musteri_rowlari[i]["TC_KIMLIK"])))
            self.clients_win.tbwMusteriler.setItem(i, 12, QTableWidgetItem(str(self.musteri_rowlari[i]["PASAPORT_NO"])))
            self.clients_win.tbwMusteriler.setItem(i, 13, QTableWidgetItem(self.common.date_format(str(self.musteri_rowlari[i]["KAYIT_TAR"]).split("-"))))
            dt = str(self.musteri_rowlari[i]["DOG_TAR"])
            if dt != "None":
                self.clients_win.tbwMusteriler.setItem(i, 14, QTableWidgetItem(self.common.date_format(dt.split("-"))))

        self.clients_win.lblMusteriler.setText(f"MÜŞTERİLER = {len(self.musteri_rowlari)}")
        self.hareket_tablosu(f"SELECT * FROM view_hareketler WHERE SILINDI = 0")

    def bilgileri(self, row):
        self.clients_win.txtIslemTakipcisi.setText(self.musteri_rowlari[row]["takipci_ADI_SOYADI"])
        adi_soyadi = f"{self.clients_win.tbwMusteriler.item(row, 3).text()} " \
                     f"{self.clients_win.tbwMusteriler.item(row, 4).text()}"
        self.clients_win.txtAdiSoyadi.setText(adi_soyadi)
        self.clients_win.txtGSMNo.setText(self.clients_win.tbwMusteriler.item(row, 5).text())
        self.clients_win.txtSabitTelefon.setText(self.clients_win.tbwMusteriler.item(row, 6).text())
        self.clients_win.txtEPosta.setText(self.clients_win.tbwMusteriler.item(row, 7).text())
        self.clients_win.txtAdresi.setText(self.clients_win.tbwMusteriler.item(row, 8).text())
        self.clients_win.txtDigerAd1.setText(self.clients_win.tbwMusteriler.item(row, 9).text())
        self.clients_win.txtDigerAd2.setText(self.clients_win.tbwMusteriler.item(row, 10).text())
        self.clients_win.txtTC.setText(self.clients_win.tbwMusteriler.item(row, 11).text())
        self.clients_win.txtPasaportNo.setText(self.clients_win.tbwMusteriler.item(row, 12).text())
        self.hareket_tablosu(f"SELECT * FROM view_hareketler WHERE SILINDI = 0 AND MUSTERI_ID = {self.musteri_rowlari[row]['ID']}")

    def hareket_tablosu(self, hareket_query):
        hareket = self.common.server(hareket_query, "all")
        self.clients_win.tbwHareketler.setRowCount(len(hareket))
        for i in range(len(hareket)):
            self.clients_win.tbwHareketler.setItem(i, 0, QTableWidgetItem(str(hareket[i]['ID'])))
            if hareket[i]["DOSYA_KAYIT_TAR"] is not None:
                dkt = str(hareket[i]["DOSYA_KAYIT_TAR"]).split("-")
                dosya_kayit_tar = f"{dkt[2]}.{dkt[1]}.{dkt[0]}"
            else:
                dosya_kayit_tar = ""
            self.clients_win.tbwHareketler.setItem(i, 1, QTableWidgetItem(dosya_kayit_tar))
            self.clients_win.tbwHareketler.setItem(i, 2, QTableWidgetItem(str(hareket[i]['ISLEM_TURU'])))
            self.clients_win.tbwHareketler.setItem(i, 3, QTableWidgetItem(str(hareket[i]['ISLEM_TIPI'])))
            self.clients_win.tbwHareketler.setItem(i, 4, QTableWidgetItem(str(hareket[i]['ISLEM'])))
            self.clients_win.tbwHareketler.setItem(i, 5, QTableWidgetItem(str(hareket[i]['MUSTERI_ID'])))
            self.clients_win.tbwHareketler.setItem(i, 6, QTableWidgetItem(str(hareket[i]['ISLEM_TURU_ID'])))
            self.clients_win.tbwHareketler.setItem(i, 7, QTableWidgetItem(str(hareket[i]['ISLEM_TIPI_ID'])))

    def sil(self):
        try:
            mesaj = QMessageBox()
            mesaj.setWindowTitle("Uyarı!")
            mesaj.setText("Bu müşteriyi silmek istediğinizden emin misiniz?")
            mesaj.setIcon(QMessageBox.Warning)
            mesaj.setWindowIcon(QtGui.QIcon.fromTheme("C:/Users/baris/Desktop/Projects/Balkan_Travel_Py/Icons/balkan-travel-logo.ico"))
            mesaj.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            mesaj.button(QMessageBox.Yes).setText("Evet")
            mesaj.button(QMessageBox.No).setText("Hayır")
            emin = mesaj.exec_()
            if emin == QMessageBox.Yes:
                id_ = self.clients_win.tbwMusteriler.item(self.clients_win.tbwMusteriler.currentRow(), 0).text()
                silindigi_tar = str(datetime.now().date())
                kullanici_id = self.kullanici["ID"]
                sil_query = f"UPDATE musteriler SET SILINDI = 1, SILEN_KULLANICI_ID = '{kullanici_id}'," \
                            f"SILINDIGI_TAR = '{silindigi_tar}' WHERE ID = {id_}"
                self.common.server(sil_query, "commit")
                self.musteri_listele()
        except:
            QMessageBox.information(self, "Uyarı!", "Hiçbir müşteri seçili değil.")

    def satir_bul(self, xID):
        items = self.clients_win.tbwMusteriler.findItems(str(xID), QtCore.Qt.MatchExactly)
        if items:
            item = items[0]
            row = item.row()
            self.clients_win.tbwMusteriler.setCurrentCell(row, 0)

    def bul(self):
        self.find_client_win.bulucu()
        self.find_client_win.setModal(True)
        self.find_client_win.showMaximized()
        self.find_client_win.exec_()
        try:
            musteri_id = self.find_client_win.hareket_doldur()
            self.satir_bul(musteri_id)
        except:
            pass
