import numpy as np
import pandas as pd
import binascii
import os, base64, json, re, io
import datetime

class Pembentukan_Codeword:
    def __init__(self):
        pass

    def _deret_fibonaci(self, limit):
        deret_fibonaci = [1, 2]
        while (deret_fibonaci[-1] + deret_fibonaci[-2]) <= limit:
            temp = deret_fibonaci[-1] + deret_fibonaci[-2] # nilai akhir + nilai ke dua akhir
            deret_fibonaci.append(temp)
    
        return deret_fibonaci

    # pembentukan codeword fibonacci (menggunakan teori zeckendorf)
    def fibonaci(self, bilangan):
        deret_fibonaci = self._deret_fibonaci(bilangan)
        codeword = []
        string_biner = ""
        
        if bilangan <= 1:
            return "11"
    
        for bilangan_fibonaci in reversed(deret_fibonaci):
            if bilangan_fibonaci <= bilangan:
                codeword.append(bilangan_fibonaci)
                bilangan = bilangan - bilangan_fibonaci
                string_biner += "1"
            else:
                string_biner += "0"
    
        string_biner = string_biner[::-1]  # reversed
        string_biner += "1"   # menambahkan angka 1 diakhir
        
        return string_biner

    # pembentukan codeword levenstein
    def levenstein(self, n):
        if n==0:
            return "0"
        else:
            return n and '1%s'%self.levenstein(len(bin(n))-3)+bin(n)[3:]

class Alat:
    def __init__(self):
        pass

    def gabung_list(self, *args, **kwargs):
        list_index = []

        for i in args[0]:
            if len(i)>0:
                list_index.append(len(i))
        
        hasil = np.concatenate(*args, **kwargs)
        return hasil, list_index

    def pisahkan_list(self, arr,  list_index):
        temp = list_index[0]
        indices = [list_index[0]]
        jumlah = 0
        for i in range(1, len(list_index)):
            jumlah = list_index[i] + temp
            indices.append(jumlah)
            temp = jumlah

        return np.split(arr, indices)[:-1]

class Konversi:
    def __init__(self):
        pass

    def objek_decode(self, data):
        return json.loads(base64.b64decode(data.encode()).decode())

    def objek_encode(self, obj):
        return base64.b64encode(json.dumps(obj).encode()).decode()

    def list_str(self, my_list, pemisah=","):
        my_str = pemisah.join(map(str, my_list))
        return my_str

    def str_list(self, my_str, pemisah=","):
        my_list = list(my_str.split(pemisah))
        return my_list

    def bin_ascii(self, string_biner):
        bilangan = int(string_biner, 2)
        return chr(bilangan)

    def ascii_bin(self, string_ascii, bit=8):
        bilangan = ord(string_ascii)
        return format(bilangan, '0'+str(bit)+'b')

    def hex_int(self, hexadesimal):
        return int(hexadesimal, 16)

    def int_hex(self, bilangan):
        return hex(bilangan)[2:]

    def hex_bin(self, hexadesimal):
        bilangan = self.hex_int(hexadesimal)
        return self.int_bin(bilangan)

    def bin_hex(self, string_biner):
        bilangan = int(string_biner, 2)
        return hex(bilangan)[2:]

    def bin_int(self, string_biner):
        return int(string_biner, 2)

    def int_bin(self, bilangan, bit=8):
        return format(bilangan, '0'+str(bit)+'b')

    def list_str(self, my_list, pemisah=','):
        # my_str = pemisah.join(my_list)   # jika list hanya mengandung str
        my_str = pemisah.join(map(str, my_list))  # ini jika mylist mengandung int, float, dll
        return my_str

    def str_list(self, my_string, pemisah=","):
        my_list = list(my_string.split(pemisah))
        return my_list
        

class Utils:
    def __init__(self):
        pass

    def generate_name(self):
        waktu_sekarang = datetime.datetime.now()
        
        return waktu_sekarang.strftime("%Y%m%d%H%M%S")


