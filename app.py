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

    # Parça listesi
    pdf.cell(200, 10, txt="Parçalar:", ln=True)
    for part in project['parts']:
        pdf.cell(200, 10, txt=f"{part}", ln=True)

    # QR Kod
    qr_code_image = generate_qr_code(str(project['parts']))
    pdf.ln(10)  # boşluk ekle
    pdf.image(qr_code_image, x=10, w=50)

    pdf.output("project_quote.pdf")

# Ana Uygulama Arayüzü
def main_ui():
    st.title("Dolap Üretim Sistemi")
    
    # Proje Bilgilerini Girme
    st.subheader("Proje Bilgileri")
    project_name = st.text_input("Proje Adı")
    project_width = st.number_input("Dolap Genişliği (mm)", min_value=0)
    project_height = st.number_input("Dolap Yüksekliği (mm)", min_value=0)
    project_depth = st.number_input("Dolap Derinliği (mm)", min_value=0)
    
    if st.button("Yeni Proje Oluştur"):
        project = {
            'name': project_name,
            'width': project_width,
            'height': project_height,
            'depth': project_depth,
            'parts': []  # Boş bir parça listesi
        }
        st.session_state.project = project
        st.success("Proje oluşturuldu.")
    
    # Parça Ekleme
    if 'project' in st.session_state:
        st.subheader("Parça Listesi")
        part_name = st.text_input("Parça Adı")
        part_qty = st.number_input("Adet", min_value=1, step=1)

        if st.button("Parça Ekle"):
            part = {'name': part_name, 'quantity': part_qty}
            st.session_state.project['parts'].append(part)
            st.success(f"{part_name} eklendi.")
        
        # Parça Listesi Görüntüleme
        st.write("Parça Listesi:")
        for part in st.session_state.project['parts']:
            st.write(f"{part['name']} - {part['quantity']} adet")

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
