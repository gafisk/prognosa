from datetime import datetime


def hitung_p5(data):

    # ==========================================
    # 1. KUALITAS TIDUR SUBJEKTIF
    # ==========================================
    p5_kualitas = int(data.get('p5_kualitas'))


    # ==========================================
    # 2. LATENSI TIDUR
    # Item 2 + Item 3 → rata-rata
    # ==========================================
    p5_latensi = int(data.get('p5_latensi'))
    p5_kesulitan_tidur = int(data.get('p5_kesulitan_tidur'))

    skor_latensi = (
        p5_latensi + p5_kesulitan_tidur
    ) / 2


    # ==========================================
    # 3. DURASI TIDUR
    # ==========================================
    p5_durasi = int(data.get('p5_durasi'))


    # ==========================================
    # 4. EFISIENSI TIDUR
    # ==========================================
    jam_tidur = data.get('p5_jam_tidur')
    jam_bangun = data.get('p5_jam_bangun')
    tidur_nyenyak = float(data.get('p5_tidur_nyenyak'))

    waktu_tidur = datetime.strptime(
        jam_tidur,
        '%H:%M'
    )

    waktu_bangun = datetime.strptime(
        jam_bangun,
        '%H:%M'
    )

    # Jika bangun lebih kecil dari jam tidur,
    # berarti tidur melewati tengah malam
    if waktu_bangun <= waktu_tidur:
        from datetime import timedelta
        waktu_bangun += timedelta(days=1)

    total_di_tempat_tidur = (
        waktu_bangun - waktu_tidur
    ).total_seconds() / 3600

    # Efisiensi tidur
    efisiensi = (
        tidur_nyenyak / total_di_tempat_tidur
    ) * 100


    # Konversi efisiensi menjadi skor 0–3
    if efisiensi >= 85:
        skor_efisiensi = 0
    elif efisiensi >= 75:
        skor_efisiensi = 1
    elif efisiensi >= 65:
        skor_efisiensi = 2
    else:
        skor_efisiensi = 3


    # ==========================================
    # 5. GANGGUAN TIDUR
    # 7 ITEM → RATA-RATA
    # ==========================================
    gangguan = [
        int(data.get('p5_gangguan_a')),
        int(data.get('p5_gangguan_b')),
        int(data.get('p5_gangguan_c')),
        int(data.get('p5_gangguan_d')),
        int(data.get('p5_gangguan_e')),
        int(data.get('p5_gangguan_f')),
        int(data.get('p5_gangguan_g'))
    ]

    skor_gangguan = sum(gangguan) / 7


    # ==========================================
    # 6. PENGGUNAAN OBAT TIDUR
    # ==========================================
    p5_obat_tidur = int(data.get('p5_obat_tidur'))


    # ==========================================
    # 7. GANGGUAN FUNGSI SIANG HARI
    # 2 ITEM → RATA-RATA
    # ==========================================
    siang = [
        int(data.get('p5_siang_1')),
        int(data.get('p5_siang_2'))
    ]

    skor_siang = sum(siang) / 2


    # ==========================================
    # TOTAL SKOR
    # ==========================================
    skor_p5 = (
        p5_kualitas +
        skor_latensi +
        p5_durasi +
        skor_efisiensi +
        skor_gangguan +
        p5_obat_tidur +
        skor_siang
    )


    # ==========================================
    # KLASIFIKASI
    # ==========================================
    if skor_p5 > 5:
        p5 = 1
    else:
        p5 = 0


    return p5

def hitung_p6(data):

    skor_risiko = (
        int(data.get('p6_1')) +
        int(data.get('p6_2')) +
        int(data.get('p6_3')) +
        int(data.get('p6_4')) +
        int(data.get('p6_5')) +
        int(data.get('p6_6')) +
        int(data.get('p6_7')) +
        int(data.get('p6_8')) +
        int(data.get('p6_16'))
    )
    
    skor_protektif = (
        int(data.get('p6_9')) +
        int(data.get('p6_10')) +
        int(data.get('p6_11')) +
        int(data.get('p6_12')) +
        int(data.get('p6_13')) +
        int(data.get('p6_14')) +
        int(data.get('p6_15')) +
        int(data.get('p6_17'))
    )

    skor_akhir = skor_risiko - skor_protektif

    if skor_akhir > 10:
        p6 = 1
    else:
        p6 = 0

    return p6

def hitung_p7(data):

    berat_badan = data.get('p7_berat_badan')
    tinggi_badan = data.get('p7_tinggi_badan')

    if not berat_badan or not tinggi_badan:
        return None

    berat_badan = float(berat_badan)
    tinggi_badan = float(tinggi_badan)

    # cm → meter
    tinggi_meter = tinggi_badan / 100

    # IMT
    bmi = berat_badan / (tinggi_meter ** 2)

    # Obesitas
    if bmi >= 30:
        p7 = 1
    else:
        p7 = 0

    return p7

def hitung_p9(data):

    skor = (
        int(data.get('p9_1')) +
        int(data.get('p9_2')) +
        int(data.get('p9_3')) +
        int(data.get('p9_4')) +
        int(data.get('p9_5')) +
        int(data.get('p9_6')) +
        int(data.get('p9_7'))
    )

    # DASS-21 → dikalikan 2
    skor_total = skor * 2

    # Klasifikasi
    if skor_total > 18:
        p9 = 1
    else:
        p9 = 0

    return p9

def hitung_p11(data):

    jarak = float(data.get('p11'))

    if jarak < 2 or jarak > 5:
        p11 = 1
    else:
        p11 = 0

    return p11

