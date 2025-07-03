import folium
from model import SampahOrganik

def buat_peta(list_laporan, nama_file_output="peta_tps.html"):
    # Pusatkan peta di tengah Kota Semarang
    peta = folium.Map(location=[-6.9904, 110.4229], zoom_start=13)

    for laporan in list_laporan:
        lat, lon = laporan.get_koordinat()
        jenis = laporan.get_jenis()

        warna = {
            "Sampah Organik": "green",
            "Sampah Plastik": "blue",
            "Sampah Elektronik": "red"
        }.get(jenis, "gray")

        folium.Marker(
            location=[lat, lon],
            popup=laporan.get_info_popup(),
            icon=folium.Icon(color=warna)
        ).add_to(peta)

    peta.save(nama_file_output)
    print(f"Peta disimpan di file: {nama_file_output}")
