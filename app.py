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

bolmeler = []
for i in range(bolme_sayisi):
    st.subheader(f"📦 Bölme {i+1} Yapılandırması")
    gen = st.number_input(f"Bölme {i+1} Genişlik (mm)", value=600, key=f"gen{i}")
    yuk = st.number_input(f"Bölme {i+1} Yükseklik (mm)", value=720, key=f"yuk{i}")
    der = st.number_input(f"Bölme {i+1} Derinlik (mm)", value=500, key=f"der{i}")
    kapak_sayisi = st.number_input(f"Kapak Sayısı", min_value=0, value=1, key=f"kapak{i}")
    cekmece_sayisi = st.number_input(f"Çekmece Sayısı", min_value=0, value=0, key=f"cekmece{i}")
    bolmeler.append({
        "gen": gen, "yuk": yuk, "der": der,
        "kapak": kapak_sayisi,
        "cekmece": cekmece_sayisi
    })

fig = go.Figure()
z_offset = 0
kesim_listesi = []

if not os.path.exists("paneller"):
    os.makedirs("paneller")
if not os.path.exists("nesting"):
    os.makedirs("nesting")
if not os.path.exists("etiketler"):
    os.makedirs("etiketler")

for i, b in enumerate(bolmeler):
    for j in range(2):
        kesim_listesi.append({"Parça": f"Yan Panel {j+1} Bölme {i+1}", "Genişlik": b["yuk"], "Yükseklik": b["der"], "Kalınlık": kalinlik})
    for k in range(b["kapak"]):
        kesim_listesi.append({"Parça": f"Kapak {k+1} Bölme {i+1}", "Genişlik": b["gen"], "Yükseklik": b["yuk"], "Kalınlık": kalinlik})
    for c in range(b["cekmece"]):
        yuk_parca = b["yuk"] // (b["cekmece"] or 1)
        kesim_listesi.append({"Parça": f"Çekmece {c+1} Bölme {i+1}", "Genişlik": b["gen"], "Yükseklik": yuk_parca, "Kalınlık": kalinlik})
    z_offset += b["gen"] + 50

fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'), margin=dict(l=0, r=0, b=0, t=0))
st.subheader("🧱 3D Katı Model ve Bölme Görünümü")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Kesim Listesi")
df = pd.DataFrame(kesim_listesi)
st.dataframe(df)
csv_buffer = df.to_csv(index=False).encode()
st.download_button("📥 Kesim Listesini İndir (CSV)", data=csv_buffer, file_name="kesim_listesi.csv", mime="text/csv")

# 🔄 Nesting DXF
st.subheader("🧩 Nesting Planı (DXF)")
plaka_w, plaka_h = 2100, 2800
x, y, max_y = 0, 0, 0
nesting_dxf = ezdxf.new()
nesting_msp = nesting_dxf.modelspace()

for i, row in df.iterrows():
    w, h = row["Genişlik"], row["Yükseklik"]
    if x + w > plaka_w:
        x = 0
        y += max_y + 10
        max_y = 0
    if y + h > plaka_h:
        continue
    nesting_msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], close=True)
    text = nesting_msp.add_text(row["Parça"], dxfattribs={"height": 10})
    text.dxf.insert = (x + 10, y + 10)
    x += w + 10
    if h > max_y:
        max_y = h

nesting_path = "nesting/nesting_plan.dxf"
nesting_dxf.saveas(nesting_path)
st.download_button("📥 Nesting DXF Planını İndir", data=open(nesting_path, "rb"), file_name="nesting_plan.dxf")

# 🖨️ Etiket PDF üretimi
st.subheader("🏷️ PDF Etiket Üretimi")
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for row in df.itertuples():
    pdf.add_page()
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 20, txt=f"{row.Parça}", ln=True, align="C")
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=f"{row.Genişlik} x {row.Yükseklik} x {row.Kalınlık} mm", ln=True, align="C")

etiket_path = "etiketler/etiketler.pdf"
pdf.output(etiket_path)
st.download_button("📥 PDF Etiketleri İndir", data=open(etiket_path, "rb"), file_name="etiketler.pdf")
