from PyQt5.QtWidgets import *
from demirbas_db import *
from datetime import *


class kisiler_ekr(QDialog):
    def __init__(self, parent, dindex=None, p=None):
        super(kisiler_ekr, self).__init__(parent)
        self.dindex = dindex
        self.db = db_helper()
        self.kisiler_liste = self.db.kisiler_aktif()

        if dindex != None:
            self.ksl = self.db.kisi(dindex)

        self.p = p

        self.setWindowTitle("Teslim Alacak Kişiler")

        self.tablelayout = QGridLayout()

        self.ad_label = QLabel("Ad")
        self.gorevi_label = QLabel("Görevi")

        self.ad = QLineEdit()
        self.gorevi = QLineEdit()

        self.tablelayout.addWidget(self.ad_label, 0, 0)
        self.tablelayout.addWidget(self.ad, 0, 1)
        self.tablelayout.addWidget(self.gorevi_label, 1, 0)
        self.tablelayout.addWidget(self.gorevi, 1, 1)

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()

        self.btn_yeni = QPushButton("YENİ")
        self.btn_kaydet = QPushButton("KAYDET")
        self.btn_sil = QPushButton("SİL")

        self.btn_yeni.clicked.connect(self.yeni_kayit)
        self.btn_kaydet.clicked.connect(self.kaydet)
        self.btn_sil.clicked.connect(self.sil)

        yatay.addWidget(self.btn_yeni)
        yatay.addWidget(self.btn_kaydet)
        yatay.addWidget(self.btn_sil)
        widg = QWidget()
        widg.setLayout(yatay)
        self.tablelayout.addWidget(widg, 2, 1)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)

        self.tableWidget.setHorizontalHeaderLabels(("id", "Ad", "Görevi"))
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.itemSelectionChanged.connect(self.table_change)

        self.arama_txt = QLineEdit()
        self.arama_txt.textChanged.connect(self.onTextChange)
        self.arama_txt.setFixedHeight(30)
        dikey.addLayout(self.tablelayout)
        dikey.addWidget(self.arama_txt)
        dikey.addWidget(self.tableWidget)

        self.setLayout(dikey)

        self.veriyukle()
        self.setMinimumWidth(450)

    def veriyukle(self):
        result = self.kisiler_liste
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            self.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(row_data[3])))

    def table_change(self):
        ind = self.tableWidget.currentRow()
        ind = int(self.tableWidget.item(ind, 0).text())
        kisi = self.db.kisi(ind)
        self.form_yukle(kisi)
        self.dindex = ind
        print(ind)

    def form_yukle(self, kisi):
        self.ad.setText(kisi[1])
        self.gorevi.setText(kisi[3])

    def yeni_kayit(self):
        self.ad.setText("")
        self.gorevi.setText("")
        self.dindex = None
        self.tableWidget.clearSelection()

    def kaydet(self):
        ad = self.ad.text().strip()
        gorevi = self.gorevi.text().strip()
        if len(ad) > 0 and len(gorevi) > 0:
            lst = []
            lst.append(ad)
            lst.append(gorevi)
            if self.dindex != None:
                self.db.kisi_duzenle(lst, self.dindex)
            else:
                self.db.kisi_ekle(lst)
                if self.p != None:
                    self.done(QDialog.Accepted)
                else:
                    self.tableWidget.clearSelection()
                    self.kisiler_liste = self.db.kisiler_aktif()
                    self.veriyukle()
        else:
            QMessageBox.information(self, "Hata", "Lütfen bilgileri tam giriniz!")

    def sil(self):
        ind = self.tableWidget.currentRow()
        if ind > -1:
            res = QMessageBox.question(self, "Onay", "Kaydı silmeyi onaylıyor musunuz?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if res == QMessageBox.Yes:
                ind = self.tableWidget.currentRow()
                ind = int(self.tableWidget.item(ind, 0).text())
                self.db.kisi_sil(ind)
                self.tableWidget.clearSelection()
                self.kisiler_liste = self.db.kisiler_aktif()
                self.veriyukle()
        else:
            QMessageBox.information(self, "Hata", "Bir kayıt seçiniz!")

    def onTableWidgetClearSelection(self):
        if self.tableWidget.currentRow() > 0:
            self.tableWidget.clearSelection()

    def fa(self, s1, s2):
        if s1 in s2:
            return True
        else:
            return False

    def filtre(self, ar):
        lst = []
        for r in self.kisiler_liste:
            print(r)
            for k in r:
                if self.fa(str(ar).casefold(), str(k).casefold()):
                    lst.append(r)
                    break
        self.kisiler_liste = lst

    def onTextChange(self, e):
        self.tableWidget.clearSelection()
        if len(e) > 1:
            self.filtre(e)
        else:
            self.kisiler_liste = self.db.kisiler_aktif()
        self.veriyukle()
