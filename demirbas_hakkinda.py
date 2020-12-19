from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import *


class hakkinda(QDialog):
    def __init__(self, parent):
        super(hakkinda, self).__init__(parent)

        self.setWindowTitle("Demirbaş Yönetim Sistemi")

        self.etiket = QLabel(self)
        self.etiket.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("icon/dmr_cube.png")
        pixmap=pixmap.scaled(128 ,128)
        self.etiket.setPixmap(pixmap)


        self.baslik = QLabel(self)
        self.baslik.setText("Demirbaş Envanter Yönetim Sistemi")
        self.baslik.setFont(QtGui.QFont("Segoe UI",20,QtGui.QFont.Bold))
        self.baslik.setAlignment(Qt.AlignCenter)

        self.yapanlar=QLabel(self)
        self.yapanlar.setText("Hasan Özçetin, İsmail Gövercin, Selahattin Çekcen")
        self.yapanlar.setAlignment(Qt.AlignCenter)

        label = QLabel()
        label.openExternalLinks()
        label.setText("<a href='https://github.com/faytoncular/demirbas_yonetim'>https://github.com/faytoncular/demirbas_yonetim</a>")
        label.setAlignment(Qt.AlignCenter)

        dikey = QVBoxLayout()
        dikey.addWidget(self.etiket)
        dikey.addWidget(self.baslik)
        dikey.addWidget(self.yapanlar)
        dikey.addWidget(label)



        self.setMinimumSize(500, 500)
        self.setLayout(dikey)
