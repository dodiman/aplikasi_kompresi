import numpy as np
import pandas as pd
import binascii
import os, base64, json, re, io

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
        
class Kompresi:
    def __init__(self, file_path="", mode=None):
        self.biner_file = ""
        self.integer_file = None
        self.hexa_file = None
        self.string_biner_file = None
        self.kolom = ["hexa", "integer", "biner", "frekuensi", "ascii"]
        
        self.konversi = Konversi()
        self.informasi = Informasi()
        self.codeword = Pembentukan_Codeword()

        self.dataku = pd.DataFrame()
        self._dataku = pd.DataFrame()

        self.indeks1_np = np.array([])
        self.indeks2_np = np.array([])
        self.decode_fib_s = pd.Series([])
        self.decode_lev_s = pd.Series([])

        # kode
        self._key = ["indeks1", "indeks2", "decode_fib", "decode_lev"]
        self.kode = {
            self._key[0]: [],
            self._key[1]: [],
            self._key[2]: {},
            self._key[3]: {},
        }

        # fit
        self.encode_fib = {}
        self.decode_fib = {}
        self.encode_lev = {}
        self.decode_lev = {}

        self.kompresi1 = ""
        self.kompresi2 = ""
        self.dekompresi1 = ""
        self.dekompresi2 = ""

        self._string_biner = ""  # untuk menyimpan hasil padding & flagging

        self.dict_kompresi1 = {}
        self.dict_kompresi2 = {}

    def __str__(self):
        return f"class kompresi data"

    def gabung_string_biner(self, s) -> dict:
        hasil = {}
        indeks = s.apply(lambda x: len(x)).values
        string_biner = "".join(map(str, s))  # menggabung string biner
        
        hasil["indeks"] = indeks
        hasil["string_biner"] = string_biner
        return hasil

    def pisahkan_string_biner(self, dict_kompresi) -> pd.Series:
        indeks = dict_kompresi["indeks"]
        s = dict_kompresi["string_biner"]
        n = len(indeks)
        s_baru = np.empty(n, dtype=object)
        
        awal = 0
        akhir = 0
        for i in range(0, n):
            if i>0:
                awal = akhir
        
            if i < n-1:
                akhir += indeks[i]
                # print(indeks[i] + indeks[i+1])
            else:
                akhir = sum(indeks)
            
            # print(f"{awal} {akhir}")
            s_baru[i] = s[awal:akhir]
        
        return pd.Series(s_baru)

    def input_data_hexa(self, list_hexa, s=False):
        if s:
            self.dataku[self.kolom[0]] = list_hexa.tolist()
        else:
            self.dataku[self.kolom[0]] = list_hexa
            
        self.dataku[self.kolom[1]] = self.dataku[self.kolom[0]].apply(self.konversi.hex_int)
        self.dataku[self.kolom[2]] = self.dataku[self.kolom[1]].apply(self.konversi.int_bin)
        

        return

    def input_file_pdf(self, file_path=None):
        if not file_path:
            raise ValueError("file path harus di isi")

        with open(file_path, "rb") as file:
            self.biner_file = file.read()
            self.integer_file = np.frombuffer(self.biner_file, dtype=np.uint8)

        self.dataku[self.kolom[1]] = self.integer_file
        self.dataku[self.kolom[0]] = self.dataku[self.kolom[1]].apply(self.konversi.int_hex)
        self.dataku[self.kolom[2]] = self.dataku[self.kolom[1]].apply(self.konversi.int_bin)
        
        
        return

    def urutkan_data(self, df, berdasarkan_kolom="biner"):
        a = df[berdasarkan_kolom].value_counts()
        return a

    # ------------------- kompresi 1-----------------
    def fit_fibonaci(self, berdasarkan_kolom="biner"): # fit
        a = self.dataku[berdasarkan_kolom].value_counts().index.values
        n = a.shape[0]
        b = np.array([self.codeword.fibonaci(x) for x in range(1, n+1)])

        assert n==len(b), "panjang kedua data tidak sesuai"

        self.encode_fib = {i: v for i,v in list(zip(a, b))}
        self.decode_fib = {v: k for k, v in self.encode_fib.items()}

        self.decode_fib_s = pd.Series(self.decode_fib)
        self.kode[self._key[2]] = self.decode_fib
        
    
        # map = {item[key]: item[value] for item in dict_list}
        # reverse_map = inverse_dict(map)
    
        # return map, reverse_map
        return self

    def transformasi_fib(self, berdasarkan_kolom="biner"):
        self.dataku[berdasarkan_kolom] = self.dataku[berdasarkan_kolom].apply(lambda x: self.encode_fib[x])

        self.kode[self._key[0]] = self.dataku[berdasarkan_kolom].apply(lambda x: len(x)).tolist() # hitung bit
        self.indeks1_np = np.array(self.kode[self._key[0]])

        self.dict_kompresi1 = self.gabung_string_biner(self.dataku[berdasarkan_kolom])
        self.kompresi1 = self.dict_kompresi1["string_biner"]
        
        return self
    # ------------------- end kompresi 1-----------------
        

    # -------------------  kompresi 2-----------------
    def fit_levenstein(self, berdasarkan_kolom="biner"): # fit
        a = self._dataku[berdasarkan_kolom].value_counts().index.values
        n = a.shape[0]
        b = np.array([self.codeword.levenstein(x) for x in range(0, n)])

        assert n==len(b), "panjang kedua data tidak sesuai"

        self.encode_lev = {i: v for i,v in list(zip(a, b))}
        self.decode_lev = {v: k for k, v in self.encode_lev.items()}
        
        self.kode[self._key[3]] = self.decode_lev
        self.decode_fib_s = pd.Series(self.decode_lev)
        
        # map = {item[key]: item[value] for item in dict_list}
        # reverse_map = inverse_dict(map)
    
        # return map, reverse_map
        return self

    def transformasi_lev(self, berdasarkan_kolom="biner"):
        self._dataku[berdasarkan_kolom] = self._dataku[berdasarkan_kolom].apply(lambda x: self.encode_lev[x])
        
        self.kode[self._key[1]] = self._dataku[berdasarkan_kolom].apply(lambda x: len(x)).tolist() # hitung bit
        self.indeks2_np = np.array(self.kode[self._key[1]])
        
        # self.kompresi2 = self.konversi.list_str(self._dataku[berdasarkan_kolom].tolist())
        self.dict_kompresi2 = self.gabung_string_biner(self._dataku[berdasarkan_kolom])
        self.kompresi2 = self.dict_kompresi2["string_biner"]
        
        return self
    # ------------------- end kompresi 2-----------------

    def inverse_transformasi_fib(self, berdasarkan_kolom="biner"):
        self.dataku[berdasarkan_kolom] = self.dataku[berdasarkan_kolom].apply(lambda x: self.decode_fib[x])
        
        return self

    def inverse_transformasi_lev(self, berdasarkan_kolom="biner"):
        self._dataku[berdasarkan_kolom] = self.dataku[berdasarkan_kolom].apply(lambda x: self.decode_lev[x])
        
        return self

    # padding dan flagging
    def padding_flag(self, string_biner, jumlah_bit=8):   # update self._string_biner
        # string_biner = self.kompresi1
        n = len(string_biner)
        sisa_bagi = n % jumlah_bit
        
        # assert n >= 8, "panjang string binernya kurang dari 8"
    
        if sisa_bagi == 0:
            self._string_biner = string_biner
        else:
            padding = "0" * (7-sisa_bagi) + "1"   # rumus: 7 - sisa_bagi + "1"
            flag = 9 - sisa_bagi                  # rumus: 9 - sisa_bagi
            flag = format(flag, '08b')
    
            self._string_biner = string_biner + padding + flag

        return self
    
    # padding dan flagging decode
    def padding_flag_decode(self, string_biner, n_awal):
        hasil = string_biner[0:n_awal]
        return hasil

    def menyusun_ulang_8bit(self, string="", n=8, pemisah="-") -> str:
        # string = self._string_biner
        assert len(string) >= 8, "string terlalu sedikit"
        result = ''
        no = 0
        for i, char in enumerate(string, 1):
            if char=="0" or char=="1":
                no += 1
                
            result += char
            if (no % n == 0) and (result[-2] != pemisah) and (len(string) != i):
                result += pemisah

        # update _strng_biner
        self._string_biner = result

        # update _dataku
        self._dataku = pd.DataFrame()  # menyusun ulang
        self._dataku[self.kolom[2]] = self.konversi.str_list(result, pemisah="-")
        # self._dataku[self.kolom[2]] = self._dataku["x"].apply(lambda x: x.replace(",", ""))
        self._dataku[self.kolom[0]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_hex)        
        self._dataku[self.kolom[1]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_int)        
        
        return self

    def hitung_bit(self, df):
        hasil = df[self.kolom[2]].apply(lambda x: len(x))
        return hasil

    # def simpan_hasil_kompresi(self, teks="", nama_file="hasil_kompresi.txt"):
    #     with open(nama_file, "w", encoding="utf-8") as file:
    #         file.write(teks)
    #     return self

    def simpan_kompresi(self, nama_file="hasil_kompresi.txt"):
        # # cara 1
        # a = self._dataku[self.kolom[2]]
        # with open(nama_file, 'wb') as file:
        #     np.save(file, a, allow_pickle=True)

        # cara 2
        a = self._dataku[self.kolom[1]].to_numpy(dtype=np.uint8).tobytes()
        with open(nama_file, 'wb') as file:
            file.write(a)
            
        return self

    def simpan_kode(self, nama_kode="kode.txt"):
        # kode = self.dict_kompresi2["indeks"].tolist()
        kode = self.kode
        teks_kode = self.konversi.objek_encode(kode)
        
        with open(nama_kode, 'w') as file:
            file.write(teks_kode)
        return self

    def load_file(self, nama_file="hasil_kompresi.txt"):
        with open(nama_file, 'rb') as file:
            d = np.load(file, allow_pickle=True)
        return d

    # def simpan_kompresi1(self, nama_file="hasil_kompresi1.txt"):
    #     pass

    def menyusun_ascii(self):
        self._dataku[self.kolom[4]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_ascii)
        return self

