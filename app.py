import streamlit as st
import numpy as np
from pythreejs import *
from fpdf import FPDF
import qrcode
import io
import csv
import random

# Streamlit Başlığı
st.title('Dolap Üretim ve Tasarım Uygulaması')

# Kullanıcıdan dolap ölçülerini alma
width = st.number_input('Dolap Genişliği (cm)', min_value=30, max_value=200, value=60)
height = st.number_input('Dolap Yüksekliği (cm)', min_value=30, max_value=300, value=80)
thickness = st.number_input('Malzeme Kalınlığı (mm)', min_value=5, max_value=30, value=18) / 10  # cm cinsinden

# Parçaları oluşturma (örneğin, bir panel)
panel_geometry = BoxGeometry(width=width, height=height, depth=thickness)
panel_material = MeshLambertMaterial(color='blue', opacity=0.7, transparent=True)
panel = Mesh(geometry=panel_geometry, material=panel_material)

# Işık ekleme
light = DirectionalLight(color='white', intensity=1)
light.position = [5, 5, 5]

# Sahne oluşturma
scene = Scene(children=[panel, light])

# Kamera ve Perspektif
camera = PerspectiveCamera(fov=75, aspect=1, near=0.1, far=1000)
camera.position = [100, 100, 100]
camera.lookAt([0, 0, 0])

# WebGL Renderer
renderer = WebGLRenderer(camera=camera, scene=scene, width=600, height=600)
renderer.setSize(600, 600)

# 3D Görselleştirmeyi Streamlit'e entegre etme
st.write("### 18mm Kalınlığında Dolap Parçası Görselleştirmesi")
st.components.v1.html(renderer.to_html(), height=600)

# Parça listesi oluşturma
parts = {
    'Panel': {'width': width, 'height': height, 'thickness': thickness},
}

# Parça CSV çıktısı oluşturma
def create_csv(parts):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Part Name', 'Width (cm)', 'Height (cm)', 'Thickness (cm)'])
    for part_name, dimensions in parts.items():
        writer.writerow([part_name, dimensions['width'], dimensions['height'], dimensions['thickness']])
    return output.getvalue()

# PDF teklif şablonu üretme
def generate_pdf(parts):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Dolap Üretim Teklif Şablonu", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Parçalar:", ln=True)
    for part_name, dimensions in parts.items():
        pdf.cell(200, 10, txt=f"{part_name}: {dimensions['width']} x {dimensions['height']} x {dimensions['thickness']} cm", ln=True)
    pdf.output("project_quote.pdf")

# QR kod üretimi
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# PDF, CSV ve QR kodları gösterme
if st.button('PDF Teklif Oluştur'):
    generate_pdf(parts)
    st.success("PDF Teklif Oluşturuldu")

if st.button('CSV Parça Listesi Oluştur'):
    csv_data = create_csv(parts)
    st.download_button('Parça Listesi CSV', csv_data, file_name='parts_list.csv')

# QR kodu gösterme
qr_code_data = "https://www.dolapsihirbazi.com"
img = generate_qr_code(qr_code_data)
st.image(img, caption="QR Kod")

# Akıllı Fonksiyonlar (Montaj sırası ve zaman tahmini)
def smart_functions():
    assembly_order = np.random.choice(list(parts.keys()), size=len(parts), replace=False)
    st.write("Montaj Sırası:", assembly_order)

    # Üretim zaman tahmini (sadece örnek)
    estimated_time = np.random.randint(30, 120)  # 30-120 dakika arasında rastgele bir değer
    st.write(f"Üretim Zamanı Tahmini: {estimated_time} dakika")

# Akıllı Fonksiyonları çalıştırma
if st.button('Akıllı Fonksiyonlar'):
    smart_functions()

# CNC Entegrasyonu: DXF ve G-code çıktısı üretme
def generate_dxf(parts):
    dxf_content = f"DXF for {len(parts)} parts:\n"
    for part_name, dimensions in parts.items():
        dxf_content += f"{part_name}: {dimensions['width']} x {dimensions['height']} x {dimensions['thickness']} cm\n"
    return dxf_content

if st.button('DXF Çıktısı Oluştur'):
    dxf_data = generate_dxf(parts)
    st.text(dxf_data)

# Donanım ve maliyet hesaplama
def calculate_hardware_cost(parts):
    hardware_costs = {
        'Vida': 0.5,  # unit cost per part
        'Minifix': 2.0,  # unit cost per part
        'Ray': 5.0,  # unit cost per part
        'Kulp': 3.0,  # unit cost per part
    }
    total_cost = len(parts) * sum(hardware_costs.values())
    st.write(f"Donanım Maliyeti: {total_cost} TL")
    return total_cost

# Maliyet hesaplama butonu
if st.button('Maliyet Hesaplama'):
    calculate_hardware_cost(parts)