class Dataku:
    def __init__(self):
        self.list_kompresi = np.array([], dtype=np.uint8)  # hasil gabungan kompresi 
        self.list_dekompresi = np.array([], dtype=np.uint8)  # hasil gabungan dekompresi 
        self.list_kode = []  # hasil kode kompresi 
        # self.part_kompresi = []  # hasil pemisahan kompresi 
        self.konversi = Konversi()
        # self.utils = Utils()
        self.alat = Alat()
        self.indeks = []

        self.arr_1d = None
        self.arr_1d_potongan = []

    def baca_data_dari_numpy(self, arr_1d):
        self.arr_1d = arr_1d
        return self

    def load_sampel(self, nama_file):
        with open(nama_file, "rb") as file:
            self.arr_1d = np.frombuffer(file.read(), dtype=np.uint8)
            
        return self

    def potong_data(self, jumlah_potongan):
        nTotal = self.arr_1d.shape[0]
        arr = self.arr_1d

        potongan = []
        for i in range(0, nTotal, jumlah_potongan):
            temp = arr[i:i+jumlah_potongan]
            potongan.append(temp)


        self.arr_1d_potongan = potongan
        
        return self

    def set_list_kode(self, value=None):
        assert value is not None, "value tidak boleh kosong"
        
        self.list_kode.append(value)
        
        return self

    def set_part_kompresi(self, arr_1d=None, indeks=None):
        if indeks is None:
            assert len(self.indeks) > 0, "self indeks masih kosong"
            
            return self.alat.pisahkan_list(arr_1d, self.indeks)
        
        return self.alat.pisahkan_list(arr_1d, indeks)
        

    def astype(self, arr_1d, tipe="desimal"):
        if tipe == "desimal":
            vfunc = np.vectorize(self.konversi.bin_int)
        elif tipe == "biner":
            vfunc = np.vectorize(self.konversi.int_bin)
        elif tipe == "hexa":
            vfunc = np.vectorize(self.konversi.int_hex)
        else:
            raise Exception("tipe tidak sesuai")
            
        return vfunc(arr_1d)

    def add_kompresi(self, arr_1d):
        self.indeks.append(len(arr_1d))
        self.list_kompresi = np.append(self.list_kompresi, arr_1d)
        return self

    def add_dekompresi(self, arr_1d):
        self.list_dekompresi = np.append(self.list_dekompresi, arr_1d)
        return self

    def simpan_indeks(self, nama_file="index.txt"):
        
        # simpan indeks
        a = np.array(self.indeks, dtype=np.uint8)
        a.tofile(nama_file)
        
        return self

    def load_indeks(self, nama_file="index.txt"):
        
        # load indeks
        with open(nama_file, "rb") as file:
            a = np.frombuffer(file.read(), dtype=np.uint8)
        self.indeks = a.tolist()
        
        return self

    def simpan_kode(self, nama_file="kode1.npy"):
        assert len(self.list_kode) > 0, "list_kode tidak boleh kosong"

        # simpan kode
        np.save(nama_file, self.list_kode)
        
        return self

    def load_kode(self, nama_file="kode1.npy"):
        # load kode
        self.list_kode = np.load(nama_file, allow_pickle=True)
        
        return self

    def simpan_list_kompresi(self, nama_file="hasil_kompresi1.pdf"):
        with open(nama_file, "wb") as file:
            file.write(self.list_kompresi.tobytes())
        
        return self

    def load_list_kompresi(self, nama_file="hasil_kompresi1.pdf"):
        with open(nama_file, "rb") as file:
            self.list_kompresi = np.frombuffer(file.read(), dtype=np.uint8)
            
        return self

    def set_list_kompresi(self, arr_1d):
        self.list_kompresi = arr_1d
        return self

    def simpan_list_dekompresi(self, nama_file="hasil_dekompresi1.pdf"):
        with open(nama_file, "wb") as file:
            file.write(self.list_dekompresi.tobytes())
        
        return self
    