class Informasi:
    def __init__(self):
        pass

    def ukuran_file(self, file_path):
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            size_kb = size / 1024  # mengkonversi ukuran menjadi satuan kb
            return round(size_kb, 2)
        else:
            raise Exception("file tidak tersedia")
        return self
    
    def ukuran_df(self, df):
        return round(df.shape[0] / 1024, 2)

class Dekompresi:
    def __init__(self):
        self.dataku = pd.DataFrame()
        self._dataku = pd.DataFrame()
        self.konversi = Konversi()
        
        self._string_biner = ""
        
        # kode
        self._key = ["indeks1", "indeks2", "decode_fib", "decode_lev"]
        # self.kode = {
        #     self._key[0]: [],
        #     self._key[1]: [],
        #     self._key[2]: {},
        #     self._key[3]: {},
        # }
        self.kode = {}

        self.kolom = ["hexa", "integer", "biner", "frekuensi", "ascii"]

    def load_file(self, nama_file="hasil_kompresi.txt", update=True):
        if not nama_file:
            raise ValueError("file path tidak boleh kosong")
            
        with open(nama_file, 'rb') as file:
            # hasil = np.load(file, allow_pickle=True)  # cara 1 penyimpanan (di kelas Kompresi) 
            hasil = np.frombuffer(file.read(), dtype=np.uint8)  # cara 2 penyimpanan (di kelas kompresi()

        # with open(file_path, "rb") as file:
        #     self.biner_file = file.read()
        #     self.integer_file = np.frombuffer(self.biner_file, dtype=np.uint8)

        # cara 1
        # self.dataku[self.kolom[1]] = hasil
        # self.dataku[self.kolom[1]] = self.dataku[self.kolom[2]].apply(self.konversi.bin_int)
        # self.dataku[self.kolom[0]] = self.dataku[self.kolom[1]].apply(self.konversi.int_hex)

        # cara 2
        self.dataku[self.kolom[1]] = hasil
        self.dataku[self.kolom[0]] = self.dataku[self.kolom[1]].apply(self.konversi.int_hex)
        self.dataku[self.kolom[2]] = self.dataku[self.kolom[1]].apply(self.konversi.int_bin)

        if update:
            # update
            my_list = self.dataku[self.kolom[2]].tolist()
            self._string_biner = self.konversi.list_str(my_list).replace(",", "")
        else:
            pass
        
        return self

    def load_file_from_bt(self, data_bytes=None, update=True):
        if not data_bytes:
            raise ValueError("data_bytes tidak boleh kosong")

        hasil = np.frombuffer(data_bytes, dtype=np.uint8)
            
        # cara 2
        self.dataku[self.kolom[1]] = hasil
        self.dataku[self.kolom[0]] = self.dataku[self.kolom[1]].apply(self.konversi.int_hex)
        self.dataku[self.kolom[2]] = self.dataku[self.kolom[1]].apply(self.konversi.int_bin)

        if update:
            # update
            my_list = self.dataku[self.kolom[2]].tolist()
            self._string_biner = self.konversi.list_str(my_list).replace(",", "")
        else:
            pass
        
        return self


    def set_string_biner(self, list_int):
        """
        params
        ------
        list_int: numpy array 1D

        return
        ------
        """
        my_list = list_int.tolist()
        self._string_biner = self.konversi.list_str(my_list, pemisah="")
        return self

    def load_kode(self, nama_kode="kode.txt"):
        with open(nama_kode, "r") as file:
            string_kode = file.read()

        # update kode
        self.kode = self.konversi.objek_decode(string_kode)
        
        return self

    # padding dan flagging decode
    def padding_flag_decode(self, string_biner, fib=True, auto_kode=True, kode=None):
        if auto_kode:
            if fib:
                n_awal = sum(self.kode[self._key[0]])
            else:
                n_awal = sum(self.kode[self._key[1]])
        else:
            assert kode is not None, "kode tidak bisa kosong"
            
            if fib:
                n_awal = sum(kode[self._key[0]])
            else:
                n_awal = sum(kode[self._key[1]])
                
        hasil = string_biner[0:n_awal]    
        self._string_biner = hasil
        
        return self

    def menyusun_ulang(self, fib=True, auto_kode=True, kode=None):   # kebalikan dari mengusun ulang
        # indeks = dict_kompresi["indeks"]
        # s = dict_kompresi["string_biner"]

        if auto_kode:
            if fib:
                indeks = self.kode[self._key[0]]
            else:
                indeks = self.kode[self._key[1]]
        else:
            assert kode is not None, "kode tidak boleh kosong"
            if fib:
                indeks = kode[self._key[0]]
            else:
                indeks = kode[self._key[1]]
            
        s = self._string_biner
        
        n = len(indeks)
        s_baru = np.empty(n, dtype=object)
        
        
        awal = 0
        akhir = 0
        for i in range(0, n):
            if i>0:
                awal = akhir
        
            if i < n-1:
                akhir += indeks[i]
                # print(indeks[i] + indeks[i+1])
            else:
                akhir = sum(indeks)
            
            # print(f"{awal} {akhir}")
            s_baru[i] = s[awal:akhir]


        # reset self._dataku
        self._dataku = pd.DataFrame()

        self._dataku[self.kolom[2]] = pd.Series(s_baru)
        # self._dataku[self.kolom[0]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_int)
        
        return self

    def dekompresi(self, fib=True, auto_kode=True, kode=None):
        if auto_kode:
            if fib:
                decode_fib = self.kode[self._key[2]]
                self._dataku[self.kolom[2]] = self._dataku[self.kolom[2]].apply(lambda x: decode_fib[x])
                self._dataku[self.kolom[0]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_hex)
                self._dataku[self.kolom[1]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_int)
            else:
                decode_lev = self.kode[self._key[3]]
                self._dataku[self.kolom[2]] = self._dataku[self.kolom[2]].apply(lambda x: decode_lev[x])
                self._dataku[self.kolom[0]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_hex)
                self._dataku[self.kolom[1]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_int)
        else:
            assert kode is not None, "kode tidak boleh kosong"
            if fib:
                decode_fib = kode[self._key[2]]
                self._dataku[self.kolom[2]] = self._dataku[self.kolom[2]].apply(lambda x: decode_fib[x])
                self._dataku[self.kolom[0]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_hex)
                self._dataku[self.kolom[1]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_int)
            else:
                decode_lev = kode[self._key[3]]
                self._dataku[self.kolom[2]] = self._dataku[self.kolom[2]].apply(lambda x: decode_lev[x])
                self._dataku[self.kolom[0]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_hex)
                self._dataku[self.kolom[1]] = self._dataku[self.kolom[2]].apply(self.konversi.bin_int)
    
        
        self._string_biner = self.konversi.list_str(self._dataku[self.kolom[2]], "")
            
        return self

    def simpan_hasil(self, nama_file="hasil_kompresi.pdf"):
        data_bytes = self._dataku[self.kolom[1]].to_numpy(dtype=np.uint8).tobytes()
        with open(nama_file, "wb") as file:
            file.write(data_bytes)
            
        return self

    

