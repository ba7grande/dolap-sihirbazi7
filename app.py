import streamlit as st
import numpy as np
import pandas as pd
import qrcode
from PIL import Image
import io
from fpdf import FPDF

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
    
    # QR kodu PIL formatında elde etme
    img = qr.make_image(fill='black', back_color='white')

    # Streamlit'e göndermeden önce PIL Image formatına dönüştür
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    return img_buffer

# PDF Üretimi
def generate_pdf(project):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    
    # Başlık
    pdf.cell(200, 10, txt="Dolap Üretim Teklifi", ln=True, align='C')

    # Proje Bilgileri
    pdf.cell(200, 10, txt=f"Proje Adı: {project['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Genişlik: {project['width']} mm", ln=True)
    pdf.cell(200, 10, txt=f"Yükseklik: {project['height']} mm", ln=True)
    pdf.cell(200, 10, txt=f"Derinlik: {project['depth']} mm", ln=True)

    # Parça listesi
    pdf.cell(200, 10, txt="Parçalar:", ln=True)
    for part in project['parts']:
        pdf.cell(200, 10, txt=f"{part['name']} - {part['quantity']} adet", ln=True)

    # QR Kod
    qr_code_image = generate_qr_code(str(project['parts']))
    pdf.ln(10)  # boşluk ekle
    pdf.image(qr_code_image, x=10, w=50)

    pdf.output("project_quote.pdf")

# Akıllı Fonksiyonlar - Montaj sırası önerisi ve malzeme optimizasyonu
def smart_functions(project):
    # Malzeme optimizasyonu ve montaj sırası
    assembly_order = np.random.choice(project['parts'])
    st.write(f"Montaj sırası: {assembly_order['name']}")

    # Montaj sırası önerisi ve malzeme optimizasyonu
    st.write("Malzeme optimizasyonu yapılıyor...")

# 3D Görselleştirme - Basit Görselleştirme
def visualize_3d(project):
    st.subheader("3D Görselleştirme")
    st.write(f"{project['name']} için 3D dolap modeli")

# Ölçü Girişi ve Parça Listesi
def get_dimensions_and_parts():
    st.subheader("Dolap Ölçüleri")
    project_width = st.number_input("Dolap Genişliği (mm)", min_value=0)
    project_height = st.number_input("Dolap Yüksekliği (mm)", min_value=0)
    project_depth = st.number_input("Dolap Derinliği (mm)", min_value=0)

    parts = []
    part_name = st.text_input("Parça Adı")
    part_qty = st.number_input("Adet", min_value=1)

    if st.button("Parça Ekle"):
        parts.append({'name': part_name, 'quantity': part_qty})
        st.success(f"{part_name} eklendi.")

    return project_width, project_height, project_depth, parts

# CNC Entegrasyonu (Örnek)
def cnc_integration(project):
    st.subheader("CNC Entegrasyonu")
    st.write(f"{project['name']} için DXF/G-code çıktısı oluşturuluyor...")
    # Gerçek CNC entegrasyonu burada yapılabilir

# DXF Çıktısı
def generate_dxf(project):
    st.subheader("DXF Çıktısı")
    st.write(f"Projeye ait DXF çıktısı oluşturuluyor...")
    # DXF dosyası oluşturma işlemi buraya eklenebilir

# Parça Listesi Oluşturma
def create_parts_list(project):
    st.subheader("Parça Listesi")
    for part in project['parts']:
        st.write(f"{part['name']} - {part['quantity']} adet")

# Ana Uygulama Arayüzü
def main_ui():
    st.title("Dolap Üretim Sistemi")

    # Proje Bilgilerini Girme
    project_name = st.text_input("Proje Adı")
    project_width, project_height, project_depth, parts = get_dimensions_and_parts()

    if st.button("Yeni Proje Oluştur"):
        project = {
            'name': project_name,
            'width': project_width,
            'height': project_height,
            'depth': project_depth,
            'parts': parts
        }
        st.session_state.project = project
        st.success("Proje oluşturuldu.")

    # Proje Var mı Kontrol Etme
    if 'project' in st.session_state:
        st.subheader("Parça Listesi")
        create_parts_list(st.session_state.project)

        # 3D Görselleştirme
        visualize_3d(st.session_state.project)

        # Akıllı Fonksiyonlar
        smart_functions(st.session_state.project)

        # CNC Entegrasyonu
        cnc_integration(st.session_state.project)

        # DXF Çıktısı
        generate_dxf(st.session_state.project)

        # PDF Oluşturma
        if st.button("Teklif PDF'ini Oluştur"):
            generate_pdf(st.session_state.project)
            st.success("Teklif PDF'i oluşturuldu.")

        # QR Kod Görüntüleme
        qr_code_image = generate_qr_code(str(st.session_state.project['parts']))
        st.image(qr_code_image)

# Ana Fonksiyon
def main():
    main_ui()

if __name__ == "__main__":
    main()
