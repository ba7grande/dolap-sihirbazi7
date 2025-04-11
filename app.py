import streamlit as st
import numpy as np
import pandas as pd
import qrcode
from fpdf import FPDF  # fpdf2 yerine fpdf kullandık
import plotly.graph_objects as go
import os

# Üretim Verilerini Tanımlama
class Project:
    def __init__(self, name, width, height, depth, parts, hardware, material_cost, labor_cost):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.parts = parts
        self.hardware = hardware
        self.material_cost = material_cost
        self.labor_cost = labor_cost

    def get_total_cost(self):
        total_hardware_cost = sum(part['cost'] for part in self.hardware)
        return self.material_cost + total_hardware_cost + self.labor_cost

# PDF ve Etiket Üretimi
def generate_pdf(project):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Project Quote", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(100, 10, txt=f"Project Name: {project.name}")
    pdf.ln(10)
    pdf.cell(100, 10, txt=f"Width: {project.width} cm")
    pdf.ln(10)
    pdf.cell(100, 10, txt=f"Height: {project.height} cm")
    pdf.ln(10)
    pdf.cell(100, 10, txt=f"Depth: {project.depth} cm")
    pdf.ln(10)

    pdf.cell(100, 10, txt=f"Total Cost: {project.get_total_cost()} USD")
    pdf.ln(10)

    pdf.output("project_quote.pdf")

# QR Kod Üretimi
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save("qrcode.png")

# CNC Delik Simülasyonu ve 3D Görselleştirme
def create_3d_visualization(project):
    fig = go.Figure()

    # 3D Box for the cabinet
    fig.add_trace(go.Mesh3d(
        x=[0, project.width, project.width, 0, 0, project.width, project.width, 0],
        y=[0, 0, project.depth, project.depth, 0, 0, project.depth, project.depth],
        z=[0, 0, 0, 0, project.height, project.height, project.height, project.height],
        opacity=0.5,
        color='lightblue'
    ))

    fig.update_layout(scene=dict(
        xaxis=dict(range=[0, project.width]),
        yaxis=dict(range=[0, project.depth]),
        zaxis=dict(range=[0, project.height]),
    ))

    fig.update_layout(scene=dict(
        xaxis_title="Width",
        yaxis_title="Depth",
        zaxis_title="Height"
    ))

    st.plotly_chart(fig)

# Akıllı Fonksiyonlar (Optimizasyon, Montaj sırası, vs.)
def smart_functions(project):
    # Malzeme optimizasyonu
    optimized_parts = np.random.choice(project.parts, size=len(project.parts), replace=False)
    
    # Montaj sırası önerisi
    assembly_order = np.random.choice(project.parts)
    
    st.write("Malzeme Optimizasyonu: ", optimized_parts)
    st.write("Montaj Sırası: ", assembly_order)

# CNC DXF Çıktısı
def generate_dxf(project):
    dxf_data = f"""
    0
    SECTION
    2
    HEADER
    0
    ENDSEC
    0
    SECTION
    2
    TABLES
    0
    ENDSEC
    0
    SECTION
    2
    BLOCKS
    0
    ENDSEC
    0
    SECTION
    2
    ENTITIES
    0
    LINE
    10
    0
    20
    0
    30
    0
    11
    {project.width}
    21
    0
    31
    0
    0
    ENDSEC
    0
    SECTION
    2
    OBJECTS
    0
    ENDSEC
    0
    END
    """
    with open("cabinet_design.dxf", "w") as dxf_file:
        dxf_file.write(dxf_data)

# Streamlit UI
def main():
    st.title("Dolap Üretim Programı")

    project_name = st.text_input("Proje Adı", "Dolap Projesi")
    width = st.number_input("Genişlik (cm)", 50, 300, 100)
    height = st.number_input("Yükseklik (cm)", 50, 300, 200)
    depth = st.number_input("Derinlik (cm)", 50, 300, 50)
    
    parts = [{"name": "Parça 1", "cost": 5}, {"name": "Parça 2", "cost": 7}]
    hardware = [{"name": "Vida", "cost": 0.5}, {"name": "Menteşe", "cost": 2}]
    material_cost = 50
    labor_cost = 20

    project = Project(project_name, width, height, depth, parts, hardware, material_cost, labor_cost)

    if st.button("PDF Teklif Oluştur"):
        generate_pdf(project)

    if st.button("QR Kod Üret"):
        generate_qr_code(f"Proje: {project.name}")
    
    if st.button("3D Görselleştir"):
        create_3d_visualization(project)
    
    if st.button("CNC DXF Çıktısı Oluştur"):
        generate_dxf(project)

    if st.button("Akıllı Fonksiyonlar"):
        smart_functions(project)

if __name__ == "__main__":
    main()
