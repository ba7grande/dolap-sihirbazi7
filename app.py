import numpy as np
import pandas as pd
import qrcode
import matplotlib.pyplot as plt
import ezdxf
from fpdf import FPDF

# Örnek proje verisi
project = {
    'parts': ['panel1', 'panel2', 'panel3', 'panel4'],
    'measurements': {'width': 1000, 'height': 2000, 'depth': 500},
    'hardware': {'screws': 20, 'minifix': 10, 'hinges': 5},  # Donanım verisi
}

# Parça yerleşimi fonksiyonu (Akıllı fonksiyon)
def smart_functions(project):
    # 'project.parts' bir liste veya numpy array olmalı
    if isinstance(project['parts'], (list, np.ndarray)):
        # Eğer 'project.parts' doğru formatta ise
        assembly_order = np.random.choice(project['parts'])
        print(f"Assembly Order: {assembly_order}")
    else:
        print("project.parts doğru formatta değil!")

# PDF teklif şablonu oluşturma
def generate_pdf(project):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Dolap Teklifi", ln=True, align='C')
    
    # Proje bilgileri ekleme
    pdf.cell(200, 10, txt=f"Parça Listesi: {', '.join(project['parts'])}", ln=True)
    pdf.cell(200, 10, txt=f"Ölçüler: {project['measurements']}", ln=True)
    pdf.cell(200, 10, txt=f"Donanım: {project['hardware']}", ln=True)
    
    # PDF dosyasını kaydetme
    pdf.output("project_quote.pdf")
    print("PDF Teklif Oluşturuldu!")

# CSV çıktısı oluşturma
def generate_csv(project):
    data = {
        'Part': project['parts'],
        'Width': [project['measurements']['width']] * len(project['parts']),
        'Height': [project['measurements']['height']] * len(project['parts']),
        'Depth': [project['measurements']['depth']] * len(project['parts']),
    }
    df = pd.DataFrame(data)
    df.to_csv('project_parts.csv', index=False)
    print("CSV Dosyası Oluşturuldu!")

# QR kod üretme ve barkod oluşturma
def generate_qr_code(data, filename="qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    print(f"QR Kodu {filename} olarak kaydedildi.")

# CNC Entegrasyonu: DXF dosyası üretme
def generate_dxf(project):
    doc = ezdxf.new()
    msp = doc.modelspace()
    
    # Basit bir dikdörtgen dolap çizimi
    msp.add_lwpolyline([(0, 0), (0, project['measurements']['height']),
                         (project['measurements']['width'], project['measurements']['height']),
                         (project['measurements']['width'], 0), (0, 0)], close=True)
    
    doc.saveas('project.dxf')
    print("DXF Dosyası Oluşturuldu!")

# 3D Görselleştirme (Matplotlib ile basit görselleştirme)
def visualize_3d(project):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d([0, 0, 1], [0, 1, 1], [0, 0, 0], [project['measurements']['width']] * 3, [project['measurements']['height']] * 3, [project['measurements']['depth']] * 3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# Donanım ve maliyet hesaplama
def calculate_costs(project):
    # Örnek maliyet hesaplaması
    material_cost = (project['measurements']['width'] * project['measurements']['height']) * 0.02  # m² başına 0.02 TL
    hardware_cost = sum(project['hardware'].values()) * 0.5  # Donanım başına 0.5 TL
    total_cost = material_cost + hardware_cost
    print(f"Malzeme Maliyeti: {material_cost:.2f} TL")
    print(f"Donanım Maliyeti: {hardware_cost:.2f} TL")
    print(f"Toplam Maliyet: {total_cost:.2f} TL")
    return total_cost

# Akıllı fonksiyonlar
def optimize_materials(project):
    # Malzeme optimizasyonu (basit örnek)
    print("Malzeme optimizasyonu yapılıyor...")
    optimized_layout = np.random.choice(project['parts'], size=len(project['parts']), replace=False)
    print(f"Optimized layout: {optimized_layout}")

# Ana fonksiyon
def main():
    print("Proje Başlatılıyor...")
    
    # Smart Functions
    smart_functions(project)
    
    # PDF Teklif Oluşturma
    generate_pdf(project)
    
    # CSV Çıktısı Oluşturma
    generate_csv(project)
    
    # QR Kod Üretimi
    generate_qr_code('Parça QR Kodu')
    
    # CNC DXF Entegrasyonu
    generate_dxf(project)
    
    # 3D Görselleştirme
    visualize_3d(project)
    
    # Donanım ve Maliyet Hesaplama
    calculate_costs(project)
    
    # Malzeme Optimizasyonu
    optimize_materials(project)

# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    main()
