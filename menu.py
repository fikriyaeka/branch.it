
import sqlite3

databaseName='iniDBbuatCoba.db'
conn = sqlite3.connect(databaseName)

from method import *
from databaseInit import *


#login()
def login():
    username=input("masukkan username ")
    password=input("masukkan password ")
    a=conn.cursor().execute("select * from user where username=? AND password=?",(username,password))
    result=a.fetchall()
    print(result)
    if result:
        print("selamat datang di Branch.it {}".format(username))
    else:
        print("maaf, username dan password yang anda masukkan salah. silahkan coba kembali")

#absenKehadiran()
def absenKehadiran(username):
    username.setJumlahAbsensi()
    print("Absensi telah ditambahkan, Selamat Bekerja!")


def cekStokToko(cabang):
    id=Toko.getIdCabang(str(cabang))
    data=conn.cursor().execute("select * from barang where idCabang=?",(id,))
    for row in data:
        print("====")
        print("{}\t stok : {}".format(row[1],row[4]))


def cekStokSemuaToko():
    listId=list(Toko.getCabangDict().values())
    for i in listId:
        print("=====STOK TOKO {}=====".format(Toko.getCabangbyId(i)).upper())
        data=conn.cursor().execute("select * from barang where idCabang=?",(i,))
        for row in data:
            print("{}\t stok : {}".format(row[1],row[4]))


def cetakTransaksi(username,cabang):
    cekStokToko(cabang)
    tgl=input("masukkan tanggal :")
    barang=input("tuliskan nama barang : ").lower()
    jumlah=int(input("tuliskan jumlah barang : "))
    listTransaksi={}
    listTransaksi[barang] = jumlah
    Transaksi(tgl,listTransaksi,username,cabangObjek)
    namaBarang=eval(barang+str(idCabang))
    namaBarang.setJumlahTerjual(jumlah)
    # acer2.setJumlahTerjual(1)
    

def tampilkanOmsetSemuaToko():
    # idCabang=input("masukkan cabang yang ingin ditampilkan :")
    # cabang.tampilkanInfo()
    listId=list(Toko.getCabangDict().values())
    for i in listId:
        data=conn.cursor().execute("select * from toko where idCabang=?",(i,))
        for row in data:
            print("Toko {}\t Omset : {}".format(row[1],row[2]))


#=============
def daftarAbsensiKaryawan(cabang):
    idCabang=Toko.getIdCabang(cabang)
    data=conn.cursor().execute("select idUser,username,jumlahAbsensi from user")
    for row in data:
        if row[0][0]==str(3) and row[0][5]==str(idCabang):
            print("Nama : {} \t jumlahAbsensi : {} ".format(row[1],row[2]))
            break


def rekapitulasiToko(idCabang):
    dataTransaksi=conn.cursor().execute("select * from transaksi")
    print("REKAPITULASI PENJUALAN TOKO {} ".format(Toko.getCabangbyId(int(idCabang))))
    for row in dataTransaksi:
        if row[0][0]==str(idCabang):
            print("""
    ID Transaksi : {}
    Tanggal      : {}
    jumlah       : {}
            """.format(row[0],row[1],row[2]))


def rekapitulasiSemuaToko():
    dictToko=Toko.getCabangDict()
    listIdToko=list(dictToko.values())
    for i in listIdToko:
        rekapitulasiToko(i)


def tambahBarang():
    namaBarang=input("masukkan nama barang : ")
    harga=int(input("masukkan harga barang : "))
    keuntungan=float(input("masukkan persentase keuntungan : "))
    jumlahStok=int(input("masukkan jumlah stok yang tersedia : "))
    namaObjek=(str(namaBarang)+str(idCabang))
    namaObjek=Barang(namaBarang,harga,keuntungan,jumlahStok,idCabang)

def tambahKaryawan():
    usernameKaryawan=input("masukkan nama karyawan baru :")
    password=int(input("masukkan password karyawan baru :"))
    listStatus=Karyawan.getStatusDict()
    # for i in listStatus:
    # print ("status {} ".format(i))
    status=input("masukkan status kepegawaian karyawan :")
    status=status.title()
    usernameKaryawan=Karyawan(usernameKaryawan,password,cabang,status)

def dataKehadiranKaryawan(idCabang):
    data=data=conn.cursor().execute("select * from user")
    for row in data:
        x=row[0].split("-")
        if x[2]==idCabang and x[0]=="3":
            print ("Nama Karyawan: {}\t JumlahAbsensi: {} ".format(row[1],row[3]))

def ubahStok(idCabang):
    cekStokToko(str(cabang))
    namaBarang=input("masukkan nama barang yang ingin diubah")
    idBarang=None
    data=conn.cursor().execute("select idBarang from barang where namaBarang=? and idCabang=?",(namaBarang,idCabang,))
    for row in data:
        idBarang=row[0]
    jumlah=int(input("masukkan update jumlah barang"))
    data=conn.cursor().execute("update barang set jumlahStok=? where idBarang=?",(jumlah,idBarang,))
    conn.commit()

def tampilkanListHargaBarang(idCabang):
    
    data=conn.cursor().execute("select * from barang where idCabang=?",(idCabang,))
    for row in data:
        print ("Nama Barang : {} \t harga : {}".format(row[1],row[3]))

def rankPenjualanBarang(idCabang):
    data=conn.cursor().execute("select * from barang where idCabang=? order by jumlahTerjual desc",(idCabang,))
    for row in data:
        print("Nama barang : {} \t jumlah Terjual : {} \t keuntungan: {} ".format(row[1],row[5],row[6]))

