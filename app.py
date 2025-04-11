import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dolap Sihirbazı 3D", layout="centered")
st.title("🧱 Dolap Toplama ve Bağlantı Önizleme")

st.subheader("📦 Malzeme Girişi ve Ayarlar")
malzeme_adet = st.number_input("Panel Adedi", min_value=1, max_value=20, value=6)
malzeme_genislik = st.number_input("Panel Genişliği (X)", value=600)
malzeme_yukseklik = st.number_input("Panel Yüksekliği (Y)", value=720)
malzeme_derinlik = st.number_input("Panel Derinliği (Z)", value=500)
kalinlik = st.number_input("Panel Kalınlığı (mm)", value=18)

st.subheader("🔩 Donatı Seçenekleri")
menteşe_adedi = st.number_input("Menteşe Sayısı", min_value=0, max_value=5, value=2)
cabineo_yon = st.selectbox("Cabineo Delik Yönü", ["Üst", "Alt", "Sağ", "Sol", "Hepsi"])

fig = go.Figure()
renkler = ["red", "green", "blue", "orange", "purple", "gray"]

# Her panel için kutu oluştur
for i in range(malzeme_adet):
    x0, y0, z0 = 0, 0, i * (malzeme_derinlik + 30)
    w, h, d = kalinlik, malzeme_yukseklik, malzeme_derinlik
    x = [x0, x0+w, x0+w, x0, x0, x0+w, x0+w, x0]
    y = [y0, y0, y0+h, y0+h, y0, y0, y0+h, y0+h]
    z = [z0, z0, z0, z0, z0+d, z0+d, z0+d, z0+d]
    fig.add_trace(go.Mesh3d(
        x=x, y=y, z=z,
        color=renkler[i % len(renkler)],
        opacity=0.5,
        name=f"Panel {i+1}"
    ))

# Silindir fonksiyonu (delik olarak çizim)
def silindir_olustur(cx, cy, cz, r, h, eksen='x', segment=12):
    theta = np.linspace(0, 2*np.pi, segment)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    verts = []
    for i in range(segment):
        if eksen == 'x':
            verts.append((cx - h/2, cy + x[i], cz + y[i]))
            verts.append((cx + h/2, cy + x[i], cz + y[i]))
        elif eksen == 'y':
            verts.append((cx + x[i], cy - h/2, cz + y[i]))
            verts.append((cx + x[i], cy + h/2, cz + y[i]))
        else:
            verts.append((cx + x[i], cy + y[i], cz - h/2))
            verts.append((cx + x[i], cy + y[i], cz + h/2))
    triangles = []
    for i in range(0, len(verts)-2, 2):
        triangles.append((i, i+1, i+3))
        triangles.append((i, i+2, i+3))
    x, y, z = zip(*verts)
    i, j, k = zip(*triangles)
    return x, y, z, i, j, k

# Menteşe delikleri
menteşe_delikler = []
if menteşe_adedi > 0:
    aralik = malzeme_yukseklik / (menteşe_adedi + 1)
    for i in range(menteşe_adedi):
        menteşe_delikler.append((kalinlik / 2, (i+1)*aralik, malzeme_derinlik + kalinlik / 2))

for x, y, z in menteşe_delikler:
    sx, sy, sz, si, sj, sk = silindir_olustur(x, y, z, 17.5, kalinlik, 'z')
    fig.add_trace(go.Mesh3d(x=sx, y=sy, z=sz, i=si, j=sj, k=sk, color='blue', opacity=0.9, name='Menteşe'))

# Cabineo delikleri (örnek: üst ve alt)
cabineo_delikler = []
if cabineo_yon in ["Üst", "Hepsi"]:
    cabineo_delikler.append((kalinlik/2, kalinlik/2, malzeme_derinlik/2))
if cabineo_yon in ["Alt", "Hepsi"]:
    cabineo_delikler.append((kalinlik/2, malzeme_yukseklik - kalinlik/2, malzeme_derinlik/2))
if cabineo_yon in ["Sol", "Hepsi"]:
    cabineo_delikler.append((kalinlik/2, malzeme_yukseklik/2, kalinlik/2))
if cabineo_yon in ["Sağ", "Hepsi"]:
    cabineo_delikler.append((kalinlik/2, malzeme_yukseklik/2, malzeme_derinlik - kalinlik/2))

for x, y, z in cabineo_delikler:
    sx, sy, sz, si, sj, sk = silindir_olustur(x, y, z, 6, kalinlik, 'x')
    fig.add_trace(go.Mesh3d(x=sx, y=sy, z=sz, i=si, j=sj, k=sk, color='black', opacity=1.0, name='Cabineo'))

fig.update_layout(scene=dict(
    xaxis_title='X (Genişlik)',
    yaxis_title='Y (Yükseklik)',
    zaxis_title='Z (Derinlik)'
), margin=dict(l=0, r=0, b=0, t=0))

st.subheader("🧱 3D Katı Model ve Bağlantı Önizleme")
st.plotly_chart(fig, use_container_width=True)

# 2D Nesting Yerleşimi
st.subheader("🧩 2D Nesting Yerleşim Görünümü")
fig2d, ax = plt.subplots(figsize=(6, 8))
plaka_gen = 2100
plaka_yuk = 2800
x, y = 0, 0
max_y = 0
paneller = []

for i in range(malzeme_adet):
    w = malzeme_genislik
    h = malzeme_yukseklik
    if x + w > plaka_gen:
        x = 0
        y += max_y + 10
        max_y = 0
    if y + h > plaka_yuk:
        st.warning(f"Panel {i+1} plakaya sığmadı, atlandı.")
        continue
    rect = plt.Rectangle((x, y), w, h, edgecolor='black', facecolor='lightgray')
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, f"Panel {i+1}", ha='center', va='center')
    paneller.append({"Panel": f"Panel {i+1}", "Genişlik": w, "Yükseklik": h})
    x += w + 10
    if h > max_y:
        max_y = h

ax.set_xlim(0, plaka_gen)
ax.set_ylim(0, plaka_yuk)
ax.set_title("Plaka Üzerine Yerleşim")
ax.set_xlabel("Genişlik (mm)")
ax.set_ylabel("Yükseklik (mm)")
plt.gca().invert_yaxis()
st.pyplot(fig2d)

# Kesim listesi göster
st.subheader("📋 Kesim Listesi")
df = pd.DataFrame(paneller)
st.dataframe(df)

st.success("✅ 3D görünüm, bağlantılar ve nesting başarıyla oluşturuldu!")
