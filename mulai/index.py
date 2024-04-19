import functools
import os
import numpy as np
import pandas as pd

import time

from .kompresi import modulku, tkp

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, send_file, send_from_directory, make_response)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# api
from flask_restful import Resource, Api

bp = Blueprint('mulai', __name__, url_prefix='/mulai')

api = Api(bp)

# -------------------------------------------- api -----------------
class Mulai_kompres(Resource):
    def get(self):
        return {"pesan": "selamat datang"}
    
    def post(self):
        start = time.time()
        file = request.files.get("mydata")
        file_content = np.frombuffer(file.read(), dtype=np.uint8)

        aplikasiku = tkp.Aplikasiku()
        aplikasiku.tahap1(file=file_content, dari_numpy=True)
        aplikasiku.tahap2(simpan_bt=True)

        end = time.time()

        # simpan data bytes ke session
        session["hasil_kompresi"] = aplikasiku.hasil_bt
        # print(len(session["hasil_kompresi"]))

        dataku = {"data1": []}
        informasi = {
            "ukuran_awal": aplikasiku.info.ukuran_sebelum,
            "ukuran_setelah": aplikasiku.info.ukuran_setelah,
            "nilai_cr": aplikasiku.info.nilai_cr,
            "nilai_rc": aplikasiku.info.nilai_rc,
            "nilai_ss": aplikasiku.info.nilai_ss,
            "waktu" : round(end - start, 2)
        }
        
        return jsonify({
            "data": dataku,
            "informasi": informasi,
            "status": "sukses",
            "pesan": "data berhasil di proses"
        })


        # --------------------------end revisi------------------------

        # start = time.time()

        # file = request.files.get("mydata")
        # file_content = np.frombuffer(file.read(), dtype=np.uint8)
        # data1 = modulku.Mydata()
        # data1.baca_data_dari_numpy(file_content)
        # tahapan = modulku.Langkah(data1)
        # tahapan.langka1()
        # tahapan.langka2()

        # end = time.time()

        # session.clear()

        # # simpan data bytes ke session
        # session["hasil_kompresi"] = tahapan.hasil_kompresi_bt
        # print(len(session["hasil_kompresi"]))

        # dataku = {"data1": data1.df.head(10).to_json(orient='records')}
        # informasi = {
        #     "ukuran_awal": tahapan.ukuran_awal,
        #     "ukuran_setelah": tahapan.ukuran_setelah_kompresi,
        #     "nilai_cr": tahapan.cr,
        #     "nilai_rc": tahapan.rc,
        #     "nilai_ss": tahapan.ss,
        #     "waktu" : round(end - start, 2)
        # }
        
        # return jsonify({
        #     "data": dataku,
        #     "informasi": informasi,
        #     "status": "sukses",
        #     "pesan": "data berhasil di proses"
        # })
    
class DownloadFile(Resource):
    def get(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        # df.to_csv('sample.csv', index=False)
        # return send_file('db.py', as_attachment=True)
        # return {'status': 'berhasil'}

        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        print("response adalah dibawah ini")
        return resp
    
class Dekompresi_file(Resource):
    def post(self):
        file = request.files.get("my_file")
        file_content = np.frombuffer(file.read(), dtype=np.uint8)

        aplikasiku2 = tkp.Aplikasiku()
        aplikasiku2.tahap3(dari_numpy=True, file=file_content)
        aplikasiku2.tahap4(simpan_bt=True)

        session.pop("hasil_dekompresi", None)
            
        # # simpan data bytes ke session
        session["hasil_dekompresi"] = aplikasiku2.hasil_bt

        # ------------------revisi------------------

        # tahapan_dekompresi = modulku.Tahapan_dekompresi()
        # tahapan_dekompresi.langka3(data_bytes=file)

        # filename = "hasilnya_dekompresi.pdf"
        # data_bytes = tahapan_dekompresi.hasil_dekompresi_bt

        # session.pop("hasil_dekompresi", None)
            
        # # simpan data bytes ke session
        # session["hasil_dekompresi"] = tahapan_dekompresi.hasil_dekompresi_bt

        # return ke alamat lain
        return redirect(url_for('mulai.downloadhasildekompresi'))

        # response = make_response(data_bytes)
        # response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        
        # print("file data: ")
        # print(data_bytes)

        # return {"pesan": "berhasil"}
        # return send_from_directory(directory, nama_file, as_attachment=True)
        # return response
    
class DownloadHasilKompresi(Resource):
    def get(self):
        filename = "hasil_kompresi.pdf"

        # print("hasil kompresi")
        # print(session["hasil_kompresi"])

        data_bytes = session["hasil_kompresi"]

        response = make_response(data_bytes)
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        
        # print("file data: ")
        # print(data_bytes)

        # return {"pesan": "berhasil"}
        # return send_from_directory(directory, nama_file, as_attachment=True)
        return response

class DownloadHasilDekompresi(Resource):
    def get(self):
        if 'hasil_dekompresi' not in session:
            raise Exception("tidak ada nama di sesion")
        
        filename = "hasil_dekompresi.pdf"

        # print("hasil kompresi")
        # print(session["hasil_kompresi"])

        data_bytes = session["hasil_dekompresi"]

        response = make_response(data_bytes)
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        
        # print("file data: ")
        # print(data_bytes)

        # return {"pesan": "berhasil"}
        # return send_from_directory(directory, nama_file, as_attachment=True)
        return response

api.add_resource(Mulai_kompres, '/mulaikompresi')
api.add_resource(DownloadFile, '/downloadfile')
api.add_resource(Dekompresi_file, '/dekompresifile')
api.add_resource(DownloadHasilKompresi, '/downloadhasilkompresi')
api.add_resource(DownloadHasilDekompresi, '/downloadhasildekompresi')

# -------------------------------------------- end api -----------------

@bp.route('', methods=["GET", "POST"])
def halaman_mulai():
    if request.method == 'POST':
        print("selamat ini adalah post")
        file = request.files.get("mydata")
        file_content = np.frombuffer(file.read(), dtype=np.uint8)

        data1 = modulku.Mydata()
        data1.baca_data_dari_numpy(file_content)
        tahapan = modulku.Langkah(data1)
        tahapan.langka1()


    nama= "budi"
    context = {
        "nama": nama
    }
    return render_template("mulai/index.html", **context)

