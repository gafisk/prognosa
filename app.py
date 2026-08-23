import re
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import sklearn
from utils import hitung_p5, hitung_p6, hitung_p7, hitung_p9, hitung_p11
from connections.connections import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    hasil_prediksi = None
    if request.method == 'POST':
        # Nama
        nama = request.form.get('nama')
        # P1
        p1 = int(request.form.get('p1'))
        # P2
        p2 = int(request.form.get('p2'))
        # P3
        p3 = int(request.form.get('p3'))
        # P4
        p4 = int(request.form.get('p4'))
        # P5
        p5 = hitung_p5(request.form)
        # P6
        p6 = hitung_p6(request.form)
        # P7
        p7 = hitung_p7(request.form)
        # P9
        p9 = hitung_p9(request.form)
        # p10
        p10 = int(request.form.get('p10'))
        # p11
        p11 = hitung_p11(request.form)
        # p12
        p12 = int(request.form.get('p12'))
        
        # Belum ada
        p8 = 0
        p13 = 0
        prediksi = 1

        # =========================
        # PREDIKSI SEMENTARA
        # =========================

        if prediksi == 1:
            hasil_prediksi = "Prediksi Benar"
        else:
            hasil_prediksi = "Prediksi Tidak Benar"
        
        # =========================
        # SIMPAN KE DATABASE
        # =========================

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO prediksi (
                    nama, usia, paritas, riwayat_hipertensi, riwayat_pe_keluarga,
                    pola_istirahat, pola_makan, obesitas, pola_aktivitas,
                    stress, diabetes, jarak_hamil, gemelli, alkohol, prediksi
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                nama, p1, p2, p3, p4,
                p5, p6, p7, p8,
                p9, p10, p11, p12, p13, prediksi
            ))

            connection.commit()

        finally:

            cursor.close()
            connection.close()


        # =========================
        # DEBUG
        # =========================

        print("=== DATA PREDIKSI ===")
        print("Nama:", nama)
        print("Usia:", p1)
        print("Paritas:", p2)
        print("Riwayat Hipertensi:", p3)
        print("Riwayat Preeklampsia Keluarga:", p4)
        print("Pola Istirahat:", p5)
        print("Pola Makan:", p6)
        print("Obesitas:", p7)
        print("Pola Aktivitas:", p8 , "masih belum")
        print("Stres:", p9)
        print("Diabetes:", p10)
        print("Jarak Kehamilan:", p11)
        print("Gemelli:", p12)
        print("Alkohol:", p13 , "masih belum")
        print("Prediksi:", prediksi)
        

    return render_template("prediksi.html", hasil_prediksi=hasil_prediksi)

@app.route('/api/prediksi', methods=['GET'])
def api_prediksi():

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM prediksi
            ORDER BY id DESC
        """)

        data = cursor.fetchall()

        return jsonify({
            "status": True,
            "data": data
        })

    except Exception as e:

        return jsonify({
            "status": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)