import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from fpdf import FPDF
import ezdxf

# Proje verisi
projects = [
    {"ID": 1, "Proje Adı": "Dolap 1", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-01", "Bitiş Tarihi": "2025-04-10", "Panel Sayısı": 12, "Kapak Sayısı": 4, "Toplam Maliyet": 5000, "İlerleme": 60},
    {"ID": 2, "Proje Adı": "Dolap 2", "Durum": "Tamamlandı", "Başlangıç Tarihi": "2025-03-01", "Bitiş Tarihi": "2025-03-15", "Panel Sayısı": 8, "Kapak Sayısı": 2, "Toplam Maliyet": 3000, "İlerleme": 100},
    {"ID": 3, "Proje Adı": "Dolap 3", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-05", "Bitiş Tarihi": "2025-04-12", "Panel Sayısı": 15, "Kapak Sayısı": 5, "Toplam Maliyet": 7000, "İlerleme": 80},
]

# Panel Hesaplama
def calculate_panels(project):
    st.subheader("Panel Hesaplama")
    panel_count = project["Panel Sayısı"]
    panel_area = 2 * 2.5  # Panelin yaklaşık alanı (2m x 2.5m)
    total_area = panel_count * panel_area
    st.write(f"Toplam Panel Alanı: {total_area} m²")

# Donanım Listesi ve Maliyet Hesaplama
def hardware_list(project):
    st.subheader("Donanım Listesi ve Maliyet Hesaplama")
    hardware_items = {
        "Vidalar": 1.5,  # TL / Adet
        "Menteşe": 10,   # TL / Adet
        "Raylar": 30,    # TL / Adet
        "Lamello": 2,    # TL / Adet
    }
    total_cost = sum(hardware_items.values()) * (project["Kapak Sayısı"] + project["Panel Sayısı"])
    st.write(f"Toplam Donanım Maliyeti: {total_cost} TL")

# DXF Çizim Çıkartma
def create_dxf(project):
    st.subheader("DXF Çizimi Oluşturma")
    doc = ezdxf.new()
    msp = doc.modelspace()
    
    # Basit bir panel çizebiliriz
    width = 200
    height = 200
    msp.add_line((0, 0), (width, 0))  # Alt kenar
    msp.add_line((0, 0), (0, height))  # Sol kenar
    msp.add_line((width, 0), (width, height))  # Sağ kenar
    msp.add_line((0, height), (width, height))  # Üst kenar
    
    # DXF dosyasını kaydetme
    file_name = f"panel_{project['Proje Adı']}.dxf"
    doc.saveas(file_name)
    st.write(f"DXF dosyası kaydedildi: {file_name}")

# Proje Arşivleme
def archive_project(project):
    st.subheader("Proje Arşivleme")
    # Arşivleme işlemleri burada yapılabilir
    st.write(f"Proje {project['Proje Adı']} başarıyla arşivlendi.")

# Basit 3D Dolap Görselleştirici
def display_cabinet(project):
    st.subheader(f"{project['Proje Adı']} 3D Görselleştirme")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    width = 100
    height = 200
    depth = 50
    shelf_count = project["Panel Sayısı"] // 2
    shelf_height = height / (shelf_count + 1)
    ax.bar3d(0, 0, 0, width, depth, height, color='lightgrey', alpha=0.6)
    for i in range(shelf_count):
        shelf_z = (i + 1) * shelf_height
        ax.bar3d(0, 0, shelf_z, width, depth, 5, color='brown', alpha=0.8)
    ax.set_xlabel('Width (Genişlik)')
    ax.set_ylabel('Depth (Derinlik)')
    ax.set_zlabel('Height (Yükseklik)')
    ax.set_title('Basit 3D Dolap Görselleştirmesi')
    st.pyplot(fig)

# Ana Kullanıcı Arayüzü
def main_ui(projects):
    st.title("Dolap Üretim Programı")

    selected_project_id = st.selectbox("Proje Seçin", [project["Proje Adı"] for project in projects])
    selected_project = next(project for project in projects if project["Proje Adı"] == selected_project_id)

    # Proje Güncellemeleri
    st.subheader(f"{selected_project['Proje Adı']} Proje Detayları")
    display_cabinet(selected_project)
    calculate_panels(selected_project)
    hardware_list(selected_project)
    create_dxf(selected_project)
    archive_project(selected_project)

if __name__ == "__main__":
    main_ui(projects)
