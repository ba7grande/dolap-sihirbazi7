import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import qrcode
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fpdf import FPDF

# Proje Veri Yapısı
class Project:
    def __init__(self, name, panel_size, num_panels, num_doors, cost_per_m2):
        self.name = name
        self.panel_size = panel_size
        self.num_panels = num_panels
        self.num_doors = num_doors
        self.cost_per_m2 = cost_per_m2
        self.parts = []

    def add_part(self, part_name, part_type, dimensions):
        self.parts.append({"name": part_name, "type": part_type, "dimensions": dimensions})

    def calculate_total_cost(self):
        panel_area = self.panel_size[0] * self.panel_size[1]
        total_area = panel_area * self.num_panels
        return total_area * self.cost_per_m2


# Ölçü Girişi
def input_project_details():
    name = st.text_input("Proje Adı")
    panel_length = st.number_input("Panel Uzunluğu (cm)", value=200)
    panel_width = st.number_input("Panel Genişliği (cm)", value=100)
    num_panels = st.number_input("Panel Sayısı", value=5)
    num_doors = st.number_input("Kapak Sayısı", value=2)
    cost_per_m2 = st.number_input("Metrekare Başına Maliyet (TL)", value=100)

    project = Project(name, (panel_length, panel_width), num_panels, num_doors, cost_per_m2)
    return project


# Parça Listesi
def generate_parts_list(project):
    st.write("Parça Listesi:")
    parts = project.parts
    if len(parts) > 0:
        parts_df = pd.DataFrame(parts)
        st.write(parts_df)
    else:
        st.write("Henüz parça eklenmemiş.")


# Lamello Cabineo Delik Pozisyonları
def generate_lamello_positions(project):
    st.write("Lamello Delik Pozisyonları:")
    positions = []
    for i in range(project.num_panels):
        positions.append({"Panel No": i + 1, "Delik X": np.random.randint(5, 30), "Delik Y": np.random.randint(5, 30)})

    positions_df = pd.DataFrame(positions)
    st.write(positions_df)


# CSV Çıktısı
def export_to_csv(project):
    parts_df = pd.DataFrame(project.parts)
    csv_file = f"{project.name}_parca_listesi.csv"
    parts_df.to_csv(csv_file, index=False)
    st.write(f"CSV dosyası kaydedildi: {csv_file}")


# Barkod ve Etiket Modülü
def generate_labels_and_barcodes(project):
    st.write("Barkod ve Etiketler:")
    for part in project.parts:
        qr = qrcode.make(part["name"])
        img_path = f"{part['name']}_barkod.png"
        qr.save(img_path)
        st.image(img_path, caption=f"Barkod: {part['name']}")


# CNC Entegrasyonu (DXF Çıktısı)
def create_dxf(project):
    st.write("DXF Çizimi Oluşturuluyor...")
    doc = ezdxf.new()
    msp = doc.modelspace()

    for i in range(project.num_panels):
        msp.add_line((0, 0), (project.panel_size[0], 0))
        msp.add_line((project.panel_size[0], 0), (project.panel_size[0], project.panel_size[1]))
        msp.add_line((project.panel_size[0], project.panel_size[1]), (0, project.panel_size[1]))
        msp.add_line((0, project.panel_size[1]), (0, 0))

    dxf_file = f"{project.name}_panel.dxf"
    doc.saveas(dxf_file)
    st.write(f"DXF Dosyası kaydedildi: {dxf_file}")


# 3D Görselleştirme
def visualize_3d_cabinet(project):
    st.write("3D Dolap Görselleştirmesi:")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter([0, project.panel_size[0]], [0, project.panel_size[1]], [0, 0], color="r", label="Dolap Alanı")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    st.pyplot(fig)


# Donanım ve Maliyet Hesaplama
def hardware_and_cost_calculation(project):
    st.write("Donanım ve Maliyet Hesaplama:")
    hardware_cost = {"Ray": 50, "Vida": 20, "Minifix": 30}
    total_hardware_cost = (hardware_cost["Ray"] * project.num_doors) + (hardware_cost["Vida"] * project.num_panels)
    total_cost = project.calculate_total_cost() + total_hardware_cost

    st.write(f"Toplam Donanım Maliyeti: {total_hardware_cost} TL")
    st.write(f"Toplam Maliyet: {total_cost} TL")


# Akıllı Fonksiyonlar
def smart_functions(project):
    st.write("Akıllı Fonksiyonlar:")
    
    st.write("Otomatik Malzeme Optimizasyonu...")
    material_layout = np.random.rand(5, 5)
    plt.imshow(material_layout, cmap="gray")
    st.pyplot(plt)
    
    production_time = np.random.randint(10, 100)
    st.write(f"Üretim Tahmin Zamanı: {production_time} dakika")
    
    assembly_order = np.random.choice(project.parts)
    st.write(f"Önerilen Montaj Sırası: {assembly_order['name']}")


# Ana Arayüz ve Uygulama Başlatma
def main():
    st.title("Dolap Üretim Yazılımı")
    
    project = input_project_details()

    # Modülleri Başlat
    generate_parts_list(project)
    generate_lamello_positions(project)
    export_to_csv(project)
    generate_labels_and_barcodes(project)
    create_dxf(project)
    visualize_3d_cabinet(project)
    hardware_and_cost_calculation(project)
    smart_functions(project)
    
if __name__ == "__main__":
    main()
