import streamlit as st
import numpy as np
from fpdf import FPDF
import qrcode
import pyautogui
import plotly.graph_objects as go
from pythreejs import *  # 3D render için

# Proje veri yapısı
class Project:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.parts = []
        self.material_cost = 0
        self.hardware_cost = 0
        self.assembly_order = []
        self.dxf_output = ""

    def add_part(self, part):
        self.parts.append(part)

    def set_material_cost(self, cost):
        self.material_cost = cost

    def set_hardware_cost(self, cost):
        self.hardware_cost = cost

# 3D görselleştirme
def generate_3d_view(project):
    # Burada, streamlit ile uyumlu olarak 3D görselleştirme kodu olacak
    # Pythreejs veya başka bir kütüphane kullanılabilir
    pass

# DXF çıktı üretimi
def generate_dxf(project):
    # Burada DXF dosyalarını üretmek için kod olacak
    pass

# QR Kod üretimi
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# PDF Teklif Raporu
def generate_pdf(project):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Project Dimensions: {project.width} x {project.height} x {project.depth}", ln=True)
    pdf.cell(200, 10, txt=f"Material Cost: {project.material_cost} USD", ln=True)
    pdf.cell(200, 10, txt=f"Hardware Cost: {project.hardware_cost} USD", ln=True)
    pdf.output("project_quote.pdf")

# Ana UI
def main_ui():
    st.title("Fithole Benzeri Dolap Üretim Yazılımı")

    # Proje oluşturma
    st.sidebar.header("Proje Girişi")
    width = st.sidebar.number_input("Dolap Genişliği (cm)", min_value=50, max_value=500, value=120)
    height = st.sidebar.number_input("Dolap Yüksekliği (cm)", min_value=100, max_value=300, value=200)
    depth = st.sidebar.number_input("Dolap Derinliği (cm)", min_value=30, max_value=100, value=60)

    project = Project(width, height, depth)

    if st.sidebar.button("Oluştur"):
        st.sidebar.write(f"Proje: {width} x {height} x {depth} cm")
        # 3D Görselleştirme
        generate_3d_view(project)

        # DXF çıktısı
        generate_dxf(project)

        # QR Kod
        qr_code_image = generate_qr_code(f"Project: {width}x{height}x{depth}")
        st.image(qr_code_image, caption="QR Code for Project")

        # PDF Teklif Raporu
        generate_pdf(project)
        st.write("PDF raporu başarıyla oluşturuldu!")

# Main fonksiyonu
def main():
    main_ui()

if __name__ == "__main__":
    main()