class Compression:
    def __init__(self, arr_1d):
        self.arr_1d = arr_1d
        self.codeword = Pembentukan_Codeword()
        self.encode = {}
        self.decode = {}
        self.konversi = Konversi()

         # kode
        self._key = ["indeks1", "indeks2", "decode_fib", "decode_lev"]
        self.kode = {
            self._key[0]: [],
            self._key[1]: [],
            self._key[2]: {},
            self._key[3]: {},
        }

    def set_kode(self, indeks=0, value=None):
        self.kode[self._key[indeks]] = value
        return self

    def _reset_encode_decode(self):
        self.encode = {}
        self.decode = {}
        return self

    def _pengurutan(self, arr=None):
        if arr is None:
            arr = self.arr_1d
            
        element_unik, frekuensi = np.unique(arr, return_counts=True)
        sorted_indexes = np.argsort(frekuensi)[::-1]
        sorted_by_freq = element_unik[sorted_indexes]
        
        return sorted_by_freq

    def _pembentukan_codeword(self, arr_unique, tipe):
        n = arr_unique.shape[0]

        if tipe=="fib":
            hasil = np.array([self.codeword.fibonaci(x) for x in range(1, n+1)], dtype=object)
        else:
            hasil = np.array([self.codeword.levenstein(x) for x in range(0, n)], dtype=object)
            
        return hasil

    def fit(self, arr=None, tipe="fib"):
        if not(tipe=="fib" or tipe=="lev"):
            raise Exception("tipe tidak sesuai")
            
        x = self._pengurutan(arr)
        y = self._pembentukan_codeword(x, tipe)

        assert len(x) == len(y), "panjang data tidak sesuai"

        self._reset_encode_decode()
        
        self.encode = {i: v for i,v in list(zip(x, y))}
        self.decode = {v: i for i,v in list(zip(x, y))}
        return self


    def transformasi(self, arr_1d=None):
        if arr_1d is None:
            raise Exception("arr_1d tidak boleh kosong")
            
        hasil = np.array([self.encode[x] for x in arr_1d], dtype=object)
            
        return hasil

    def penggabungan(self, arr_1d=None):
        if arr_1d is None:
            arr_1d = self.arr_1d

        # simapn kode indeks sebelum digabungkan
        vfunc = np.vectorize(len)
        indeks = vfunc(arr_1d)
            
        hasil = "".join(map(str, arr_1d))
        
        return indeks, hasil

    def padding_flag(self, string_biner, jumlah_bit=8):  
        # string_biner = self.kompresi1
        n = len(string_biner)
        sisa_bagi = n % jumlah_bit
        
        # assert n >= 8, "panjang string binernya kurang dari 8"
    
        if sisa_bagi == 0:
            return string_biner
        else:
            padding = "0" * (7-sisa_bagi) + "1"   # rumus: 7 - sisa_bagi + "1"
            flag = 9 - sisa_bagi                  # rumus: 9 - sisa_bagi
            flag = format(flag, '08b')
    
            return string_biner + padding + flag    

    def pembagian_8_bit(self, string_biner):
        assert len(string_biner) % 8 == 0, "string biner tidak dapat di susun 8 bit"
        
        hasil = np.array([string_biner[i:i+8] for i in range(0, len(string_biner), 8)])
        
        return hasil

    def pembentukan_ascii(self, arr_1d=None):
        if arr_1d is None:
            raise Exception("tidak boleh kosong")
            
        vfunc = np.vectorize(self.konversi.bin_ascii)
        return self.penggabungan(vfunc(arr_1d))

    def pembentukan_desimal(self, arr_1d_string_biner=None):
        if arr_1d_string_biner is None:
            raise Exception("arr_1d_string_biner tidak boleh kosong")
        vfunc = np.vectorize(self.konversi.bin_int)
        
        return vfunc(arr_1d_string_biner).astype(dtype=np.uint8)
    
class Decompression:
    def __init__(self, arr_1d=None):
        self.arr_1d = arr_1d
        self.konversi = Konversi()
        
        # kode
        self._key = ["indeks1", "indeks2", "decode_fib", "decode_lev"]
        self.kode = {
            self._key[0]: [],
            self._key[1]: [],
            self._key[2]: {},
            self._key[3]: {},
        }

    def set_kode(self, value):
        self.kode = value
        return self

    def read_kode(self, nama_file):  # update code
        return self

    def set_arr_1d(self, arr_1d):
        self.arr_1d = arr_1d
        return self

    def baca_data(self):
        return

    def pembentukan_biner(self, arr_1d=None):
        if arr_1d is None:
            # raise Exception("arr_1d tidak boleh kosong")
            arr_1d = self.arr_1d
            
        vfunc = np.vectorize(self.konversi.int_bin)
        
        return vfunc(arr_1d).astype(dtype=object)

    def penggabungan(self, arr_1d=None):
        if arr_1d is None:
            arr_1d = self.arr_1d
            
        hasil = "".join(map(str, arr_1d))
        
        return hasil

    def padding_flag_decode(self, string_biner=None, fib=True):
        assert string_biner is not None, "string_biner tidak bisa kosong"
            
        if fib:
            n_awal = sum(self.kode[self._key[0]])
        else:
            n_awal = sum(self.kode[self._key[1]])
                
        return string_biner[0:n_awal]

    def pemisahan(self, string_biner=None, fib=True):
        assert string_biner is not None, "string_biner tidak boleh kosong"

        if fib:
            indeks = self.kode[self._key[0]]
        else:
            indeks = self.kode[self._key[1]]
                        
        n = len(indeks)
        arr_baru = np.empty(n, dtype=object)
        
        awal = 0
        akhir = 0
        for i in range(0, n):
            if i>0:
                awal = akhir
        
            if i < n-1:
                akhir += indeks[i]
            else:
                akhir = sum(indeks)
            
            arr_baru[i] = string_biner[awal:akhir]
        
        return arr_baru

    def _inverse(self, x, decode):
        return decode[x]

    def inverse_transformasi(self, arr_1d=None, fib=True):
        if arr_1d is None:
            raise Exception("arr_1d tidak boleh kosong")
            
        vfunc = np.vectorize(self._inverse)

        if fib:
            return vfunc(arr_1d, self.kode[self._key[2]])
        else:
            return vfunc(arr_1d, self.kode[self._key[3]])

