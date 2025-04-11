import streamlit as st
import ezdxf
import os
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dolap Sihirbazı 3D", layout="centered")
st.title("🧱 3D Dolap Toplama ve Bağlantı Önizleme")

# Kullanıcıdan ölçüleri al
st.subheader("📐 Ölçüleri Girin")
genislik = st.number_input("Genişlik (mm)", value=600)
yukseklik = st.number_input("Yükseklik (mm)", value=720)
derinlik = st.number_input("Derinlik (mm)", value=500)
kalinlik = st.number_input("Malzeme Kalınlığı (mm)", value=18)

st.subheader("🔩 Donatı Seçenekleri")
raf_sayisi = st.slider("Raf Sayısı", 0, 5, 2)
menteşe_adedi = st.radio("Menteşe Sayısı (kapakta)", [2, 3])

# Panel listesi
paneller = [
    {"isim": "sol_panel", "x": 0, "y": 0, "z": 0, "w": kalinlik, "h": yukseklik, "d": derinlik},
    {"isim": "sag_panel", "x": genislik - kalinlik, "y": 0, "z": 0, "w": kalinlik, "h": yukseklik, "d": derinlik},
    {"isim": "arka_panel", "x": kalinlik, "y": 0, "z": 0, "w": genislik - 2 * kalinlik, "h": yukseklik, "d": kalinlik},
    {"isim": "alt_panel", "x": kalinlik, "y": 0, "z": 0, "w": genislik - 2 * kalinlik, "h": kalinlik, "d": derinlik},
    {"isim": "ust_panel", "x": kalinlik, "y": yukseklik - kalinlik, "z": 0, "w": genislik - 2 * kalinlik, "h": kalinlik, "d": derinlik},
    {"isim": "kapak", "x": 0, "y": 0, "z": derinlik, "w": genislik, "h": yukseklik, "d": kalinlik}
]

# 3D Görselleştirme başlat
fig = go.Figure()
renkler = ["red", "green", "blue", "orange", "purple", "gray"]

# Panelleri kutu olarak çiz
for i, p in enumerate(paneller):
    x0, y0, z0 = p["x"], p["y"], p["z"]
    w, h, d = p["w"], p["h"], p["d"]
    x = [x0, x0+w, x0+w, x0, x0, x0+w, x0+w, x0]
    y = [y0, y0, y0+h, y0+h, y0, y0, y0+h, y0+h]
    z = [z0, z0, z0, z0, z0+d, z0+d, z0+d, z0+d]
    fig.add_trace(go.Mesh3d(
        x=x, y=y, z=z,
        color=renkler[i % len(renkler)],
        opacity=0.5,
        name=p["isim"]
    ))

# Cabineo delikleri: sol_panel üzerinde 4 köşe
cabineo_delikler = [
    (kalinlik / 2, kalinlik / 2, derinlik / 2),
    (kalinlik / 2, yukseklik - kalinlik / 2, derinlik / 2),
    (kalinlik / 2, kalinlik / 2, derinlik - kalinlik / 2),
    (kalinlik / 2, yukseklik - kalinlik / 2, derinlik - kalinlik / 2),
]

# Menteşe delikleri: kapakta yukarıdan ve aşağıdan 100mm
menteşe_delikler = [
    (kalinlik + 35 / 2, 100, derinlik + kalinlik / 2),
    (kalinlik + 35 / 2, yukseklik - 100, derinlik + kalinlik / 2)
]
if menteşe_adedi == 3:
    menteşe_delikler.insert(1, (kalinlik + 35 / 2, yukseklik / 2, derinlik + kalinlik / 2))

# Delikleri scatter ile göster
for x, y, z in cabineo_delikler:
    fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z],
        mode='markers', marker=dict(size=6, color='black'), name='Cabineo'))

for x, y, z in menteşe_delikler:
    fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z],
        mode='markers', marker=dict(size=10, color='blue'), name='Menteşe'))

# Sahne ayarları
fig.update_layout(scene=dict(
    xaxis_title='X (Genişlik)',
    yaxis_title='Y (Yükseklik)',
    zaxis_title='Z (Derinlik)'
), margin=dict(l=0, r=0, b=0, t=0))

st.subheader("🧱 3D Katı Model ve Delik Önizleme")
st.plotly_chart(fig, use_container_width=True)

st.info("Modeldeki siyah noktalar Cabineo deliklerini, mavi noktalar menteşe deliklerini gösterir.")
