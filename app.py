import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from fpdf import FPDF

# Örnek proje verisi
projects = [
    {"ID": 1, "Proje Adı": "Dolap 1", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-01", "Bitiş Tarihi": "2025-04-10", "Panel Sayısı": 12, "Kapak Sayısı": 4, "Toplam Maliyet": 5000, "İlerleme": 60},
    {"ID": 2, "Proje Adı": "Dolap 2", "Durum": "Tamamlandı", "Başlangıç Tarihi": "2025-03-01", "Bitiş Tarihi": "2025-03-15", "Panel Sayısı": 8, "Kapak Sayısı": 2, "Toplam Maliyet": 3000, "İlerleme": 100},
    {"ID": 3, "Proje Adı": "Dolap 3", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-05", "Bitiş Tarihi": "2025-04-12", "Panel Sayısı": 15, "Kapak Sayısı": 5, "Toplam Maliyet": 7000, "İlerleme": 80},
]

# Kullanıcı Rolü Yönetimi
def user_role_management():
    st.sidebar.title("Kullanıcı ve Rol Yönetimi")
    role = st.sidebar.selectbox("Kullanıcı Rolü", ["Yönetici", "Proje Yöneticisi", "Kullanıcı"])
    if role == "Yönetici":
        st.sidebar.subheader("Yönetici Paneli")
        st.sidebar.text("Yönetici olarak projeleri düzenleyebilir ve raporları görüntüleyebilirsiniz.")
    elif role == "Proje Yöneticisi":
        st.sidebar.subheader("Proje Yöneticisi Paneli")
        st.sidebar.text("Proje yöneticisi olarak projelere dair ilerleme güncellemeleri yapabilirsiniz.")
    else:
        st.sidebar.subheader("Kullanıcı Paneli")
        st.sidebar.text("Kullanıcı olarak yalnızca mevcut projeleri görüntüleyebilirsiniz.")

# Basit 3D Dolap Görselleştirici
def display_cabinet(project):
    st.subheader(f"{project['Proje Adı']} 3D Görselleştirme")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Dolap Boyutları
    width = 100  # Genişlik
    height = 200  # Yükseklik
    depth = 50  # Derinlik

    # Raf Sayısı ve Yükseklik
    shelf_count = project["Panel Sayısı"] // 2
    shelf_height = height / (shelf_count + 1)

    # Dolap Zemin (Taban)
    ax.bar3d(0, 0, 0, width, depth, height, color='lightgrey', alpha=0.6)

    # Rafları ekleyelim
    for i in range(shelf_count):
        shelf_z = (i + 1) * shelf_height  # Raf yüksekliği
        ax.bar3d(0, 0, shelf_z, width, depth, 5, color='brown', alpha=0.8)

    # Kapakları ekleyelim (sol ve sağ)
    ax.bar3d(0, 0, 0, 5, depth, height, color='blue', alpha=0.9)  # Sol kapak
    ax.bar3d(width-5, 0, 0, 5, depth, height, color='blue', alpha=0.9)  # Sağ kapak

    # Eksen etiketleri
    ax.set_xlabel('Width (Genişlik)')
    ax.set_ylabel('Depth (Derinlik)')
    ax.set_zlabel('Height (Yükseklik)')
    ax.set_title('Basit 3D Dolap Görselleştirmesi')

    # Görselleştirmeyi göster
    st.pyplot(fig)

# Lamello Deliği ve Delik Pozisyonları
def lamello_hole_positions():
    st.subheader("Lamello Delik Pozisyonları ve 3D Gösterimi")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([10, 20, 30], [10, 20, 30], [10, 20, 30], c='r', marker='o')  # Delik noktaları
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title('Lamello Delik Pozisyonları')

    st.pyplot(fig)

# DXF ve Delik Pozisyonlarının Eşleşmesi
def dxf_matching():
    st.subheader("DXF Dosyası ve Delik Pozisyonlarının Eşleşmesi")
    st.write("DXF dosyasındaki delik pozisyonlarıyla, Lamello sistemindeki delik pozisyonlarının nasıl eşleştiği burada gösterilecek.")
    st.write("Bu işlem için DXF dosyasının okunması, pozisyonların tespiti ve karşılaştırılması gerekmektedir.")

# PDF Teklif Şablonu Tasarımı
def pdf_quote_template():
    st.subheader("PDF Teklif Şablonu")
    st.write("Teklif şablonunu oluşturmak için gerekli parametreleri girin:")
    project_name = st.text_input("Proje Adı")
    client_name = st.text_input("Müşteri Adı")
    total_cost = st.number_input("Toplam Maliyet", min_value=0)
    
    if st.button("Teklif Oluştur"):
        st.write(f"Teklif Başlığı: {project_name}")
        st.write(f"Müşteri: {client_name}")
        st.write(f"Toplam Maliyet: {total_cost} TL")
        
        # PDF Oluşturma
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Teklif - " + project_name, ln=True, align='C')
        pdf.cell(200, 10, txt=f"Müşteri: {client_name}", ln=True)
        pdf.cell(200, 10, txt=f"Toplam Maliyet: {total_cost} TL", ln=True)
        pdf.output(f"Teklif_{project_name}.pdf")

        st.write("Teklif başarıyla oluşturuldu ve PDF'ye kaydedildi.")

# Ana Kullanıcı Arayüzü
def main_ui(projects):
    st.title("Dolap Üretim Programı")

    # Kullanıcı yönetimi
    user_role_management()

    # Proje Seçimi
    selected_project_id = st.selectbox("Proje Seçin", [project["Proje Adı"] for project in projects])
    selected_project = next(project for project in projects if project["Proje Adı"] == selected_project_id)

    # Proje Güncellemeleri
    st.subheader(f"{selected_project['Proje Adı']} Proje Detayları")
    display_cabinet(selected_project)
    lamello_hole_positions()

    # DXF ve Delik Pozisyonları
    dxf_matching()

    # Teklif Şablonu
    pdf_quote_template()

if __name__ == "__main__":
    main_ui(projects)
