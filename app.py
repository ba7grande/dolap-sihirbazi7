import streamlit as st
import numpy as np
import pandas as pd
from fpdf2 import FPDF
import qrcode
import os
from io import BytesIO

# PDF sınıfı oluşturuluyor
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, txt="Dolap Teklifi", ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)

    def add_content(self, project):
        self.add_page()
        self.chapter_title("Proje Bilgileri")
        self.chapter_body(f"Parça Listesi: {', '.join(project.parts)}\n"
                          f"Ölçüler: {project.measurements}\n"
                          f"Donanım: {project.hardware}")

# Proje sınıfı
class Project:
    def __init__(self, measurements, parts, hardware):
        self.measurements = measurements
        self.parts = parts
        self.hardware = hardware

# 3D Görselleştirme (Basit bir gösterim)
def generate_3d_visualization(project):
    st.write("3D Görselleştirme: Burada 3D dolap modeli yer alacak!")
    st.write(f"Ölçüler: {project.measurements}")

# Etiket ve Barkod Modülü
def generate_barcode(part_name):
    qr = qrcode.make(part_name)
    barcode_image = BytesIO()
    qr.save(barcode_image, format="PNG")
    barcode_image.seek(0)
    st.image(barcode_image)

# CNC Entegrasyonu (DXF / G-code için)
def generate_dxf(project):
    st.write("DXF çıktısı burada yer alacak...")
    # Basit bir DXF çıktısı simülasyonu
    st.write(f"DXF verisi oluşturuldu: {', '.join(project.parts)}")

# Maliyet Hesaplama
def calculate_cost(project):
    st.write("Maliyet Hesaplama: Donanım ve metrekare hesaplamaları")
    cost = len(project.parts) * 10  # Basit maliyet hesaplama
    st.write(f"Toplam Maliyet: {cost} TL")

# PDF Teklif Oluşturma
def generate_pdf(project):
    pdf = PDF()
    pdf.add_content(project)
    pdf.output("project_quote.pdf")
    st.write("PDF Teklif Oluşturuldu!")

# Akıllı Fonksiyonlar (Montaj sırası vb.)
def smart_functions(project):
    st.write("Akıllı Fonksiyonlar: Montaj sırası önerisi ve üretim zaman tahmini")
    assembly_order = np.random.choice(project.parts, size=len(project.parts), replace=False)
    st.write(f"Montaj Sırası: {', '.join(assembly_order)}")

# Ana arayüz
def main_ui(projects):
    st.title("Dolap Üretim Programı")
    project = st.selectbox("Proje Seçin", projects)

    if st.button('3D Görselleştirme'):
        generate_3d_visualization(project)

    if st.button('Barkod/Etiket Oluştur'):
        part_name = st.text_input("Parça Adı")
        if part_name:
            generate_barcode(part_name)

    if st.button('DXF Çıktısı Üret'):
        generate_dxf(project)

    if st.button('Maliyet Hesapla'):
        calculate_cost(project)

    if st.button('PDF Teklif Oluştur'):
        generate_pdf(project)

    if st.button('Akıllı Fonksiyonlar'):
        smart_functions(project)

# Proje listesi oluşturuluyor
projects = [
    Project({'width': 100, 'height': 200, 'depth': 50}, ['parça1', 'parça2', 'parça3'], ['vida', 'minifix', 'ray']),
    Project({'width': 150, 'height': 250, 'depth': 60}, ['parça4', 'parça5', 'parça6'], ['ray', 'kulp'])
]

# Ana fonksiyon çağrılıyor
def main():
    main_ui(projects)

if __name__ == "__main__":
    main()
