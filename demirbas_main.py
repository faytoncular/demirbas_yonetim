
from PyQt5.QtGui import *

from demirbas_urunekle import *
from kisiler_dialog import *
from kategori_dialog import *
import sys



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon/dmr_cube.png'))

        self.setWindowTitle("Demirbaş Yönetim Sistemi")
        self.setMinimumSize(700, 500)

        self.arama = QLineEdit()

        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setHorizontalHeaderLabels(("id", "Demirbaş No", "Ad", "Teslim Alan", "Tarih", "Kategori"))

        self.arama_label = QLabel("ARA")
        self.arama_label.setFixedWidth(50)

        self.yatay = QHBoxLayout()
        self.dikey = QVBoxLayout()

        self.yatay.addWidget(self.arama_label)
        self.yatay.addWidget(self.arama)

        self.dikey.addLayout(self.yatay)
        self.dikey.addWidget(self.tableWidget)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        self.statusBar().showMessage("497_10_FAYTONCULAR:Hasan Özçetin, İsmail Gövercin, Selahattin Çekcen")

        btn_demirbas_ekle = QAction(QIcon("icon/dmr_ekle.png"), "Demirbaş Ekle", self)
        btn_demirbas_ekle.triggered.connect(self.demirbasekle)
        btn_demirbas_ekle.setStatusTip("Demirbaş Ekle")
        toolbar.addAction(btn_demirbas_ekle)

        btn_demirbas_duzenle = QAction(QIcon("icon/dmr_duzenle2.png"), "Demirbaş Düzenle", self)
        btn_demirbas_duzenle.triggered.connect(self.demirbasduzenle)
        btn_demirbas_duzenle.setStatusTip("Demirbaş Düzenle")
        toolbar.addAction(btn_demirbas_duzenle)

        btn_kisi_ekle = QAction(QIcon("icon/dmr_kisi.png"), "Kişi Ekle", self)  # add student icon
        btn_kisi_ekle.triggered.connect(self.kisiekle)
        btn_kisi_ekle.setStatusTip("Kişiler")
        toolbar.addAction(btn_kisi_ekle)

        btn_kategori_ekle = QAction(QIcon("icon/dmr_nesne.png"), "Kategori", self)  # search icon
        btn_kategori_ekle.triggered.connect(self.kategori)
        btn_kategori_ekle.setStatusTip("Kategoriler")
        toolbar.addAction(btn_kategori_ekle)

        btn_demirbas_sil = QAction(QIcon("icon/dmr_sil1.png"), "Sil", self)
        btn_demirbas_sil.triggered.connect(self.delete)
        btn_demirbas_sil.setStatusTip("Demirbaş Sil")
        toolbar.addAction(btn_demirbas_sil)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.dikey)

    def veriyukle(self):
        db = db_helper()
        result = db.demirbas_liste()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            self.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(row_data[2])))
            kisi = db.kisi(row_data[3])
            self.tableWidget.setItem(row_number, 3, QTableWidgetItem(kisi[1]))
            self.tableWidget.setItem(row_number, 4, QTableWidgetItem(str(row_data[4])))

            if row_data[5] == -1:
                kat = "Kategorisiz"
            else:
                kat = db.kategori(row_data[5])[1]
            self.tableWidget.setItem(row_number, 5, QTableWidgetItem(kat))

    def delete(self):
        ind = self.tableWidget.currentRow()
        if ind > -1:
            res = QMessageBox.question(self, "Onay", "Kaydı silmeyi onaylıyor musunuz?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if res == QMessageBox.Yes:
                ind = self.tableWidget.currentRow()
                ind = int(self.tableWidget.item(ind, 0).text())
                db = db_helper()
                db.demirbas_sil(ind)
                self.veriyukle()

    def kategori(self):
        katekr = kategori_ekr(self)
        result = katekr.exec()
        print(result)

    def about(self):
        pass

    def demirbasekle(self):
        urunekle_ekran = urunekle(self)
        result = urunekle_ekran.exec()
        if result == QDialog.Accepted:
            self.veriyukle()

    def demirbasduzenle(self):
        ind = self.tableWidget.currentRow()
        ind = int(self.tableWidget.item(ind, 0).text())
        urunekle_ekran = urunekle(self, ind)
        result = urunekle_ekran.exec()
        if result == QDialog.Accepted:
            self.veriyukle()

    def kisiekle(self):
        kisiekr = kisiler_ekr(self)
        result = kisiekr.exec()
        print(result)


app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = MainWindow()
    window.show()
    window.veriyukle()
sys.exit(app.exec_())
