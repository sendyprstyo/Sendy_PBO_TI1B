from abc import ABC, abstractmethod

class LaporanSampah(ABC):
    def __init__(self, id_laporan, lokasi, deskripsi, waktu, status="Dilaporkan"):
        self.id_laporan = id_laporan
        self.lokasi = lokasi  # tuple: (lat, lon)
        self.deskripsi = deskripsi
        self.waktu = waktu
        self.status = status

    @abstractmethod
    def get_jenis(self):
        pass

    def get_koordinat(self):
        return self.lokasi

    def get_info_popup(self):
        return f"{self.get_jenis()}<br>{self.deskripsi}<br>Status: {self.status}"

class SampahOrganik(LaporanSampah):
    def get_jenis(self):
        return "Sampah Organik"

class SampahPlastik(LaporanSampah):
    def get_jenis(self):
        return "Sampah Plastik"

class SampahElektronik(LaporanSampah):
    def get_jenis(self):
        return "Sampah Elektronik"
