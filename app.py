import streamlit as st
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
import ezdxf
import os

# Panel Hesaplama Modülü
def calculate_panels(project):
    panel_area = project['Panel Boyutları']['Uzunluk'] * project['Panel Boyutları']['Genişlik']
    total_area = panel_area * project['Panel Sayısı']
    st.write(f"Toplam Panel Alanı: {total_area} cm²")
    st.write(f"Panel Sayısı: {project['Panel Sayısı']}")

# Donanım Listesi ve Maliyet Hesaplama
def hardware_list(project):
    donanım_fiyatları = {"Ray": 100, "Vida": 50, "Lamello": 200}
    toplam_maliyet = (donanım_fiyatları["Ray"] * project['Kapak Sayısı']) + \
                     (donanım_fiyatları["Vida"] * project['Panel Sayısı']) + \
                     (donanım_fiyatları["Lamello"] * project['Lamello Sayısı'])
    st.write(f"Toplam Maliyet: {toplam_maliyet} TL")
    st.write("Donanım Listesi:")
    for donanım, fiyat in donanım_fiyatları.items():
        st.write(f"{donanım}: {fiyat} TL")

# DXF Çizimi
def create_dxf(project):
    st.write("DXF Çizimi Oluşturuluyor")
    doc = ezdxf.new()
    msp = doc.modelspace()
    # Basit bir panel çizimi
    msp.add_line((0, 0), (project['Panel Boyutları']['Uzunluk'], 0))
    msp.add_line((project['Panel Boyutları']['Uzunluk'], 0), 
                 (project['Panel Boyutları']['Uzunluk'], project['Panel Boyutları']['Genişlik']))
    msp.add_line((project['Panel Boyutları']['Uzunluk'], project['Panel Boyutları']['Genişlik']), 
                 (0, project['Panel Boyutları']['Genişlik']))
    msp.add_line((0, project['Panel Boyutları']['Genişlik']), (0, 0))
    
    # DXF dosyasını kaydetme
    dxf_file = f"panel_{project['Proje Adı']}.dxf"
    doc.saveas(dxf_file)
    st.write(f"DXF Dosyası: {dxf_file}")

# 3D Görselleştirme Modülü
def display_cabinet(project):
    st.write("3D Görselleştirme")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(0, 0, 0, color='r', label="Dolap Başlangıcı")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    st.pyplot(fig)

# Kapak Çizimi ve Görünüm
def door_visualization(project):
    st.write("Kapak Çizimi ve Açılır/Kapalı Görünüm")
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 0], label="Kapak")
    ax.set_title("Kapak Çizimi")
    ax.legend()
    st.pyplot(fig)

# Lamello Delik Görselleştirme
def lamello_hole_visualization(project):
    st.write("Lamello Deliği Görselleştirmesi")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(1, 1, 1, color='g', label="Lamello Deliği")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    st.pyplot(fig)

# Raf Görselleştirme
def shelf_visualization(project):
    st.write("Raf Pozisyonları ve Raf Görselleştirmesi")
    fig, ax = plt.subplots()
    ax.barh([1, 2, 3], [10, 20, 15])
    ax.set_xlabel("Raf Yükseklikleri")
    ax.set_ylabel("Raf Sayısı")
    st.pyplot(fig)

# PDF Teklif Oluşturma
def generate_pdf(project):
    st.subheader("PDF Teklif Şablonu Oluşturma")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicode', '', 'path_to_your_font/arialunicid.ttf', uni=True)
    pdf.set_font('ArialUnicode', '', 12)

    pdf.cell(200, 10, f"Teklif: {project['Proje Adı']}", ln=True)
    pdf.cell(200, 10, f"Panel Sayısı: {project['Panel Sayısı']}", ln=True)
    pdf.cell(200, 10, f"Kapak Sayısı: {project['Kapak Sayısı']}", ln=True)
    pdf.cell(200, 10, f"Toplam Maliyet: {project['Toplam Maliyet']} TL", ln=True)
    
    pdf_output = f"Teklif_{project['Proje Adı']}.pdf"
    pdf.output(pdf_output)
    st.write(f"Teklif PDF dosyası kaydedildi: {pdf_output}")

# Rafları Otomatik Yerleştirme
def auto_place_shelves(project):
    st.write("Rafları Otomatik Yerleştiriliyor")
    fig, ax = plt.subplots()
    ax.plot([0, 1], [1, 1], label="Raf Pozisyonu")
    ax.set_title("Raf Yerleşimi")
    ax.legend()
    st.pyplot(fig)

# Ana Arayüz
def main_ui(projects):
    st.title("Dolap Üretim Programı")
    
    project_id = st.selectbox("Proje Seçin", [p["Proje Adı"] for p in projects])
    project = next(p for p in projects if p["Proje Adı"] == project_id)
    
    # Panel Hesaplama
    calculate_panels(project)
    
    # Donanım Listesi ve Maliyet Hesaplama
    hardware_list(project)
    
    # DXF Çizimi
    create_dxf(project)
    
    # 3D Görselleştirme
    display_cabinet(project)
    
    # Kapak Çizimi
    door_visualization(project)
    
    # Lamello Delik Görselleştirme
    lamello_hole_visualization(project)
    
    # Raf Görselleştirme
    shelf_visualization(project)
    
    # PDF Teklif Oluşturma
    generate_pdf(project)
    
    # Rafları Otomatik Yerleştirme
    auto_place_shelves(project)

# Projelerin başlangıç verisi
projects = [
    {
        "Proje Adı": "Proje 1",
        "Panel Sayısı": 5,
        "Kapak Sayısı": 2,
        "Lamello Sayısı": 5,
        "Toplam Maliyet": 5000,
        "Panel Boyutları": {"Uzunluk": 200, "Genişlik": 100},
    },
    {
        "Proje Adı": "Proje 2",
        "Panel Sayısı": 3,
        "Kapak Sayısı": 1,
        "Lamello Sayısı": 3,
        "Toplam Maliyet": 3000,
        "Panel Boyutları": {"Uzunluk": 150, "Genişlik": 80},
    }
]

if __name__ == "__main__":
    main_ui(projects)
