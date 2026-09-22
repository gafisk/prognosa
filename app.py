import re
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import sklearn
from utils import hitung_p1, hitung_p5, hitung_p6, hitung_p7, hitung_p9, hitung_p11
from connections.connections import get_connection

app = Flask(__name__)

model = joblib.load("models/lr_model.pkl")
scaler = joblib.load("models/lr_scaler.pkl")

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
        p1 = hitung_p1(request.form)
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
        # p13
        p13 = int(request.form.get('p13'))
        
        X = pd.DataFrame([{
            'Usia': p1,
            'Paritas': p2,
            'Riwayat_Hipertensi': p3,
            'Riwayat_PE_Keluarga': p4,
            'Pola_Istirahat': p5,
            'Pola_Makan': p6,
            'Obesitas': p7,
            'Stress': p9,
            'Diabetes': p10,
            'Jarak_Hamil': p11,
            'Gemelli': p12,
            'Alkohol': p13
        }])
        
        # =========================
        # SCALED
        # =========================
                
        X_scaled = scaler.transform(X)

        # =========================
        # PREDIKSI
        # =========================

        prediksi = model.predict(X_scaled)[0]

        if prediksi == 1:
            hasil_prediksi = "Risiko Tinggi"
        else:
            hasil_prediksi = "Risiko Rendah"
        
        # =========================
        # SIMPAN KE DATABASE
        # =========================

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO prediksi (
                    nama, usia, paritas, riwayat_hipertensi, riwayat_pe_keluarga,
                    pola_istirahat, pola_makan, obesitas, stress, diabetes, 
                    jarak_hamil, gemelli, alkohol, prediksi
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                nama, p1, p2, p3, p4, p5, p6, p7, 
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
        print("Stres:", p9)
        print("Diabetes:", p10)
        print("Jarak Kehamilan:", p11)
        print("Gemelli:", p12)
        print("Alkohol:", p13)
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