class Mydata:
    def __init__(self):
        self._kolom = ["hexa", "bilangan", "biner", "frekuensi", "ascii"]
        self.df = pd.DataFrame()
        self.konversi = Konversi()

    def baca_data(self, nama_file="sampel1.pdf"):
        with open(nama_file, "rb") as file:
            bilangan = np.frombuffer(file.read(), dtype=np.uint8)

        self.df[self._kolom[1]] = bilangan
        self.df[self._kolom[0]] = self.df[self._kolom[1]].apply(self.konversi.int_hex)
        self.df[self._kolom[2]] = self.df[self._kolom[1]].apply(self.konversi.int_bin)
        return self

    def baca_data_dari_numpy(self, x):
        self.df[self._kolom[1]] = x
        self.df[self._kolom[0]] = self.df[self._kolom[1]].apply(self.konversi.int_hex)
        self.df[self._kolom[2]] = self.df[self._kolom[1]].apply(self.konversi.int_bin)
        return self
        

    def simpan_data(self):
        pass

class Langkah:
    def __init__(self, data):
        self.data = data
        self.kode = {}
        self.hasil_kompresi_np = np.array([], dtype=np.uint8)
        self.indeks = []

        self.ukuran_awal = round(data.df.shape[0]/1024, 2)
        self.ukuran_setelah_kompresi = 0
        self.informasi = Informasi()
        
        # evaluasi
        self.evaluasi = Evaluasi()
        self.rc = 0.0
        self.cr = 0.0
        self.ss = 0.0

        # hasil komporesi bytes
        self.hasil_kompresi_bt = None

    def langka1(self, jumlah_potongan=16):
        potongan = jumlah_potongan
        sisa_bagi = self.data.df.shape[0] % potongan
        # n = self.data.df.shape[0] - sisa_bagi
        n = self.data.df.shape[0]

        nomor = 1
        kode = {}
        for i in range(0, n, potongan):
            sampel = self.data.df.hexa[i:i+potongan]
            obj = Kompresi()

            # ----------------mulai-----------------
            obj.input_data_hexa(sampel, s=False)
        
            obj.fit_fibonaci().transformasi_fib()    # kompresi pertama
            obj.padding_flag(obj.kompresi1)
            obj.menyusun_ulang_8bit(string=obj._string_biner)
        
            obj.fit_levenstein()
            obj.transformasi_lev()    # kompresi kedua
            obj.padding_flag(obj.kompresi2)
            obj.menyusun_ulang_8bit(string=obj._string_biner)
        
            obj.menyusun_ascii()
            # ----------------selesai-----------------

            kode[nomor] = obj.kode

            alat = Alat()

            a = obj._dataku[obj.kolom[1]].to_numpy(dtype=np.uint8)
            self.hasil_kompresi_np = np.concatenate([self.hasil_kompresi_np, a])
            self.indeks.append(a.shape[0])
            

            nomor += 1

        self.kode = kode

        
        return self

    def langka2(self, nama_file="hasil_kompresi.txt", nama_kode="kode.txt"):
        kode = self.kode
        konversi = Konversi()
        teks_kode = konversi.objek_encode(kode)

        # simpan ukuran data setelah di kompresi
        self.ukuran_setelah_kompresi = self.informasi.ukuran_df(self.hasil_kompresi_np)

        # evaluasi
        self.rc = self.evaluasi.hitung_rc(self.ukuran_awal, self.ukuran_setelah_kompresi)
        self.cr = self.evaluasi.hitung_cr(self.ukuran_awal, self.ukuran_setelah_kompresi)
        self.ss = self.evaluasi.hitung_ss(self.ukuran_awal, self.ukuran_setelah_kompresi)

        # update data bytes
        self.hasil_kompresi_bt = self.hasil_kompresi_np.tobytes()

        # simpan kode
        with open(nama_kode, 'w') as file:
            file.write(teks_kode)

        # simpan indeks
        nama_index = "index.txt"
        a = np.array(self.indeks)
        a.tofile(nama_index)
        
        #simpan hasil kompresi
        a = self.hasil_kompresi_np.tobytes()
        with open(nama_file, 'wb') as file:
            file.write(a)

        return self

