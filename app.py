import streamlit as st
import ezdxf

# Sabitler
PLAKA_GENISLIK = 2440
PLAKA_YUKSEKLIK = 1220
ARA_BOSLUK = 10
CABINEO_CAPI = 15
CABINEO_MARGIN = 64
CABINEO_SPACING = 128

# Kullanıcıdan Parça Girişlerini Al
st.title("Nesting ve Cabineo Delikleri Hesaplama")

# Parçaların ölçülerini kullanıcıdan alıyoruz
parcalar = []
num_parca = st.number_input("Parça sayısı", min_value=1, max_value=20, value=4)

for i in range(num_parca):
    with st.expander(f"Parça {i + 1}"):
        genislik = st.number_input(f"Parça {i + 1} Genişlik (mm)", min_value=100, max_value=2000, value=600)
        yukseklik = st.number_input(f"Parça {i + 1} Yükseklik (mm)", min_value=100, max_value=2000, value=400)
        parcalar.append((genislik, yukseklik, 18))  # 18 mm kalınlık varsayıyoruz

# DXF Dosyası Oluşturulması İçin Fonksiyon
def add_cabineo_holes(msp, x0, y0, gen, yuk):
    x_positions = list(range(CABINEO_MARGIN, int(gen - CABINEO_MARGIN) + 1, CABINEO_SPACING))
    y_center = y0 + yuk / 2

    for x in x_positions:
        msp.add_circle(center=(x0 + x, y_center), radius=CABINEO_CAPI / 2, dxfattribs={'layer': 'cabineo'})

def nesting_with_cabineo(parcalar, plaka_genislik, plaka_yukseklik, bosluk, filename="nesting_cabineo.dxf"):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Plaka çizimi
    msp.add_lwpolyline([
        (0, 0),
        (plaka_genislik, 0),
        (plaka_genislik, plaka_yukseklik),
        (0, plaka_yukseklik),
        (0, 0)
    ], dxfattribs={'layer': 'plaka'})

    x = y = 0
    max_satir_yukseklik = 0

    for idx, (gen, yuk, kalinlik) in enumerate(parcalar):
        if x + gen > plaka_genislik:
            x = 0
            y += max_satir_yukseklik + bosluk
            max_satir_yukseklik = 0

        if y + yuk > plaka_yukseklik:
            st.warning(f"Parça sığmadı: {idx+1}. parça ({gen}x{yuk})")
            continue

        # Parça çerçevesi
        msp.add_lwpolyline([
            (x, y),
            (x + gen, y),
            (x + gen, y + yuk),
            (x, y + yuk),
            (x, y)
        ], dxfattribs={'layer': 'parca'})

        # Parça etiketi
        msp.add_text(f"P{idx+1}", dxfattribs={'height': 10}).set_pos((x + 5, y + 5))

        # Cabineo delikleri
        add_cabineo_holes(msp, x, y, gen, yuk)

        x += gen + bosluk
        max_satir_yukseklik = max(max_satir_yukseklik, yuk)

    doc.saveas(filename)
    st.success(f"DXF kaydedildi: {filename}")

# Eğer butona basılırsa DXF dosyasını oluştur
if st.button("DXF Dosyasını Oluştur"):
    # Dosya adı belirle
    filename = "nesting_cabineo.dxf"
    
    # Nesting ve Cabineo fonksiyonunu çağır
    nesting_with_cabineo(parcalar, PLAKA_GENISLIK, PLAKA_YUKSEKLIK, ARA_BOSLUK, filename)
    
    # Dosya indir butonu
    with open(filename, "rb") as file:
        st.download_button(label="DXF Dosyasını İndir", data=file, file_name=filename)

