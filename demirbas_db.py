import sqlite3 as db
import os


class db_helper():

    def db_open(self):
        if os.path.exists("demirbas.db"):
            self.vt = db.connect("demirbas.db")
            self.c = self.vt.cursor()
        else:
            raise Exception("HATA", "Veritabanı bulunamadı!")

    def db_close(self):
        self.c.close()

    def demirbas_liste(self):
        self.db_open()
        sql = "select * from demirbas"
        self.c.execute(sql)
        liste = self.c.fetchall()
        self.db_close()
        return list(liste)

    def demirbas(self, ind):
        self.db_open()
        sql = "select * from demirbas where id={}".format(ind)
        self.c.execute(sql)
        l = self.c.fetchone()
        self.db_close()
        return list(l)

    def demirbas_ekle(self, lst):
        self.db_open()
        print(lst)
        sql = "insert into demirbas(demirbas_no,urun_adi,teslim_alan,islem_tarihi,kategori,adet,marka,model,seri_no,garanti_suresi,satin_alinma_tarihi,bulundugu_yer,aciklama) values(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        print(sql)
        self.c.execute(sql, lst)
        self.vt.commit()
        ind = self.c.lastrowid
        self.db_close()
        return ind

    def demirbas_sil(self, ind):
        self.db_open()
        sql = "delete from demirbas where id={}".format(ind)
        self.c.execute(sql)
        self.vt.commit()
        self.db_close()

    def demirbas_duzenle(self, lst, ind):
        sql = "update demirbas set demirbas_no=?,urun_adi=?,teslim_alan =?,islem_tarihi=?,kategori=?,adet=?,marka=?,model=?,seri_no=?,garanti_suresi=?,satin_alinma_tarihi=?,bulundugu_yer=?,aciklama=?  where id={}".format(ind)
        print(sql)
        self.db_open()
        self.c.execute(sql,lst)
        self.vt.commit()
        self.db_close()

    def kisiler_liste(self):
        self.db_open()
        sql = "select * from kisiler"
        self.c.execute(sql)
        liste=self.c.fetchall()
        self.db_close()
        return list(liste)

    def kisiler_aktif(self):
        self.db_open()
        sql = "select * from kisiler where aktif=1"
        self.c.execute(sql)
        liste=self.c.fetchall()
        self.db_close()
        return list(liste)

    def kisi(self,ind):
        self.db_open()
        sql = "select * from kisiler where id={}".format(ind)
        self.c.execute(sql)
        liste = self.c.fetchone()
        self.db_close()
        return liste

    def kisi_ekle(self, lst):
        self.db_open()
        sql = "insert into kisiler(ad,aktif,gorevi) values(?,1,?)"
        self.c.execute(sql, lst)
        self.vt.commit()
        self.db_close()
        return self.c.lastrowid

    def kisi_sil(self, ind):
        self.db_open()
        sql = "update kisiler set aktif=-1 where id={}".format(ind)
        self.c.execute(sql)
        self.vt.commit()
        self.db_close()


    def kisi_duzenle(self, lst, ind):
        self.db_open()
        sql = "update kisiler set ad=?, gorevi=?  where id={}".format(ind)
        self.c.execute(sql, lst)
        self.vt.commit()
        self.db_close()

    def kategori_liste(self):
        self.db_open()
        sql = "select * from kategori"
        self.c.execute(sql)
        liste = self.c.fetchall()
        self.db_close()
        return list(liste)

    def kategori_ekle(self, lst):
        self.db_open()
        sql = "insert into kategori(ad ,aciklama) values(?,?)"
        self.c.execute(sql, lst)
        self.vt.commit()
        self.db_close()

    def kategori_sil(self, ind):
        self.db_open()
        sql = "delete from kategori where id={}".format(ind)
        self.c.execute(sql)
        self.vt.commit()
        sql = "update demirbas set kategori=-1  where kategori={}".format(ind)
        self.c.execute(sql)
        self.vt.commit()
        self.db_close()

    def kategori_duzenle(self, lst, ind):
        self.db_open()
        sql = "update kategori set ad=?,aciklama=? where id={}".format(ind)
        self.c.execute(sql,lst)
        self.vt.commit()
        self.db_close()

    def kategori(self,ind):
        self.db_open()
        sql = "select * from kategori where id={}".format(ind)
        self.c.execute(sql)
        liste = self.c.fetchone()
        self.db_close()
        return liste