class Informasi:
    def __init__(self):
        pass

    def ukuran_file(self, file_path):
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            size_kb = size / 1024  # mengkonversi ukuran menjadi satuan kb
            return round(size_kb, 3)
        else:
            raise Exception("file tidak tersedia")
        return self

    def ukuran_df(self, df):
        return round(df.shape[0] / 1024, 2)

class Evaluasi:
    def __init__(self):
        pass

    def hitung_rc(self, ukuran_sebelum, ukuran_sesudah):
        hasil = ukuran_sebelum / ukuran_sesudah
        return round(hasil, 2)

    def hitung_cr(self, ukuran_sebelum, ukuran_sesudah):
        hasil = ukuran_sesudah / ukuran_sebelum * 100
        return round(hasil, 2)

    def hitung_ss(self, ukuran_sebelum, ukuran_sesudah):
        hasil = (ukuran_sebelum - ukuran_sesudah) / ukuran_sebelum * 100
        return round(hasil, 2)
        
        
class Info:
    def __init__(self):
        self.ukuran_sebelum = None
        self.ukuran_setelah = None
        
        self.nilai_cr = None
        self.nilai_rc = None
        self.nilai_ss = None

        self.evaluasi = Evaluasi()

    def set_ukuran_sebelum(self, arr_1d):
        if type(arr_1d == list):
            self.ukuran_sebelum = round(len(arr_1d) / 1024, 2)
        else:
            self.ukuran_sebelum = round(arr_1d.shape[0] / 1024, 2)
            
        return self

    def set_ukuran_setelah(self, arr_1d):
        if type(arr_1d == list):
            self.ukuran_setelah = round(len(arr_1d) / 1024, 2)
        else:
            self.ukuran_setelah = round(arr_1d.shape[0] / 1024, 2)
            
        return self


    def set_nilai_cr_rc_ss(self):
        sebelum = self.ukuran_sebelum
        setelah = self.ukuran_setelah
        
        self.nilai_cr = self.evaluasi.hitung_cr(sebelum, setelah)
        self.nilai_rc = self.evaluasi.hitung_rc(sebelum, setelah)
        self.nilai_ss = self.evaluasi.hitung_ss(sebelum, setelah)
    
        return self
    
