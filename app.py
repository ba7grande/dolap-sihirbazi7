import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import ezdxf
import os

st.set_page_config(page_title="Dolap Sihirbazı 3D", layout="centered")
st.title("🧱 Dolap Toplama ve Bağlantı Önizleme")

st.subheader("📦 Panel Türü ve Sayısı")
panel_turleri = ["Yan Panel", "Orta Panel", "Kapak", "Çekmece"]
panel_listesi = []

for tur in panel_turleri:
    adet = st.number_input(f"{tur} Adedi", min_value=0, max_value=10, value=2 if tur == "Yan Panel" else 1)
    genislik = st.number_input(f"{tur} Genişliği (mm)", value=600 if tur != "Kapak" else 595)
    yukseklik = st.number_input(f"{tur} Yüksekliği (mm)", value=720)
    derinlik = st.number_input(f"{tur} Derinliği (mm)", value=500)
    panel_listesi.append({"tur": tur, "adet": adet, "gen": genislik, "yuk": yukseklik, "der": derinlik})

kalinlik = st.number_input("Panel Kalınlığı (mm)", value=18)
raf_araligi = st.number_input("Raflar Arası Mesafe (cm)", value=30) * 10
kenar_radius = st.number_input("Kenar Radius (mm)", value=0)
kenarlar = st.multiselect("Radius Uygulanacak Kenarlar", ["Üst", "Alt", "Sağ", "Sol"])

st.subheader("🔩 Donatı Seçenekleri")
menteşe_adedi = st.number_input("Menteşe Sayısı", min_value=0, max_value=5, value=2)
menteşe_cap = 35
cabineo_yon = st.selectbox("Cabineo Delik Yönü", ["Üst", "Alt", "Sağ", "Sol", "Hepsi"])

fig = go.Figure()
renk_map = {"Yan Panel": "wheat", "Orta Panel": "burlywood", "Kapak": "lightblue", "Çekmece": "lightgray"}
z_offset = 0
kesim_listesi = []

if not os.path.exists("paneller"):
    os.makedirs("paneller")

for p in panel_listesi:
    for i in range(p["adet"]):
        x0, y0, z0 = 0, 0, z_offset
        w, h, d = kalinlik, p["yuk"], p["der"]
        x = [x0, x0+w, x0+w, x0, x0, x0+w, x0+w, x0]
        y = [y0, y0, y0+h, y0+h, y0, y0, y0+h, y0+h]
        z = [z0, z0, z0, z0, z0+d, z0+d, z0+d, z0+d]
        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, color=renk_map.get(p["tur"], "wheat"), opacity=1.0, name=f"{p['tur']} {i+1}"))

        raf_sayisi = int(h // raf_araligi) if p["tur"] in ["Yan Panel", "Orta Panel"] else 0
        for r in range(1, raf_sayisi):
            ry = y0 + r * raf_araligi
            fig.add_trace(go.Scatter3d(x=[x0+w/2], y=[ry], z=[z0+d/2], mode='markers', marker=dict(size=4, color='green'), name='Raf'))

        kesim_listesi.append({"Parça": f"{p['tur']} {i+1}", "Genişlik": p["gen"], "Yükseklik": p["yuk"], "Kalınlık": kalinlik})

        doc = ezdxf.new()
        msp = doc.modelspace()
        msp.add_lwpolyline([(0, 0), (p["gen"], 0), (p["gen"], p["yuk"]), (0, p["yuk"])], close=True)
        msp.add_circle((35, 35), 5)
        msp.add_circle((p["gen"] - 35, 35), 5)
        msp.add_circle((35, p["yuk"] - 35), 5)
        msp.add_circle((p["gen"] - 35, p["yuk"] - 35), 5)
        doc.saveas(f"paneller/{p['tur'].lower()}_{i+1}.dxf")
        z_offset += d + 30

fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'), margin=dict(l=0, r=0, b=0, t=0))
st.subheader("🧱 3D Katı Model ve Bağlantı Önizleme")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Kesim Listesi")
df = pd.DataFrame(kesim_listesi)
st.dataframe(df)

csv_buffer = df.to_csv(index=False).encode()
st.download_button("📥 Kesim Listesini İndir (CSV)", data=csv_buffer, file_name="kesim_listesi.csv", mime="text/csv")

st.subheader("🧩 Nesting Yerleşim Planı")
fig2d, ax = plt.subplots(figsize=(6, 8))
x, y, max_y = 0, 0, 0
plaka_w, plaka_h = 2100, 2800
for i, row in df.iterrows():
    w, h = row["Genişlik"], row["Yükseklik"]
    if x + w > plaka_w:
        x = 0
        y += max_y + 10
        max_y = 0
    if y + h > plaka_h:
        continue
    rect = plt.Rectangle((x, y), w, h, edgecolor='black', facecolor='lightgray')
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, row["Parça"], ha='center', va='center', fontsize=6)
    x += w + 10
    if h > max_y:
        max_y = h

ax.set_xlim(0, plaka_w)
ax.set_ylim(0, plaka_h)
plt.gca().invert_yaxis()
st.pyplot(fig2d)

st.success("✅ Tüm çıktılar hazır: 3D model, DXF, CSV ve nesting görselleştirmesi")

# 🔄 Nesting DXF Çıktısı
if not os.path.exists("nesting"):
    os.makedirs("nesting")

nesting_dxf = ezdxf.new()
nesting_msp = nesting_dxf.modelspace()
x, y, max_y = 0, 0, 0

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
