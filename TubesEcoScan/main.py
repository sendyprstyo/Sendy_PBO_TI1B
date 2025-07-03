from konversi import baca_csv, konversi_ke_objek
from peta import buat_peta
import logging

def setup_logging(nama_file_log="log_aksi.log"):
    logging.basicConfig(
        filename=nama_file_log,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

setup_logging()
print("\n--- EcoScan: Visualisasi Data TPS ---")

df = baca_csv("data_tps_sampah.csv")
if df is not None:
    daftar_laporan = konversi_ke_objek(df)
    logging.info(f"Berhasil memproses {len(daftar_laporan)} titik TPS")
    buat_peta(daftar_laporan)
    logging.info("Peta berhasil dibuat dan disimpan.")
else:
    logging.error("Gagal membaca file CSV.")