class Aplikasiku:
    def __init__(self):
        self.dataku = Dataku()
        self.info = Info()
        self.utils = Utils()
        
        self.hasil_bt = None

    def tahap1(self, file, dari_numpy=False):
        """
        params
        -----
        file bisa berupa string (nama file) bisa juga berupa numpy array 1D

        return
        ------
        self
        
        """
        
        dataku = self.dataku
        info = self.info
        
        if dari_numpy:
            dataku.baca_data_dari_numpy(file)
        else:
            dataku.load_sampel(file)

        info.set_ukuran_sebelum(dataku.arr_1d) # untuk menyinpan informasi ukuran awal
        
        dataku.potong_data(16)

        for i in dataku.arr_1d_potongan:
            komp1 = Compression(i)
            komp1.fit(arr=komp1.arr_1d, tipe="fib")
            hasil_kompresi = komp1.transformasi(arr_1d=komp1.arr_1d)
            indeks, hasil_penggabungan = komp1.penggabungan(hasil_kompresi)
            hasil_padding_flag = komp1.padding_flag(hasil_penggabungan)
            hasil_penyusunan_ulang = komp1.pembagian_8_bit(hasil_padding_flag)
            hasil_pembentukan_desimal = komp1.pembentukan_desimal(hasil_penyusunan_ulang)
    
            komp1.set_kode(0, indeks)
            komp1.set_kode(2, komp1.decode)
            
            komp1.fit(arr=hasil_pembentukan_desimal, tipe="lev")
            hasil_kompresi = komp1.transformasi(arr_1d=hasil_pembentukan_desimal)
            indeks, hasil_penggabungan = komp1.penggabungan(hasil_kompresi)
            hasil_padding_flag = komp1.padding_flag(hasil_penggabungan)
            hasil_penyusunan_ulang = komp1.pembagian_8_bit(hasil_padding_flag)
            hasil_pembentukan_desimal = komp1.pembentukan_desimal(hasil_penyusunan_ulang)
            
            komp1.set_kode(1, indeks)
            komp1.set_kode(3, komp1.decode)
    
            dataku.set_list_kode(komp1.kode)
            dataku.add_kompresi(hasil_pembentukan_desimal)
        
        info.set_ukuran_setelah(dataku.list_kompresi)
        info.set_nilai_cr_rc_ss()
        
        return self

    def tahap2(self, nama_file="hasil_kompresi11.txt", simpan_bt=False):
        dataku = self.dataku

        nama = self.utils.generate_name()    # len 14
        
        dataku.simpan_indeks(nama+".txt")
        dataku.simpan_kode(nama+".npy")

        # tambahkan nama_kode di data kompresi
        list_nama = np.array([*nama], dtype=np.uint8)    # konversi string menjasi list menggunanan unpack(*) method
        tambahan = np.concatenate([list_nama, dataku.list_kompresi])
        dataku.set_list_kompresi(tambahan)

        if simpan_bt:
            self.hasil_bt = self.dataku.list_kompresi.tobytes()
        else:
            dataku.simpan_list_kompresi(nama_file)

        return self

    def tahap3(self, file="hasil_kompresi11.txt", dari_numpy=False):
        dataku = self.dataku

        
        if dari_numpy:
            dataku.set_list_kompresi(file)
        else:
            dataku.load_list_kompresi(file)

        # modifikasi baru
        nama = dataku.list_kompresi[0:14].tolist()
        nama = dataku.konversi.list_str(nama, "")

        assert len(nama) == 14, "panjang nama tidak sesuai"
        
        dataku.load_indeks(nama+".txt")
        dataku.load_kode(nama+".npy")
    
        data_kompresi = dataku.list_kompresi[14:]  # sudah dipotong
        potongan_data_kompresi = dataku.set_part_kompresi(data_kompresi)

        for i, v in enumerate(potongan_data_kompresi):
            dekomp1 = Decompression(v)
            dekomp1.set_kode(dataku.list_kode[i])
            
            hasil_pembentukan_biner = dekomp1.pembentukan_biner(arr_1d=None)
            d_penggabungan = dekomp1.penggabungan(arr_1d=hasil_pembentukan_biner)
            decode_padding_flag = dekomp1.padding_flag_decode(d_penggabungan, fib=False)
            hasil_pemisahan = dekomp1.pemisahan(decode_padding_flag, fib=False)
            hasil_dekompresi = dekomp1.inverse_transformasi(hasil_pemisahan, fib=False)
        
            hasil_pembentukan_biner = dekomp1.pembentukan_biner(arr_1d=hasil_dekompresi)
            d_penggabungan = dekomp1.penggabungan(arr_1d=hasil_pembentukan_biner)
            decode_padding_flag = dekomp1.padding_flag_decode(d_penggabungan, fib=True)
            hasil_pemisahan = dekomp1.pemisahan(decode_padding_flag, fib=True)
            hasil_dekompresi = dekomp1.inverse_transformasi(hasil_pemisahan, fib=True)
    
            dataku.add_dekompresi(hasil_dekompresi)

        return self

    def tahap4(self, nama_file="hasil_dekompresi11.pdf", simpan_bt=False):
        
        if simpan_bt:
            self.hasil_bt = self.dataku.list_dekompresi.tobytes()
        else:
            self.dataku.simpan_list_dekompresi(nama_file)
        
        return self