def rankSemuaToko():
    data=conn.cursor().execute("select * from toko order by omset desc")
    i=0
    for row in data:
        i+=1
        print("Rank {} Cabang Toko : {} \t Omset : {}  ".format(i,row[1],row[2]))

def omsetSemuaToko():
    data=conn.cursor().execute("select sum(omset) from toko")
    for row in data:
        print("Selamat Owner, Omset hingga saat ini sudah mencapai {}".format(row))


def menuOwner():
    print("""
            Selamat datang Owner, berikut pilihan menu yang tersedia :
                1. Melihat identitas tiap toko 
                2. Melihat rekapitulasi penjualan di semua toko
                3. Melihat data stok barang di semua toko
                4. Omset keseluruhan
                5. Rank Toko dengan Omset Tertinggi 
            """)
    pilihan=input("masukkan angka pilihan menu : ")
    if pilihan=="1":
        tampilkanOmsetSemuaToko()
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuOwner()
        else:
            print("terimakasih Owner, sampai jumpa besok")
    elif pilihan=="2":
        rekapitulasiSemuaToko()
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuOwner()
        else:
            print("terimakasih Owner, sampai jumpa besok")
    elif pilihan=="3":
        cekStokSemuaToko()
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuOwner()
        else:
            print("terimakasih Owner, sampai jumpa besok")

    elif pilihan=="4":
        omsetSemuaToko()
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuOwner()
        else:
            print("terimakasih Owner, sampai jumpa besok")
    elif pilihan=="5":
        rankSemuaToko()
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuOwner()
        else:
            print("terimakasih Owner, sampai jumpa besok")
  

def menuManager():
    print("""
            Selamat datang Bapak/Ibu Manager, berikut pilihan menu yang tersedia :
            1. Melihat stok barang pada toko
            2. Menambahkan data barang
            3. Menambahkan data karyawan 
            4. Melihat data kehadiran karyawan
            5. Melihat rekapitulasi penjualan toko
            6. Rank penjualan barang tertinggi

            """)
    pilihanManager=input("masukkan angka pilihan menu : ")
    if pilihanManager=="1":
        cekStokToko(cabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuManager()
        else:
            print("terimakasih, sampai jumpa besok")
    elif pilihanManager=="2":
        tambahBarang()
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuManager()
        else:
            print("terimakasih, sampai jumpa besok")

    elif pilihanManager=="3":
        tambahKaryawan()
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuManager()
        else:
            print("terimakasih, sampai jumpa besok")
    
    elif pilihanManager=="4":
        dataKehadiranKaryawan(idCabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuManager()
        else:
            print("terimakasih, sampai jumpa besok")

    elif pilihanManager=="5":
        rekapitulasiToko(idCabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuManager()
        else:
            print("terimakasih, sampai jumpa besok")
    elif pilihanManager=="6":
        print(idCabang)
        rankPenjualanBarang(idCabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuManager()
        else:
            print("terimakasih, sampai jumpa besok")


def menuKaryawan():
    absenKehadiran(objek)
    print("""
            Selamat datang {}, berikut pilihan menu yang tersedia :
            1. Mengubah stok barang
            2. Melihat list data harga barang
            3. Membuat data transaksi penjualan
            4. Melihat data stok barang
            5. Exit
            """.format(username))
    pilihan=input("masukkan angka pilihan menu : ")
    if pilihan=="1":
        ubahStok(idCabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuKaryawan()
        else:
            print("terimakasih, sampai jumpa besok")
    elif pilihan=="2":
        tampilkanListHargaBarang(idCabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuKaryawan()
        else:
            print("terimakasih, sampai jumpa besok")
    elif pilihan=="3":
        cetakTransaksi(usernameObjek,cabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuKaryawan()
        else:
            print("terimakasih, sampai jumpa besok")
    elif pilihan=="4":
        cekStokToko(cabang)
        inputMenu=input("apakah ingin kembali ke menu? y/n ")
        if inputMenu== "y":
            menuKaryawan()
        else:
            print("terimakasih, sampai jumpa besok")
    elif pilihan=="5":
        print("terimakasih, sampai ketemu besok!")





def menuLanding():
    while True:
        global idUser
        global idCabang
        global idJabatan
        global username
        global usernameObjek
        global objek
        global cabang
        global cabangObjek
        global namaBarang
        print("Halooo selamat datang di program kami, untuk melanjutkan silahkan login terlebih dahulu")
        username=input("masukkan username ")
        usernameObjek=eval(username)
        
        password=input("masukkan password ")
        a=conn.cursor().execute("select * from user where username=? AND password=?",(username,password))
        result=a.fetchall()
        #print(result)
        if result:
            print("selamat datang di Branch.it {}".format(username))
        else:
            print("maaf, username dan password yang anda masukkan salah. silahkan coba kembali")
            break
        
        x=conn.cursor().execute("select idUser from user where username=?",(username,)).fetchall()
        for row in x:
            idUser=row[0]
            idCabang=row[0][5]
            idJabatan=row[0][0]
        if idJabatan=="1":
            cabang=str(00)
        else:
            cabang=Toko.getCabangbyId(int(idCabang))
            cabangObjek=eval(cabang)
        objek=eval(username)
        if idJabatan=="1":
            menuOwner()
            break
        elif idJabatan=="2":
            menuManager()
            break
        elif idJabatan=="3":
            menuKaryawan()
            break

        #print(username,idJabatan,idCabang,cabang)


menuLanding()


    










