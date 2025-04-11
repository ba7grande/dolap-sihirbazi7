import streamlit as st
import pandas as pd

st.set_page_config(page_title="Alt Dolap Üretim", layout="wide")
st.title("📐 Basit Alt Dolap Üretim Hesaplama (Lamello Cabineo)")

st.markdown("Lamello Cabineo bağlantı sistemine göre parçaları ve bağlantı noktalarını listeler.")

# Giriş: Ölçüler
with st.form("ölçü_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        genislik = st.number_input("Dolap Genişliği (mm)", min_value=300, value=600, step=10)
    with col2:
        yukseklik = st.number_input("Dolap Yüksekliği (mm)", min_value=300, value=720, step=10)
    with col3:
        derinlik = st.number_input("Dolap Derinliği (mm)", min_value=300, value=560, step=10)

    plaka_kalinligi = 18  # sabit
    submit = st.form_submit_button("Hesapla")

if submit:
    st.subheader("📦 Parça Listesi")

    # Parça Hesapları
    parcalar = [
        {
            "Parça": "Yan Panel (2 adet)",
            "En": derinlik,
            "Boy": yukseklik,
            "Adet": 2
        },
        {
            "Parça": "Alt Panel",
            "En": derinlik,
            "Boy": genislik - (2 * plaka_kalinligi),
            "Adet": 1
        },
        {
            "Parça": "Üst Panel",
            "En": derinlik,
            "Boy": genislik - (2 * plaka_kalinligi),
            "Adet": 1
        },
        {
            "Parça": "Arka Panel (opsiyonel)",
            "En": genislik,
            "Boy": yukseklik,
            "Adet": 1
        },
        {
            "Parça": "Kapak (çift)",
            "En": genislik / 2,
            "Boy": yukseklik,
            "Adet": 2
        }
    ]

    df = pd.DataFrame(parcalar)
    st.dataframe(df, use_container_width=True)

    st.subheader("🔩 Lamello Cabineo Delik Yerleri (Yan Paneller İçin)")
    # Örnek delik yerleri - üst ve alt paneli bağlamak için
    delik_ust = 37  # üstten 37mm aşağı
    delik_alt = yukseklik - 37  # alttan 37mm yukarı

    st.markdown(f"""
    - Üst Panel Bağlantısı: **{delik_ust} mm**
    - Alt Panel Bağlantısı: **{delik_alt} mm**
    - Derinlik merkezde: **{plaka_kalinligi / 2} mm** delik açılır (CNC)
    """)

    st.success("Delik merkezleri CNC'ye göre ayarlandı. DXF entegrasyonu istersen, bir sonraki adımda ekleriz.")
