import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Verilerin örnek olarak hazırlanması
projects = [
    {"ID": 1, "Proje Adı": "Dolap 1", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-01", "Bitiş Tarihi": "2025-04-10", "Panel Sayısı": 12, "Kapak Sayısı": 4, "Toplam Maliyet": 5000, "İlerleme": 60},
    {"ID": 2, "Proje Adı": "Dolap 2", "Durum": "Tamamlandı", "Başlangıç Tarihi": "2025-03-01", "Bitiş Tarihi": "2025-03-15", "Panel Sayısı": 8, "Kapak Sayısı": 2, "Toplam Maliyet": 3000, "İlerleme": 100},
    {"ID": 3, "Proje Adı": "Dolap 3", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-05", "Bitiş Tarihi": "2025-04-12", "Panel Sayısı": 15, "Kapak Sayısı": 5, "Toplam Maliyet": 7000, "İlerleme": 80},
]

# 3D Görselleştirme (örnekleme, burada basit bir görselleştirme olacak)
def plot_3d_design():
    st.subheader("3D Dolap Tasarımı")
    st.write("3D görselleştirme burada olacak. [Burada bir görsel eklenebilir.]")

# Zaman Çizelgesi - Gantt Şeması
def plot_project_timeline(projects):
    df = pd.DataFrame(projects, columns=["ID", "Proje Adı", "Durum", "Başlangıç Tarihi", "Bitiş Tarihi"])
    plt.figure(figsize=(10, 6))
    df['Başlangıç Tarihi'] = pd.to_datetime(df['Başlangıç Tarihi'])
    df['Bitiş Tarihi'] = pd.to_datetime(df['Bitiş Tarihi'])
    
    for i, row in df.iterrows():
        plt.barh(row['Proje Adı'], (row['Bitiş Tarihi'] - row['Başlangıç Tarihi']).days, left=row['Başlangıç Tarihi'])
    
    plt.title("Projelerin Zaman Çizelgesi")
    plt.xlabel("Tarih")
    plt.ylabel("Proje Adı")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    st.pyplot()

# İlerleme Çubukları
def plot_progress_bar(projects):
    df = pd.DataFrame(projects, columns=["ID", "Proje Adı", "Durum", "Başlangıç Tarihi", "Bitiş Tarihi", "İlerleme"])
    for i, row in df.iterrows():
        st.write(f"{row['Proje Adı']} - {row['Durum']}")
        st.progress(row['İlerleme'] / 100)

# Proje Detayları
def project_details(project_id, projects):
    project = next((item for item in projects if item["ID"] == project_id), None)
    if project:
        st.subheader(f"Proje Detayları - {project['Proje Adı']}")
        st.write(f"Proje Adı: {project['Proje Adı']}")
        st.write(f"Durum: {project['Durum']}")
        st.write(f"Başlangıç Tarihi: {project['Başlangıç Tarihi']}")
        st.write(f"Bitiş Tarihi: {project['Bitiş Tarihi']}")
        st.write(f"Panel Sayısı: {project['Panel Sayısı']}")
        st.write(f"Kapak Sayısı: {project['Kapak Sayısı']}")
        st.write(f"Toplam Maliyet: {project['Toplam Maliyet']} ₺")
    else:
        st.error("Proje bulunamadı.")

# Özelleştirilmiş Raporlar
def custom_report(projects, panel_threshold, cost_threshold):
    filtered_projects = [p for p in projects if p['Panel Sayısı'] >= panel_threshold and p['Toplam Maliyet'] >= cost_threshold]
    if filtered_projects:
        st.subheader("Özelleştirilmiş Rapor - Panel ve Maliyet Filtreleme")
        df = pd.DataFrame(filtered_projects, columns=["Proje Adı", "Durum", "Başlangıç Tarihi", "Bitiş Tarihi", "Panel Sayısı", "Kapak Sayısı", "Toplam Maliyet"])
        st.write(df)
    else:
        st.warning("Filtrene göre proje bulunamadı.")

# Performans İzleme (Kapanış Raporu)
def performance_tracking(projects):
    completed_projects = [p for p in projects if p['Durum'] == 'Tamamlandı']
    if completed_projects:
        st.subheader("Tamamlanan Projeler - Kapanış Raporu")
        completed_project_data = []
        for project in completed_projects:
            start_date = datetime.strptime(project['Başlangıç Tarihi'], "%Y-%m-%d")
            end_date = datetime.strptime(project['Bitiş Tarihi'], "%Y-%m-%d")
            project_duration = (end_date - start_date).days
            completed_project_data.append({
                'Proje Adı': project['Proje Adı'],
                'Başlangıç Tarihi': project['Başlangıç Tarihi'],
                'Bitiş Tarihi': project['Bitiş Tarihi'],
                'Proje Süresi (gün)': project_duration,
                'Toplam Maliyet': project['Toplam Maliyet']
            })
        df = pd.DataFrame(completed_project_data)
        st.write(df)
    else:
        st.warning("Henüz tamamlanmış proje yok.")

# Kullanıcı Yönetimi ve Giriş Yapma
def user_management():
    st.sidebar.title("Kullanıcı Girişi")
    user_name = st.sidebar.text_input("Kullanıcı Adı")
    password = st.sidebar.text_input("Parola", type='password')
    
    if user_name and password:
        # Gerçek giriş sistemleri için burada doğrulama yapılır
        st.sidebar.success(f"Hoşgeldiniz, {user_name}")
    else:
        st.sidebar.warning("Giriş yapmak için kullanıcı adı ve parola girin.")

# Ana Uygulama UI
st.set_page_config(page_title="📋 Dolap Üretim Programı", layout="wide")
st.title("📋 Dolap Üretim Programı")

# Kullanıcı Girişi
user_management()

# 3D Tasarım Görselleştirme
plot_3d_design()

# Proje Zaman Çizelgesi
st.subheader("Projelerin Zaman Çizelgesi")
plot_project_timeline(projects)

# Proje İlerleme
st.subheader("Projelerin İlerleme Durumu")
plot_progress_bar(projects)

# Proje Detayları
project_id = st.number_input("Proje ID'si girin", min_value=1, step=1)
if project_id:
    project_details(project_id, projects)

# Özelleştirilmiş Raporlar
st.subheader("Özelleştirilmiş Rapor - Panel ve Maliyet Filtreleme")
panel_threshold = st.slider("Minimum Panel Sayısı", min_value=0, max_value=100, value=10, step=1)
cost_threshold = st.slider("Minimum Toplam Maliyet (₺)", min_value=0, max_value=100000, value=5000, step=500)
if st.button("Raporu Göster"):
    custom_report(projects, panel_threshold, cost_threshold)

# Performans İzleme
if projects:
    performance_tracking(projects)
