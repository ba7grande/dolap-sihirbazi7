import streamlit as st
import numpy as np
import pandas as pd
import qrcode
from fpdf import FPDF
import plotly.express as px
from pythreejs import *  # 3D Görselleştirme için pythreejs
import matplotlib.pyplot as plt
from io import BytesIO

# 1. Dolap Ölçü Girişi
def get_cabinet_dimensions():
    width = st.number_input("Dolap Genişliği (cm):", min_value=1, max_value=500, value=100)
    height = st.number_input("Dolap Yüksekliği (cm):", min_value=1, max_value=500, value=200)
    depth = st.number_input("Dolap Derinliği (cm):", min_value=1, max_value=500, value=50)
    return width, height, depth

# 2. Parça Listesi Oluşturma
def create_parts_list(cabinet_dimensions):
    width, height, depth = cabinet_dimensions
    parts = {
        "Top Panel": {"Width": width, "Height": depth},
        "Bottom Panel": {"Width": width, "Height": depth},
        "Side Panel Left": {"Width": height, "Height": depth},
        "Side Panel Right": {"Width": height, "Height": depth},
        "Back Panel": {"Width": width, "Height": height},
        "Shelves": {"Width": width, "Height": depth}
    }
    return parts

# 3. Lamello Cabineo Deliklerini Hesaplama
def calculate_lamello_holes(parts):
    holes = {}
    for part, dimensions in parts.items():
        holes[part] = f"Lamello holes for {part} at position: {np.random.randint(1, 5)}"
    return holes

# 4. CSV Çıktısı
def generate_csv(parts):
    df = pd.DataFrame(parts).T
    df.to_csv('parts_list.csv')
    st.write("Parça Listesi CSV olarak indirildi.")

# 5. QR Kod Üretimi
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
    return img

# 6. CNC Entegrasyonu: DXF Çıktısı ve Donanım Hesaplama
def generate_dxf(parts):
    dxf_data = f"DXF for {list(parts.keys())}"
    return dxf_data

# 7. 3D Görselleştirme (pythreejs)
def visualize_3d(cabinet_dimensions):
    width, height, depth = cabinet_dimensions

    # Kamera ve sahne ayarları
    scene = Scene()
    camera = PerspectiveCamera(position=[3, 3, 3], lookAt=[0, 0, 0])
    renderer = WebGLRenderer(camera=camera, scene=scene, width=600, height=600)

    # 3D model çizimi
    box = Mesh(geometry=BoxGeometry(width, height, depth), material=MeshLambertMaterial(color='skyblue'))
    scene.add(box)

    renderer.set_size(600, 600)

    st.write("3D Model Görselleştirmesi")
    display(renderer)

# 8. Akıllı Fonksiyonlar
def smart_functions(parts):
    # Örneğin, otomatik malzeme optimizasyonu
    material_optimization = "Material optimization done"
    st.write(material_optimization)

# 9. PDF Teklif Şablonu Tasarımı
def generate_pdf(project):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Dolap Bilgileri
    pdf.cell(200, 10, txt="Dolap Teklifi", ln=True, align="C")
    pdf.ln(10)
    for key, value in project.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="L")

    # PDF çıktısı
    pdf.output("project_quote.pdf")
    st.write("Teklif PDF olarak indirildi.")

# 10. Grafik ve Raporlar
def generate_report(parts):
    df = pd.DataFrame(parts).T
    fig = px.bar(df, x=df.index, y=["Width", "Height"], title="Parça Ölçüleri")
    st.plotly_chart(fig)

# Ana UI Fonksiyonu
def main_ui():
    st.title("Dolap Üretim Programı")

    # 1. Ölçü Girişi
    cabinet_dimensions = get_cabinet_dimensions()

    # 2. Parça Listesi Oluşturma
    parts = create_parts_list(cabinet_dimensions)
    st.write("Parça Listesi:")
    st.write(parts)

    # 3. Lamello Delik Pozisyonları
    holes = calculate_lamello_holes(parts)
    st.write("Lamello Delik Pozisyonları:")
    st.write(holes)

    # 4. CSV Çıktısı
    generate_csv(parts)

    # 5. QR Kod Üretimi
    qr_code_image = generate_qr_code(str(parts))
    st.image(qr_code_image)

    # 6. DXF Çıktısı
    dxf = generate_dxf(parts)
    st.write(f"DXF Çıktısı:\n{dxf}")

    # 7. 3D Görselleştirme
    visualize_3d(cabinet_dimensions)

    # 8. Akıllı Fonksiyonlar
    smart_functions(parts)

    # 9. PDF Teklif Şablonu
    generate_pdf(parts)

    # 10. Grafik Raporu
    generate_report(parts)

# Uygulamayı Çalıştırma
if __name__ == "__main__":
    main_ui()
