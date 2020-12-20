from PyQt5.QtWidgets import *
from demirbas_db import *
from datetime import *


class kategori_ekr(QDialog):
    def __init__(self, parent, dindex=None, p=None):
        super(kategori_ekr, self).__init__(parent)
        self.dindex = dindex
        self.db = db_helper()
        self.kategori_liste = self.db.kategori_liste()

        self.p = p

        if dindex != None:
            self.kat = self.db.kategori(dindex)

        self.setWindowTitle("Kategori Düzenleme")

        self.tablelayout = QGridLayout()

        self.ad_label = QLabel("Kategori Adı")
        self.aciklama_label = QLabel("Açıklama")

        self.ad = QLineEdit()
        self.aciklama = QTextEdit()

        self.tablelayout.addWidget(self.ad_label, 0, 0)
        self.tablelayout.addWidget(self.ad, 0, 1)
        self.tablelayout.addWidget(self.aciklama_label, 1, 0)
        self.tablelayout.addWidget(self.aciklama, 1, 1)

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

        self.tableWidget.setHorizontalHeaderLabels(("id", "Kategori", "Açıklama"))
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
        result = self.kategori_liste
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            self.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(row_data[2])))

    def table_change(self):
        ind = self.tableWidget.currentRow()
        ind = int(self.tableWidget.item(ind, 0).text())
        kat = self.db.kategori(ind)
        self.form_yukle(kat)
        self.dindex = ind

    def form_yukle(self, kat):
        self.ad.setText(kat[1])
        self.aciklama.setText(kat[2])

    def yeni_kayit(self):
        self.ad.clear()
        self.aciklama.clear()
        self.arama_txt.clear()
        self.kategori_liste = self.db.kategori_liste()
        self.dindex = None
        self.tableWidget.clearSelection()

    def kaydet(self):
        ad = self.ad.text().strip()
        aciklama = self.aciklama.toPlainText().strip()
        if len(ad) > 0 and len(aciklama) > 0:
            lst = []
            lst.append(ad)
            lst.append(aciklama)
            if self.dindex != None:
                self.db.kategori_duzenle(lst, self.dindex)
            else:
                self.db.kategori_ekle(lst)
            if self.p != None:
                self.done(QDialog.Accepted)
            else:
                self.tableWidget.clearSelection()
                self.yeni_kayit()
                self.veriyukle()
        else:
            QMessageBox.information(self, "Hata", "Lütfen bilgileri tam giriniz!")

    def sil(self):
        self.tableWidget.clearSelection()
        if self.dindex != None:
            res = QMessageBox.question(self, "Onay", "Kaydı silmeyi onaylıyor musunuz?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if res == QMessageBox.Yes:
                self.db.kategori_sil(self.dindex)

                self.yeni_kayit()
                self.veriyukle()
        else:
            QMessageBox.information(self, "Hata", "Bir kayıt seçiniz!")
    def fa(self, s1, s2):
        if s1 in s2:
            return True
        else:
            return False

    def filtre(self, ar):
        lst = []
        for r in self.kategori_liste:
            for k in r:
                if self.fa(ar, str(k)):
                    lst.append(r)
                    break
        self.kategori_liste = lst

    def onTextChange(self, e):
        self.tableWidget.clearSelection()
        if len(e) > 1:
            self.filtre(e)
        else:
            self.kategori_liste = self.db.kategori_liste()
        self.veriyukle()
