import streamlit as st
import ezdxf
import os
import pandas as pd

st.set_page_config(page_title="Dolap Sihirbazı", layout="centered")
st.title("🛠️ Dolap Toplama Sihirbazı")

# 1️⃣ Kullanıcıdan ölçü ve seçenek girişi
st.subheader("📐 Ölçüleri Girin")
genislik = st.number_input("Genişlik (mm)", value=600)
yukseklik = st.number_input("Yükseklik (mm)", value=720)
derinlik = st.number_input("Derinlik (mm)", value=500)
kalinlik = st.number_input("Malzeme Kalınlığı (mm)", value=18)

st.subheader("🔩 Donatı Seçenekleri")
raf_sayisi = st.slider("Raf Sayısı", 0, 5, 2)
cekmece_sayisi = st.slider("Çekmece Sayısı", 0, 4, 0)
menteşe_adedi = st.radio("Menteşe Sayısı (kapakta)", [2, 3])

# Panel bilgileri hesapla
paneller = [
    {"isim": "sol_panel", "w": derinlik, "h": yukseklik},
    {"isim": "sag_panel", "w": derinlik, "h": yukseklik},
    {"isim": "arka_panel", "w": genislik, "h": yukseklik},
    {"isim": "alt_panel", "w": genislik - 2 * kalinlik, "h": derinlik},
    {"isim": "ust_panel", "w": genislik - 2 * kalinlik, "h": derinlik},
    {"isim": "kapak", "w": genislik, "h": yukseklik}
]

def dxf_ciz(panel, klasor, delik_offset=37, delik_cap=5, raflar=False, menteşe_yap=False):
    w, h = panel["w"], panel["h"]
    doc = ezdxf.new()
    msp = doc.modelspace()
    msp.add_lwpolyline([(0, 0), (w, 0), (w, h), (0, h)], close=True)
    for x in [delik_offset, w - delik_offset]:
        for y in [delik_offset, h - delik_offset]:
            msp.add_circle((x, y), delik_cap)
    if raflar:
        bolme_sayisi = raf_sayisi + 1
        aralik = h / bolme_sayisi
        for i in range(1, bolme_sayisi):
            y_raf = i * aralik
            msp.add_circle((delik_offset, y_raf), 3)
            msp.add_circle((w - delik_offset, y_raf), 3)
    if menteşe_yap:
        menteşe_yerleri = [100]
        if menteşe_adedi == 3:
            menteşe_yerleri.append(h / 2)
        menteşe_yerleri.append(h - 100)
        for y in menteşe_yerleri:
            msp.add_circle((delik_offset, y), 5)
    os.makedirs(klasor, exist_ok=True)
    doc.saveas(f"{klasor}/{panel['isim']}.dxf")

if st.button("📁 DXF + Nesting + CSV Üret"):
    klasor = "paneller_dxf"
    for p in paneller:
        if "panel" in p["isim"]:
            raf_var = p["isim"] in ["sol_panel", "sag_panel"] and raf_sayisi > 0
            dxf_ciz(p, klasor, raflar=raf_var)
        elif p["isim"] == "kapak":
            dxf_ciz(p, klasor, menteşe_yap=True)

    df = pd.DataFrame([
        {"Parça": p["isim"], "Genişlik": int(p["w"]), "Yükseklik": int(p["h"]), "Adet": 1}
        for p in paneller
    ])
    df.to_csv("kesim_listesi.csv", index=False)

    # Nesting işlemi
    doc = ezdxf.new()
    msp = doc.modelspace()
    x, y, max_y = 0, 0, 0
    plaka_w, plaka_h = 2100, 2800
    padding = 10

    for p in paneller:
        file = f"{klasor}/{p['isim']}.dxf"
        if not os.path.exists(file):
            continue
        panel_doc = ezdxf.readfile(file)
        panel_msp = panel_doc.modelspace()
        w, h = p["w"], p["h"]

        if x + w > plaka_w:
            x = 0
            y += max_y + padding
            max_y = 0
        if y + h > plaka_h:
            st.warning(f"{p['isim']} plakaya sığmadı, atlandı.")
            continue

        for e in panel_msp:
            try:
                e_copy = e.copy()
                e_copy.translate(dx=x, dy=y)
                msp.add_entity(e_copy)
            except Exception as err:
                st.warning(f"{p['isim']} parçasında eleman atlandı: {e.dxftype()} ({str(err)})")

        x += w + padding
        if h > max_y:
            max_y = h

    doc.saveas("yerlesim.dxf")
    st.success("✅ DXF, nesting ve kesim listesi üretildi!")

    # 📥 İndirme Butonları
    with open("kesim_listesi.csv", "rb") as f:
        st.download_button("📥 Kesim Listesini İndir", f, file_name="kesim_listesi.csv")

    with open("yerlesim.dxf", "rb") as f:
        st.download_button("📥 Yerleşim DXF'ini İndir", f, file_name="yerlesim.dxf")

    for p in paneller:
        dosya_yolu = f"{klasor}/{p['isim']}.dxf"
        if os.path.exists(dosya_yolu):
            with open(dosya_yolu, "rb") as f:
                st.download_button(f"📥 {p['isim']} DXF indir", f, file_name=f"{p['isim']}.dxf")