class Tahapan_dekompresi:
    def __init__(self):
        self.hasil_dekompresi_bt = None

    def langka3(self, data_bytes=None, nama_index="index.txt", nama_kode=""):
        obj_dek = Dekompresi()

        obj_dek.load_file_from_bt(data_bytes, update=False)

        # obj_dek.load_file(nama_file, update=False)
        obj_dek.load_kode()

        b = np.fromfile(nama_index, dtype=np.uint32)
        index = b.tolist()

        alat = Alat()

        c = alat.pisahkan_list(obj_dek.dataku.integer.to_numpy(), index)
        
        # ---------------------mulai-------------------
        list_integer = np.array([], dtype=np.uint8)
        for i, v in obj_dek.kode.items():
            # print(int(i))
            biner = pd.Series(c[int(i)-1]).apply(obj_dek.konversi.int_bin)
            obj_dek.set_string_biner(biner.to_numpy())
            obj_dek.padding_flag_decode(obj_dek._string_biner, fib=False, auto_kode=False, kode=v)
            obj_dek.menyusun_ulang(fib=False, auto_kode=False, kode=v)
            obj_dek.dekompresi(fib=False, auto_kode=False, kode=v)
            obj_dek.padding_flag_decode(obj_dek._string_biner, fib=True, auto_kode=False, kode=v)
            obj_dek.menyusun_ulang(fib=True, auto_kode=False, kode=v)
            obj_dek.dekompresi(fib=True, auto_kode=False, kode=v)
            
            # print(obj_dek._dataku)
            list_integer = np.concatenate([list_integer, obj_dek._dataku[obj_dek.kolom[1]].to_numpy(dtype=np.uint8)])

        # simpan hasil dekompresi
        # nama_file = "hasil_dekompresi.pdf"
        data_bytes = list_integer.tobytes()
        self.hasil_dekompresi_bt = data_bytes   # simpan data bytes hasil dekompresi
        # with open(nama_file, "wb") as file:
        #     file.write(data_bytes)
            
        return self