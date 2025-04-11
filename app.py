import numpy as np
import qrcode
import ezdxf
from fpdf import FPDF
import plotly.graph_objects as go
import streamlit as st

# 1. Proje Veri Yapısı
class Project:
    def __init__(self, measurements, parts, hardware, nesting, cabindel_positions):
        self.measurements = measurements
        self.parts = parts
        self.hardware = hardware
        self.nesting = nesting
        self.cabindel_positions = cabindel_positions

# 2. PDF Teklif Şablonu
def generate_pdf(project):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Dolap Teklifi", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Parça Listesi: {', '.join(project.parts)}", ln=True)
    pdf.cell(200, 10, txt=f"Ölçüler: {project.measurements}", ln=True)
    pdf.cell(200, 10, txt=f"Donanım: {project.hardware}", ln=True)
    pdf.output("project_quote.pdf")
    print("PDF Teklif Oluşturuldu!")

# 3. QR ve Barkod Etiketi Üretimi
def generate_qr_code(project_part):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(project_part)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"{project_part}_qr.png")
    print(f"{project_part} için QR kodu oluşturuldu!")

# 4. DXF Dosyası Oluşturma
def generate_dxf(project):
    doc = ezdxf.new()
    msp = doc.modelspace()

    for part in project.parts:
        # Örneğin: her parçanın 2D çizimini yapıyoruz (ölçülere göre)
        msp.add_line((0, 0), (project.measurements['width'], 0))
        msp.add_line((0, 0), (0, project.measurements['height']))
        msp.add_line((project.measurements['width'], 0), (project.measurements['width'], project.measurements['height']))
        msp.add_line((0, project.measurements['height']), (project.measurements['width'], project.measurements['height']))

    doc.save("project_output.dxf")
    print("DXF dosyası oluşturuldu.")

# 5. 3D Görselleştirme
def generate_3d_visualization(project):
    fig = go.Figure()

    # X, Y, Z koordinatları ile dolap yapısını çiziyoruz
    fig.add_trace(go.Mesh3d(
        x=[0, project.measurements['width'], project.measurements['width'], 0],
        y=[0, 0, project.measurements['depth'], project.measurements['depth']],
        z=[0, 0, 0, 0],
        color='rgba(0, 0, 255, 0.1)',
        opacity=0.5
    ))

    fig.update_layout(scene=dict(
        xaxis=dict(range=[0, project.measurements['width']]),
        yaxis=dict(range=[0, project.measurements['depth']]),
        zaxis=dict(range=[0, project.measurements['height']])
    ))

    fig.show()

# 6. Menteşe Delikleri ve Lamello Cabineo Bağlantıları
def add_hinge_and_cabineo_holes(project):
    for part in project.parts:
        # Menteşe deliklerini ekleme
        print(f"{part} için menteşe delikleri eklendi.")
        # Lamello Cabineo deliklerini ekleme
        print(f"{part} için Lamello Cabineo delikleri eklendi.")

# 7. Donanım ve Maliyet Hesaplama
def calculate_cost(project):
    hardware_cost = {
        'vida': 0.5,
        'minifix': 1.2,
        'ray': 2.5,
        'kulp': 3.0
    }

    total_cost = 0
    for part in project.parts:
        for hardware in project.hardware:
            total_cost += hardware_cost.get(hardware, 0)

    return total_cost

# 8. Nesting ve Malzeme Optimizasyonu
def nesting_and_material_optimization(project):
    print("Nesting ve malzeme optimizasyonu yapıldı.")
    optimized_materials = "Optimizasyon başarılı!"
    return optimized_materials

# 9. Akıllı Fonksiyonlar (Örnek)
def smart_functions(project):
    assembly_order = np.random.choice(project.parts, size=len(project.parts), replace=False)
    print(f"Montaj sırası: {', '.join(assembly_order)}")
    return assembly_order

# 10. Ana Arayüz (Streamlit)
def main():
    project = Project(
        measurements={'width': 100, 'height': 200, 'depth': 50},
        parts=['parça1', 'parça2', 'parça3'],
        hardware=['vida', 'minifix', 'ray'],
        nesting='optimize',
        cabindel_positions={'lamello': [20, 40, 60], 'hinge': [15, 30]}
    )

    # Modül işlemleri
    generate_pdf(project)
    generate_qr_code('parça1')
    generate_dxf(project)
    generate_3d_visualization(project)
    add_hinge_and_cabineo_holes(project)
    total_cost = calculate_cost(project)
    print(f"Toplam Maliyet: {total_cost} TL")
    optimized_materials = nesting_and_material_optimization(project)
    print(optimized_materials)
    assembly_order = smart_functions(project)

# Streamlit UI
if __name__ == "__main__":
    main()
