import streamlit as st
import pandas as pd
import os
from datetime import datetime
import folium
import streamlit.components.v1 as components

# --- Konstanta file ---
FILE_PATH = "data_tps_sampah.csv"
MAP_FILE = "peta_tps.html"

# --- Load data ---
def load_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        if "Status" not in df.columns:
            df["Status"] = "Dilaporkan"
        if "Waktu Lapor" not in df.columns:
            df["Waktu Lapor"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df
    else:
        return pd.DataFrame(columns=[
            "Nama TPS", "Latitude", "Longitude", "Keterangan",
            "Alamat", "Kecamatan", "Status", "Waktu Lapor"
        ])

# --- Save data ---
def save_data(df):
    df.to_csv(FILE_PATH, index=False)

# --- Buat peta ---
def buat_peta(dataframe, file_output=MAP_FILE):
    peta = folium.Map(location=[-6.990, 110.420], zoom_start=12)
    for _, row in dataframe.iterrows():
        popup_text = f"<b>{row['Nama TPS']}</b><br>{row['Alamat']}<br>Kec. {row['Kecamatan']}<br>Status: {row['Status']}"
        warna = (
            "green" if row["Status"] == "Selesai"
            else "orange" if row["Status"] == "Ditangani"
            else "red"
        )
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup_text,
            icon=folium.Icon(color=warna)
        ).add_to(peta)
    peta.save(file_output)

# --- Load awal ---
df = load_data()
df["Waktu Lapor"] = pd.to_datetime(df["Waktu Lapor"], errors="coerce")
buat_peta(df)

# --- Layout ---
st.set_page_config(page_title="EcoScan", layout="wide")
st.title("📍 EcoScan - Pantau Lokasi TPS Kota Semarang")

# --- Peta Interaktif ---
st.subheader("🗺️ Peta Interaktif TPS")
components.html(open(MAP_FILE, "r", encoding="utf-8").read(), height=500)

# --- Tambah TPS ---
st.subheader("➕ Tambah Titik TPS")
with st.form("form_tambah"):
    nama = st.text_input("Nama TPS")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    alamat = st.text_input("Alamat Lengkap")
    kecamatan = st.selectbox("Kecamatan", options=sorted(df["Kecamatan"].unique()) if not df.empty else [])
    keterangan = st.text_area("Keterangan")
    submitted = st.form_submit_button("Tambah")

    if submitted and nama and alamat and keterangan:
        new_data = {
            "Nama TPS": nama,
            "Latitude": lat,
            "Longitude": lon,
            "Keterangan": keterangan,
            "Alamat": alamat,
            "Kecamatan": kecamatan,
            "Status": "Dilaporkan",
            "Waktu Lapor": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        save_data(df)
        buat_peta(df)
        st.success("✅ Laporan berhasil ditambahkan!")
        st.experimental_rerun()

# --- Statistik Status + Filter SEJAJAR ---
st.subheader("📊 Statistik Status")
col_filter, col_chart, col_filtered = st.columns([1.3, 2, 2])

with col_filter:
    st.markdown("#### 📅 Filter Waktu")
    selected_date = st.date_input("Tanggal")
    selected_month = st.selectbox("Bulan", range(1, 13), format_func=lambda x: datetime(2025, x, 1).strftime("%B"))
    selected_year = st.selectbox("Tahun", sorted(df["Waktu Lapor"].dt.year.dropna().unique(), reverse=True))

    df_filtered = df[
        (df["Waktu Lapor"].dt.date == selected_date) &
        (df["Waktu Lapor"].dt.month == selected_month) &
        (df["Waktu Lapor"].dt.year == selected_year)
    ]

with col_chart:
    st.markdown("##### Statistik Keseluruhan")
    st.bar_chart(df["Status"].value_counts())

with col_filtered:
    st.markdown("##### 📊 Statistik Filter")
    if not df_filtered.empty:
        st.bar_chart(df_filtered["Status"].value_counts())
    else:
        st.info("⚠️ Tidak ada data untuk tanggal tersebut.")

# --- Update Status ---
st.subheader("✏️ Ubah Status TPS")
if not df.empty:
    for i, row in df.iterrows():
        col1, col2 = st.columns([3, 2])
        with col1:
            waktu = pd.to_datetime(row["Waktu Lapor"]).strftime("%d %B %Y, %H:%M")
            st.markdown(
                f"**{row['Nama TPS']}** ({row['Status']}) - {row['Kecamatan']}  \n"
                f"🗓️ Dilaporkan pada: {waktu}"
            )
        with col2:
            new_status = st.selectbox(
                f"Ubah status {i}",
                options=["Dilaporkan", "Ditangani", "Selesai"],
                index=["Dilaporkan", "Ditangani", "Selesai"].index(row["Status"]),
                key=f"status_{i}"
            )
            if new_status != row["Status"]:
                df.at[i, "Status"] = new_status
    save_data(df)
    buat_peta(df)
    st.success("✅ Semua status diperbarui!")

# --- Data Table ---
st.subheader("📋 Data Seluruh TPS")
st.dataframe(df.reset_index(drop=True))
