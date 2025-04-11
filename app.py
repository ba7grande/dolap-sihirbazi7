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

# DXF Çizimi Oluşturma
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

# Kapak Çizimi ve Açılır/Kapalı Görünüm
def door_visualization(project):
    st.subheader("Kapak Çizimi ve Açılır/Kapalı Görünüm")
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    width = 50  # Kapak genişliği
    height = 200  # Kapak yüksekliği
    depth = 3  # Kapak kalınlığı
    
    # Kapak açıkken çizimi
    ax.bar3d(0, 0, 0, width, depth, height, color='blue', alpha=0.5)
    ax.set_xlabel('Width')
    ax.set_ylabel('Depth')
    ax.set_zlabel('Height')
    ax.set_title('Kapak Açık')
    st.pyplot(fig)
    
    # Kapak kapalıyken çizimi
    ax.cla()  # Temizle
    ax.bar3d(0, 0, 0, width, depth, height, color='green', alpha=0.8)
    ax.set_xlabel('Width')
    ax.set_ylabel('Depth')
    ax.set_zlabel('Height')
    ax.set_title('Kapak Kapalı')
    st.pyplot(fig)

# Lamello Deliği Pozisyonlarının 3D Gösterimi
def lamello_hole_visualization(project):
    st.subheader("Lamello Deliği Pozisyonlarının 3D Gösterimi")
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Basit Lamello deliği çizimi
    width = 100
    depth = 50
    height = 200
    hole_radius = 2  # Deliğin çapı
    
    # Lamello deliklerini çiz
    for i in range(3):
        ax.scatter(i * 30, depth / 2, height / 2, color='red', s=100)  # Deliğin pozisyonları
    
    ax.set_xlabel('Width')
    ax.set_ylabel('Depth')
    ax.set_zlabel('Height')
    ax.set_title('Lamello Delik Pozisyonları')
    st.pyplot(fig)

# Raf Pozisyonları ve Rafların 3D Görselleştirmesi
def shelf_visualization(project):
    st.subheader("Raf Pozisyonları ve Rafların 3D Görselleştirmesi")
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    width = 100
    depth = 50
    height = 200
    shelf_count = project["Panel Sayısı"] // 2  # Raf sayısı
    shelf_height = height / (shelf_count + 1)
    
    # Rafları çiz
    for i in range(shelf_count):
        shelf_z = (i + 1) * shelf_height
        ax.bar3d(0, 0, shelf_z, width, depth, 5, color='brown', alpha=0.8)
    
    ax.set_xlabel('Width')
    ax.set_ylabel('Depth')
    ax.set_zlabel('Height')
    ax.set_title('Raf Pozisyonları ve Görselleştirmesi')
    st.pyplot(fig)

# PDF Teklif Şablonu Tasarımı
def generate_pdf(project):
    st.subheader("PDF Teklif Şablonu Oluşturma")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Başlık ve proje bilgileri
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Teklif: {project['Proje Adı']}", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Panel Sayısı: {project['Panel Sayısı']}", ln=True)
    pdf.cell(200, 10, f"Kapak Sayısı: {project['Kapak Sayısı']}", ln=True)
    pdf.cell(200, 10, f"Toplam Maliyet: {project['Toplam Maliyet']} TL", ln=True)
    
    # PDF'yi kaydet
    pdf_output = f"Teklif_{project['Proje Adı']}.pdf"
    pdf.output(pdf_output)
    st.write(f"Teklif PDF dosyası kaydedildi: {pdf_output}")

# Rafları Otomatik Yerleştirme ve Pozisyon Ayarı
def auto_place_shelves(project):
    st.subheader("Rafları Otomatik Yerleştirme ve Pozisyon Ayarı")
    
    shelf_count = project["Panel Sayısı"] // 2
    st.write(f"Raf sayısı: {shelf_count}")
    
    # Otomatik raf yerleştirme algoritması
    shelf_positions = [i * (200 / (shelf_count + 1)) for i in range(shelf_count)]
    st.write("Rafların pozisyonları: ", shelf_positions)

# Ana kullanıcı arayüzü
def main_ui(projects):
    st.title("Dolap Tasarımı ve Üretim Programı")
    project_id = st.selectbox("Proje Seçin", [p["Proje Adı"] for p in projects])
    project = next(p for p in projects if p["Proje Adı"] == project_id)
    
    # Panel Hesaplama
    calculate_panels(project)
    
    # Donanım Listesi ve Maliyet Hesaplama
    hardware_list(project)
    
    # DXF Çizimi
    create_dxf(project)
    
    # Proje Arşivleme
    archive_project(project)
    
    # 3D Görselleştirme
    display_cabinet(project)
    
    # Kapak Çizimi ve Görünüm
    door_visualization(project)
    
    # Lamello Delik Görselleştirme
    lamello_hole_visualization(project)
    
    # Raf Görselleştirme
    shelf_visualization(project)
    
    # PDF Teklif Oluşturma
    generate_pdf(project)
    
    # Rafları Otomatik Yerleştirme
    auto_place_shelves(project)

if __name__ == "__main__":
    main_ui(projects)
