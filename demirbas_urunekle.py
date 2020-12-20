from PyQt5.QtWidgets import *
from demirbas_db import *
from datetime import *

from demirbas_detay_gui import demirbas_detay
from kategori_dialog import kategori_ekr
from kisiler_dialog import kisiler_ekr


class urunekle(QDialog):
    def __init__(self, parent, dindex=None):

        super(urunekle, self).__init__(parent)
        self.dindex = dindex
        self.db = db_helper()
        self.kisiler_liste = self.db.kisiler_aktif()
        self.kategori_liste = self.db.kategori_liste()

        if dindex != None:
            self.dmr = self.db.demirbas(dindex)

        self.setWindowTitle("Demirbaş Ekleme Ekranı")

        self.tablelayout = QGridLayout()

        self.demirbas_no_label = QLabel("Demirbaş No")
        self.urun_adi_label = QLabel("Ürün Adı")
        self.teslim_alan_label = QLabel("Teslim Alan")
        self.islem_tarihi_label = QLabel("İşlem Tarihi")
        self.kategori_label = QLabel("Kategori")
        self.adet_label = QLabel("Ürün Adeti")
        self.marka_label = QLabel("Marka")
        self.model_label = QLabel("Model")
        self.seri_no_label = QLabel("Seri No")
        self.garanti_suresi_label = QLabel("Garanti Süresi")
        self.satin_alinma_tarihi_label = QLabel("Satın Alınma Tarihi")
        self.bulundugu_yer_label = QLabel("Bulunduğu Yer")
        self.aciklama_label = QLabel("Açıklama")

        self.tablelayout.addWidget(self.demirbas_no_label, 0, 0)
        self.tablelayout.addWidget(self.urun_adi_label, 1, 0)
        self.tablelayout.addWidget(self.teslim_alan_label, 2, 0)
        self.tablelayout.addWidget(self.islem_tarihi_label, 3, 0)
        self.tablelayout.addWidget(self.kategori_label, 4, 0)
        self.tablelayout.addWidget(self.adet_label, 5, 0)
        self.tablelayout.addWidget(self.marka_label, 6, 0)
        self.tablelayout.addWidget(self.model_label, 7, 0)
        self.tablelayout.addWidget(self.seri_no_label, 8, 0)
        self.tablelayout.addWidget(self.garanti_suresi_label, 9, 0)
        self.tablelayout.addWidget(self.satin_alinma_tarihi_label, 10, 0)
        self.tablelayout.addWidget(self.bulundugu_yer_label, 11, 0)
        self.tablelayout.addWidget(self.aciklama_label, 12, 0)

        self.demirbas_no = QLineEdit()
        self.urun_adi = QLineEdit()
        self.teslim_alan = QComboBox()
        for kisi in self.kisiler_liste:
            self.teslim_alan.addItem(kisi[1])
        self.teslim_alan_ekle = QPushButton("KİŞİ EKLE")
        self.teslim_alan_ekle.clicked.connect(self.kisi_ekle)
        self.islem_tarihi = QDateEdit()
        self.islem_tarihi.setDate(datetime.now().date())
        self.kategori = QComboBox()
        self.kategori.addItem("Kategorisiz")
        for kat in self.kategori_liste:
            self.kategori.addItem(kat[1])
        self.kategori_ekle = QPushButton("KATEGORİ EKLE")
        self.kategori_ekle.clicked.connect(self.kat_ekle)
        self.adet = QLineEdit()
        self.marka = QLineEdit()
        self.model = QLineEdit()
        self.seri_no = QLineEdit()
        self.garanti_suresi = QLineEdit()
        self.satin_alinma_tarihi = QDateEdit()
        self.satin_alinma_tarihi.setDate(datetime.now().date())
        self.bulundugu_yer = QLineEdit()
        self.aciklama = QTextEdit()
        if self.dindex != None:
            self.demirbas_no.setText(str(self.dmr[1]))
            self.urun_adi.setText(self.dmr[2])
            kx = self.combo_index(self.kisiler_liste, self.dmr[3])
            self.teslim_alan.setCurrentIndex(kx)
            date_obj = datetime.strptime(self.dmr[4], '%d.%m.%Y')
            self.islem_tarihi.setDate(date_obj.date())
            kc = self.combo_index(self.kategori_liste, self.dmr[5])
            print(kc)
            self.kategori.setCurrentIndex(kc + 1)
            self.adet.setText(str(self.dmr[6]))
            self.marka.setText(self.dmr[7])
            self.model.setText(self.dmr[8])
            self.seri_no.setText(self.dmr[9])
            self.garanti_suresi.setText(str(self.dmr[10]))
            date_obj1 = datetime.strptime(self.dmr[11], '%d.%m.%Y')
            self.satin_alinma_tarihi.setDate(date_obj1.date())
            self.bulundugu_yer.setText(self.dmr[12])
            self.aciklama.setText(self.dmr[13])

        self.tablelayout.addWidget(self.demirbas_no, 0, 1)
        self.tablelayout.addWidget(self.urun_adi, 1, 1)
        self.tablelayout.addWidget(self.teslim_alan, 2, 1)
        self.tablelayout.addWidget(self.teslim_alan_ekle, 2, 2)
        self.tablelayout.addWidget(self.islem_tarihi, 3, 1)
        self.tablelayout.addWidget(self.kategori, 4, 1)
        self.tablelayout.addWidget(self.kategori_ekle, 4, 2)
        self.tablelayout.addWidget(self.adet, 5, 1)
        self.tablelayout.addWidget(self.marka, 6, 1)
        self.tablelayout.addWidget(self.model, 7, 1)
        self.tablelayout.addWidget(self.seri_no, 8, 1)
        self.tablelayout.addWidget(self.garanti_suresi, 9, 1)
        self.tablelayout.addWidget(self.satin_alinma_tarihi, 10, 1)
        self.tablelayout.addWidget(self.bulundugu_yer, 11, 1)
        self.tablelayout.addWidget(self.aciklama, 12, 1)

        self.yatay = QHBoxLayout()
        self.kaydet_btn = QPushButton("KAYDET")
        self.kaydet_btn.clicked.connect(self.onKaydetBtnClick)
        self.iptal_btn = QPushButton("İPTAL")
        self.iptal_btn.clicked.connect(self.oniptalBtnClick)
        self.yatay.addWidget(self.kaydet_btn)
        self.yatay.addWidget(self.iptal_btn)

        qw = QWidget()
        qw.setLayout(self.yatay)

        self.tablelayout.addWidget(qw, 13, 1)

        self.setLayout(self.tablelayout)

        self.demirbas_dt = demirbas_detay()

    def onKaydetBtnClick(self):
        lst = []
        try:
            dno = self.demirbas_no.text()
            dno = int(dno)
        except ValueError:
            QMessageBox.warning(self, "Hata", "Demirbaş No düzgün girilmemiş")
            return
        lst.append(dno)
        if len(self.urun_adi.text()) < 1:
            QMessageBox.warning(self, "Hata", "Demirbaş adı boş bırakılamaz")
            return
        lst.append(self.urun_adi.text())
        lst.append(self.index_ver(self.kisiler_liste, self.teslim_alan.currentText()))
        lst.append(self.islem_tarihi.text())
        lst.append(self.index_ver(self.kategori_liste, self.kategori.currentText()))
        try:
            adt = self.adet.text()
            adt = int(adt)
        except ValueError:
            QMessageBox.warning(self, "Hata", "Adet düzgün girilmemiş. Sonradan giriş yapacaksanız 0 değerini giriniz!")
            return
        lst.append(adt)
        lst.append(self.marka.text())
        lst.append(self.model.text())
        lst.append(self.seri_no.text())
        try:
            grt = self.garanti_suresi.text()
            grt = int(grt)
        except ValueError:
            QMessageBox.warning(self,
                                "Garanti Süresi düzgün girilmemiş. Sonradan giriş yapacaksanız 0 değerini giriniz!")
            return
        lst.append(grt)

        lst.append(self.satin_alinma_tarihi.text())
        lst.append(self.bulundugu_yer.text())
        lst.append(str(self.aciklama.toPlainText()))

        if self.dindex != None:
            print("Düzenle")
            self.db.demirbas_duzenle(lst, self.dindex)
        else:
            print("Ekle")
            rindex = self.db.demirbas_ekle(lst)

        self.done(QDialog.Accepted)

    def oniptalBtnClick(self):
        print("İptal edildi")
        self.done(QDialog.Rejected)

    def index_ver(self, liste, isim):
        a = 0
        for kisi in liste:
            if kisi[1] == isim:
                return kisi[0]
        return -1

    def combo_index(self, liste, idx):
        a = 0
        if idx == -1:
            return -1
        for k in liste:
            if k[0] == idx:
                return a
            else:
                a += 1
        return 0

    def kisi_ekle(self):
        kisiekr = kisiler_ekr(self, p=1)
        result = kisiekr.exec()
        if result == QDialog.Accepted:
            self.kisiler_liste = self.db.kisiler_aktif()
            self.teslim_alan.clear()
            for kisi in self.kisiler_liste:
                self.teslim_alan.addItem(kisi[1])

    def kat_ekle(self):
        katekr = kategori_ekr(self, p=1)
        result = katekr.exec()
        if result == QDialog.Accepted:
            self.kategori_liste = self.db.kategori_liste()
            self.kategori.clear()
            self.kategori.addItem("Kategorisiz")
            for kat in self.kategori_liste:
                self.kategori.addItem(kat[1])
