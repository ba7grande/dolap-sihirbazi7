import streamlit as st
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Panel Hesaplama
def calculate_panels(project):
    st.write(f"Panel Sayısı: {project['Panel Sayısı']}")
    # Hesaplama mantığı buraya eklenebilir

# 2. Donanım Listesi ve Maliyet Hesaplama
def hardware_list(project):
    st.write("Donanım Listesi ve Maliyet Hesaplama")
    # Donanım listesi ve maliyet hesaplama eklenebilir

# 3. DXF Çizimi
def create_dxf(project):
    st.write("DXF Çizimi oluşturuluyor")
    # DXF çizimi oluşturma eklenebilir

# 4. 3D Görselleştirme
def display_cabinet(project):
    st.write("3D Görselleştirme")
    # Basit 3D görselleştirme kodu eklenebilir

# 5. Kapak Çizimi ve Görünümü
def door_visualization(project):
    st.write("Kapak Çizimi ve Açılır/Kapalı Görünüm")
    # Kapak çizimi için basit görselleştirme eklenebilir

# 6. Lamello Delik Görselleştirme
def lamello_hole_visualization(project):
    st.write("Lamello Deliği Görselleştirmesi")
    # Lamello delik görselleştirme eklenebilir

# 7. Raf Görselleştirme
def shelf_visualization(project):
    st.write("Raf Pozisyonları ve Raf Görselleştirmesi")
    # Raf yerleşimi ve görselleştirme eklenebilir

# 8. PDF Teklif Oluşturma
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

# 9. Rafları Otomatik Yerleştirme
def auto_place_shelves(project):
    st.write("Rafları Otomatik Yerleştiriliyor")
    # Raf yerleşimi algoritması eklenebilir

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
        "Toplam Maliyet": 5000,
    },
    {
        "Proje Adı": "Proje 2",
        "Panel Sayısı": 3,
        "Kapak Sayısı": 1,
        "Toplam Maliyet": 3000,
    }
]

if __name__ == "__main__":
    main_ui(projects)
