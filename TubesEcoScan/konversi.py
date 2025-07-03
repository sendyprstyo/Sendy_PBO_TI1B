import pandas as pd
from model import SampahOrganik  # ⬅️ tambahkan ini

def baca_csv(nama_file):
    return pd.read_csv(nama_file)

def konversi_ke_objek(df):
    list_objek = []
    for idx, row in df.iterrows():
        lokasi = (row["Latitude"], row["Longitude"])
        alamat = row["Alamat"]
        kecamatan = row["Kecamatan"]
        keterangan = row["Keterangan"]

        deskripsi = f"{alamat}, Kec. {kecamatan}<br>{keterangan}"
        waktu = "2025-06-19"
        id_laporan = f"L{idx+1:03}"

        obj = SampahOrganik(
            id_laporan=id_laporan,
            lokasi=lokasi,
            deskripsi=deskripsi,
            waktu=waktu
        )
        list_objek.append(obj)

    return list_objek
