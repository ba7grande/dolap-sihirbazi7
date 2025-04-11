import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import ezdxf
import os
from fpdf import FPDF

st.set_page_config(page_title="Dolap Sihirbazı 3D", layout="wide")
st.title("🧱 Çoklu Kapak ve Çekmece Yapılandırmalı Dolap Tasarımı")

st.sidebar.header("🔧 Genel Ayarlar")
kalinlik = st.sidebar.number_input("Panel Kalınlığı (mm)", value=18)
raf_araligi = st.sidebar.number_input("Raflar Arası Mesafe (cm)", value=30) * 10
menteşe_adedi = st.sidebar.number_input("Menteşe Sayısı", min_value=0, max_value=5, value=2)
cabineo_yon = st.sidebar.selectbox("Cabineo Delik Yönü", ["Üst", "Alt", "Sağ", "Sol", "Hepsi"])

st.sidebar.header("📐 Dolap Bölmeleri")
bolme_sayisi = st.sidebar.number_input("Bölme Sayısı", min_value=1, max_value=10, value=1)

# DXF fonksiyonları

def dxf_add_mentese(msp, x, y):
    msp.add_circle(center=(x, y), radius=17.5)

def dxf_add_cabineo(msp, x, y):
    msp.add_circle(center=(x, y), radius=6)
    msp.add_lwpolyline([(x-7, y-7), (x+7, y-7), (x+7, y+7), (x-7, y+7)], close=True)

# 3D çizim için mesh fonksiyonları

fig = go.Figure()

def add_mentese(x, y, z):
    theta = np.linspace(0, 2 * np.pi, 16)
    r = 17.5
    cx = r * np.cos(theta)
    cy = r * np.sin(theta)
    x_vals, y_vals, z_vals = [], [], []
    for dz in [0, 12]:
        x_vals.extend(x + cx)
        y_vals.extend(y + cy)
        z_vals.extend([z + dz] * len(cx))
    fig.add_trace(go.Mesh3d(x=x_vals, y=y_vals, z=z_vals, opacity=1.0, color='blue', name='Menteşe'))

def add_cabineo(x, y, z):
    theta = np.linspace(0, 2 * np.pi, 16)
    cx = 6 * np.cos(theta)
    cy = 6 * np.sin(theta)
    x_vals, y_vals, z_vals = [], [], []
    for dz in [0, 10]:
        x_vals.extend(x + cx)
        y_vals.extend(y + cy)
        z_vals.extend([z + dz] * len(cx))
    fig.add_trace(go.Mesh3d(x=x_vals, y=y_vals, z=z_vals, opacity=1.0, color='black', name='Cabineo'))
    hw = 7
    fig.add_trace(go.Mesh3d(x=[x - hw, x + hw, x + hw, x - hw], y=[y - hw, y - hw, y + hw, y + hw], z=[z + 11] * 4, i=[0], j=[1], k=[2], color='gray', name='Cabineo Başlık', opacity=1.0))

# Panel üretimi ve çizim

bolmeler = []
if not os.path.exists("paneller"):
    os.makedirs("paneller")

for i in range(bolme_sayisi):
    st.subheader(f"📦 Bölme {i+1} Yapılandırması")
    gen = st.number_input(f"Bölme {i+1} Genişlik (mm)", value=600, key=f"gen{i}")
    yuk = st.number_input(f"Bölme {i+1} Yükseklik (mm)", value=720, key=f"yuk{i}")
    der = st.number_input(f"Bölme {i+1} Derinlik (mm)", value=500, key=f"der{i}")
    kapak_sayisi = st.number_input(f"Kapak Sayısı", min_value=0, value=1, key=f"kapak{i}")
    cekmece_sayisi = st.number_input(f"Çekmece Sayısı", min_value=0, value=0, key=f"cekmece{i}")

    panel_dxf = ezdxf.new()
    msp = panel_dxf.modelspace()
    msp.add_lwpolyline([(0, 0), (gen, 0), (gen, yuk), (0, yuk)], close=True)

    # Delikler DXF'e
    dxf_add_cabineo(msp, 37, yuk / 2)
    dxf_add_cabineo(msp, gen - 37, yuk / 2)
    dxf_add_cabineo(msp, gen / 2, 37)
    dxf_add_cabineo(msp, gen / 2, yuk - 37)

    aralik = yuk / (menteşe_adedi + 1) if menteşe_adedi > 0 else 0
    for m in range(menteşe_adedi):
        y_merkez = (m + 1) * aralik
        dxf_add_mentese(msp, 5 + 17.5, y_merkez)
        dxf_add_mentese(msp, gen - 5 - 17.5, y_merkez)

    panel_path = f"paneller/bolme_{i+1}.dxf"
    panel_dxf.saveas(panel_path)

    # 3D Görünüm için delikler
    add_cabineo(37, yuk / 2, der)
    add_cabineo(gen - 37, yuk / 2, der)
    add_cabineo(gen / 2, 37, der)
    add_cabineo(gen / 2, yuk - 37, der)
    for m in range(menteşe_adedi):
        y_merkez = (m + 1) * aralik
        add_mentese(5 + 17.5, y_merkez, der)
        add_mentese(gen - 5 - 17.5, y_merkez, der)

    bolmeler.append({"gen": gen, "yuk": yuk, "der": der, "kapak": kapak_sayisi, "cekmece": cekmece_sayisi})

fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'), margin=dict(l=0, r=0, b=0, t=0))
st.subheader("🧱 3D Katı Model ve Bağlantı Önizleme")
st.plotly_chart(fig, use_container_width=True)

# 🧩 Nesting Görseli
st.subheader("🧩 Anlık Nesting Yerleşimi")
fig2d, ax = plt.subplots(figsize=(6, 8))
plaka_w, plaka_h = 2100, 2800
x, y, max_y = 0, 0, 0
ax.set_xlim(0, plaka_w)
ax.set_ylim(0, plaka_h)
ax.set_title("Plaka Yerleşimi")
ax.set_xlabel("Genişlik")
ax.set_ylabel("Yükseklik")
plt.gca().invert_yaxis()

for i, b in enumerate(bolmeler):
    w, h = b["gen"], b["yuk"]
    if x + w > plaka_w:
        x = 0
        y += max_y + 10
        max_y = 0
    if y + h > plaka_h:
        continue
    rect = plt.Rectangle((x, y), w, h, edgecolor='black', facecolor='lightgray')
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, f"Bölme {i+1}", ha='center', va='center', fontsize=7)
    x += w + 10
    if h > max_y:
        max_y = h

st.pyplot(fig2d)
