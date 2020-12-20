from PyQt5 import QtPrintSupport
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter

from demirbas_hakkinda import hakkinda
from demirbas_urunekle import *
from kisiler_dialog import *
from kategori_dialog import *
from demirbas_detay_gui import *
from shutil import *
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon/dmr_cube.png'))

        self.setWindowTitle("Demirbaş Yönetim Sistemi")
        self.setMinimumSize(950, 500)

        self.arama = QLineEdit()

        self.arama.textChanged.connect(self.onTextChange)

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
        self.tableWidget.itemSelectionChanged.connect(self.onTableChange)

        self.arama_label = QLabel("ARA")
        self.arama_label.setFixedWidth(50)

        self.yatay = QHBoxLayout()
        self.dikey = QVBoxLayout()
        self.yatay2 = QHBoxLayout()

        self.yatay.addWidget(self.arama_label)
        self.yatay.addWidget(self.arama)

        self.dikey.addLayout(self.yatay)
        self.dikey.addWidget(self.tableWidget)

        self.demirbas_dt = demirbas_detay()
        self.detay_widget = QWidget()
        self.detay_widget.setLayout(self.demirbas_dt)
        self.detay_widget.setFixedWidth(300)

        self.yatay2.addLayout(self.dikey)
        self.yatay2.addWidget(self.detay_widget)
        self.detay_widget = QWidget()

        self.widget = QWidget(self)
        self.widget.setLayout(self.yatay2)
        self.setCentralWidget(self.widget)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(32, 32))
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

        btn_kisi_ekle = QAction(QIcon("icon/customer.png"), "Kişi Ekle", self)  # add student icon
        btn_kisi_ekle.triggered.connect(self.kisiekle)
        btn_kisi_ekle.setStatusTip("Kişiler")
        toolbar.addAction(btn_kisi_ekle)

        btn_kategori_ekle = QAction(QIcon("icon/catalog.png"), "Kategori", self)  # search icon
        btn_kategori_ekle.triggered.connect(self.kategori)
        btn_kategori_ekle.setStatusTip("Kategoriler")
        toolbar.addAction(btn_kategori_ekle)

        btn_demirbas_sil = QAction(QIcon("icon/dmr_sil1.png"), "Sil", self)
        btn_demirbas_sil.triggered.connect(self.delete)
        btn_demirbas_sil.setStatusTip("Demirbaş Sil")
        toolbar.addAction(btn_demirbas_sil)
        ####################################################################
        #             M E N U     T A N I M L A M A L A R I                #
        ####################################################################
        menu_dosya = self.menuBar().addMenu("Dosya")
        menu_demirbas = self.menuBar().addMenu("Demirbaş")
        menu_kisiler = self.menuBar().addMenu("Kişiler")
        menu_kategori = self.menuBar().addMenu("Kategori")
        menu_yardim = self.menuBar().addMenu("Yardım")

        backup_action = QAction(QIcon("icon/backup.png"), "Yedek Ver", self)
        backup_action.triggered.connect(self.dosya_kaydet)
        menu_dosya.addAction(backup_action)

        restore_action = QAction(QIcon("icon/restore.png"), "Yedekten Yükle", self)
        restore_action.triggered.connect(self.yedek_al)
        menu_dosya.addAction(restore_action)
        menu_dosya.addSeparator()

        print_action_pre = QAction(QIcon("icon/loupe.png"), "Yazdırma Önizleme", self)
        print_action_pre.triggered.connect(self.yazdir_onizleme)
        print_action_pre.setShortcut("Ctrl+R")
        menu_dosya.addAction(print_action_pre)

        print_action = QAction(QIcon("icon/printer.png"), "Yazdır", self)
        print_action.triggered.connect(self.yazdir)
        print_action.setShortcut("Ctrl+P")
        menu_dosya.addAction(print_action)
        menu_dosya.addSeparator()

        cikis_action = QAction(QIcon("icon/logout.png"), "Çıkış", self)
        cikis_action.triggered.connect(self.cikis)
        cikis_action.setShortcut("Ctrl+Q")
        menu_dosya.addAction(cikis_action)

        demirbas_ekle_action = QAction(QIcon("icon/dmr_ekle.png"), "Demirbaş Ekle", self)
        demirbas_ekle_action.triggered.connect(self.demirbasekle)
        demirbas_ekle_action.setShortcut("Ctrl+A")
        menu_demirbas.addAction(demirbas_ekle_action)

        demirbas_duzenle_action = QAction(QIcon("icon/dmr_duzenle2.png"), "Demirbaş Düzenle", self)
        demirbas_duzenle_action.triggered.connect(self.demirbasduzenle)
        demirbas_duzenle_action.setShortcut("Ctrl+E")
        menu_demirbas.addAction(demirbas_duzenle_action)

        demirbas_sil_action = QAction(QIcon("icon/dmr_sil2.png"), "Demirbaş Sil", self)
        demirbas_sil_action.triggered.connect(self.delete)
        demirbas_sil_action.setShortcut("Ctrl+D")
        menu_demirbas.addAction(demirbas_sil_action)

        kisi_action = QAction(QIcon("icon/customer.png"), "Kişiler", self)
        kisi_action.triggered.connect(self.kisiekle)
        kisi_action.setShortcut("Ctrl+K")
        menu_kisiler.addAction(kisi_action)

        kat_action = QAction(QIcon("icon/catalog.png"), "Kategoriler", self)
        kat_action.triggered.connect(self.kategori)
        kat_action.setShortcut("Ctrl+T")
        menu_kategori.addAction(kat_action)

        yardim_action = QAction(QIcon("icon/question.png"), "Yardım", self)
        yardim_action.triggered.connect(self.bos)
        yardim_action.setShortcut("Ctrl+H")
        menu_yardim.addAction(yardim_action)

        hakkinda_action = QAction(QIcon("icon/about.png"), "Hakkında", self)
        hakkinda_action.triggered.connect(self.hakk_goster)
        hakkinda_action.setShortcut("Ctrl+W")
        menu_yardim.addAction(hakkinda_action)

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        self.liste = []
        self.liste_hazirla()

        self.dindex = None

    def model_olustur(self):
        document = QTextDocument()
        if len(self.liste) > 0:
            cursor = QTextCursor(document)
            model = self.liste.copy()
            lst = ["ID", "Demirbaş No", "Ürün Adı", "İşlem Tarihi", "Teslim Alan", "Kategori", "Ürün Adeti", "Marka",
                   "Model", "Seri No", "Garanti Süresi", "Satın Alınma Tarihi", "Bulunduğu Yer", "Açıklama"]

            model.insert(0, lst)
            styl = QTextTableFormat()
            styl.setCellPadding(5)
            styl.setCellSpacing(0)

            table = cursor.insertTable(len(model), len(model[0]), styl)
            for r in range(table.rows()):
                for c in range(table.columns()):
                    cursor.insertText(str(model[r][c]))
                    cursor.movePosition(QTextCursor.NextCell)
        return document

    def yazdir(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            doc = self.model_olustur()
            dialog.printer().setPageMargins(5, 5, 5, 5, QPrinter.Millimeter)
            doc.print_(dialog.printer())

    def yazdir_onizleme(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.printer().setPageMargins(5, 5, 5, 5, QPrinter.Millimeter)
        doc = self.model_olustur()
        dialog.paintRequested.connect(doc.print_)
        dialog.exec_()

    def veriyukle(self):
        result = self.liste
        self.tableWidget.clearSelection()
        self.tableWidget.setRowCount(0)
        self.dindex = None
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            self.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(row_data[2])))
            self.tableWidget.setItem(row_number, 3, QTableWidgetItem(str(row_data[3])))
            self.tableWidget.setItem(row_number, 4, QTableWidgetItem(str(row_data[4])))
            self.tableWidget.setItem(row_number, 5, QTableWidgetItem(str(row_data[5])))

    def delete(self):
        if self.dindex != None:
            ind = self.dindex
            if ind > -1:
                res = QMessageBox.question(self, "Onay", "Kaydı silmeyi onaylıyor musunuz?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if res == QMessageBox.Yes:
                    ind = self.tableWidget.currentRow()
                    ind = int(self.tableWidget.item(ind, 0).text())
                    db = db_helper()
                    db.demirbas_sil(ind)
                    self.liste_hazirla()
                    self.veriyukle()

    def kategori(self):
        katekr = kategori_ekr(self)
        result = katekr.exec()
        self.liste_hazirla()
        self.veriyukle()

    def demirbasekle(self):
        urunekle_ekran = urunekle(self)
        result = urunekle_ekran.exec()
        if result == QDialog.Accepted:
            self.liste_hazirla()
            self.veriyukle()

    def demirbasduzenle(self):
        if self.dindex != None:
            ind = self.dindex
            urunekle_ekran = urunekle(self, ind)
            result = urunekle_ekran.exec()
            print(result)
            self.liste_hazirla()
            self.veriyukle()
        else:
            QMessageBox.information(self, "UYARI", "Lütfen bir kayıt seçiniz.")

    def kisiekle(self):
        kisiekr = kisiler_ekr(self)
        result = kisiekr.exec()
        self.liste_hazirla()
        self.veriyukle()

    def liste_hazirla(self):
        self.tableWidget.clearSelection()
        self.arama.setText("")
        db = db_helper()
        demirbas_liste = db.demirbas_liste()
        lst = []
        for d in demirbas_liste:
            tlst = []
            tlst.append(d[0])
            tlst.append(d[1])
            tlst.append(d[2])
            tlst.append(db.kisi(d[3])[1])
            tlst.append(d[4])
            if d[5] > -1:
                tlst.append(db.kategori(d[5])[1])
            else:
                tlst.append("Kategorisiz")
            tlst.append(d[6])
            tlst.append(d[7])
            tlst.append(d[8])
            tlst.append(d[9])
            tlst.append(d[10])
            tlst.append(d[11])
            tlst.append(d[12])
            tlst.append(d[13])
            lst.append(tlst)
        self.liste = lst

    def fa(self, s1, s2):
        if s1 in s2:
            return True
        else:
            return False

    def filtre(self, ar):
        lst = []
        for r in self.liste:
            for k in r:
                if self.fa(ar, str(k)):
                    lst.append(r)
                    break
        self.liste = lst

    def onTextChange(self, e):
        self.tableWidget.clearSelection()
        if len(e) > 0:
            self.filtre(e)
        else:
            self.liste_hazirla()
        self.veriyukle()

    def onTableChange(self):
        ind = self.tableWidget.currentRow()
        ind = int(self.tableWidget.item(ind, 0).text())
        self.dindex = ind
        for r in self.liste:
            if r[0] == self.dindex:
                self.demirbas_dt.veri_yukle(r)

    def dosya_kaydet(self):
        dizin = QFileDialog.getExistingDirectory()
        if not dizin:
            return
        else:
            if os.path.isdir(dizin):
                try:
                    kaynak = os.path.curdir + "/demirbas.db"
                    hedef = dizin + "/demirbas.db"
                    if os.path.exists(hedef):
                        sonuc = QMessageBox.question(self, "Onay", "Belirtilen yerde dosya var. Üstüne yazılsın mı?",
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if sonuc == QMessageBox.Yes:
                            copyfile(kaynak, hedef)
                        else:
                            return
                except:
                    QMessageBox.warning(self, "Hata", "Dosya kopyalanamadı")

    def yedek_al(self):
        fd = QFileDialog()
        dosya = QFileDialog.getOpenFileName(fd, "Dosya seç", "C:\\", "DB dosyaları (*.db)")
        sonuc = QMessageBox.question(self, "Onay",
                                     "Yedekten dosya yüklenecek. Tüm kayıtlarınız kaybolabilir. Yedekten vei yüklemek istiyor musunuz?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if sonuc == QMessageBox.Yes:
            kaynak = dosya[0]
            hedef = os.path.curdir + "/demirbas.db"
            try:
                copyfile(kaynak, hedef)
            except:
                QMessageBox.warning(self, "Hata", "Dosya yüklenemedi")
        self.liste_hazirla()
        self.veriyukle()

    def bos(self):
        os.startfile("yardim.pdf")

    def cikis(self):
        app.exit(0)

    def hakk_goster(self):
        hk = hakkinda(self)
        hk.exec()


app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    window = MainWindow()
    window.show()
    window.veriyukle()
sys.exit(app.exec_())
