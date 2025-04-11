import streamlit as st
import pandas as pd
from datetime import datetime

# Proje Verisi - Örnek olarak veri eklenmiştir
projects = [
    {"ID": 1, "Proje Adı": "Dolap 1", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-01", "Bitiş Tarihi": "2025-04-10", "Panel Sayısı": 12, "Kapak Sayısı": 4, "Toplam Maliyet": 5000, "İlerleme": 60},
    {"ID": 2, "Proje Adı": "Dolap 2", "Durum": "Tamamlandı", "Başlangıç Tarihi": "2025-03-01", "Bitiş Tarihi": "2025-03-15", "Panel Sayısı": 8, "Kapak Sayısı": 2, "Toplam Maliyet": 3000, "İlerleme": 100},
    {"ID": 3, "Proje Adı": "Dolap 3", "Durum": "Devam Ediyor", "Başlangıç Tarihi": "2025-04-05", "Bitiş Tarihi": "2025-04-12", "Panel Sayısı": 15, "Kapak Sayısı": 5, "Toplam Maliyet": 7000, "İlerleme": 80},
]

# Kullanıcı Rol Yönetimi
def user_role_management():
    st.sidebar.title("Kullanıcı ve Rol Yönetimi")
    role = st.sidebar.selectbox("Kullanıcı Rolü", ["Yönetici", "Proje Yöneticisi", "Kullanıcı"])
    if role == "Yönetici":
        st.sidebar.subheader("Yönetici Paneli")
        st.sidebar.text("Yönetici olarak projeleri düzenleyebilir ve raporları görüntüleyebilirsiniz.")
    elif role == "Proje Yöneticisi":
        st.sidebar.subheader("Proje Yöneticisi Paneli")
        st.sidebar.text("Proje yöneticisi olarak projelere dair ilerleme güncellemeleri yapabilirsiniz.")
    else:
        st.sidebar.subheader("Kullanıcı Paneli")
        st.sidebar.text("Kullanıcı olarak yalnızca mevcut projeleri görüntüleyebilirsiniz.")

# Proje Güncelleme
def update_project(project_id, projects):
    project = next((item for item in projects if item["ID"] == project_id), None)
    if project:
        st.subheader(f"Proje {project_id} Güncelle")
        new_name = st.text_input("Proje Adı", value=project["Proje Adı"])
        new_status = st.selectbox("Proje Durumu", ["Devam Ediyor", "Tamamlandı", "Beklemede"], index=["Devam Ediyor", "Tamamlandı", "Beklemede"].index(project["Durum"]))
        new_start_date = st.date_input("Başlangıç Tarihi", value=datetime.strptime(project["Başlangıç Tarihi"], "%Y-%m-%d"))
        new_end_date = st.date_input("Bitiş Tarihi", value=datetime.strptime(project["Bitiş Tarihi"], "%Y-%m-%d"))
        
        if st.button(f"Proje {project_id} Güncelle"):
            project["Proje Adı"] = new_name
            project["Durum"] = new_status
            project["Başlangıç Tarihi"] = new_start_date.strftime("%Y-%m-%d")
            project["Bitiş Tarihi"] = new_end_date.strftime("%Y-%m-%d")
            st.success(f"Proje {project_id} başarıyla güncellendi.")
        return project
    else:
        st.error(f"Proje ID {project_id} bulunamadı.")
        return None

# Proje İlerleme Güncelleme
def update_progress(project_id, projects):
    project = next((item for item in projects if item["ID"] == project_id), None)
    if project:
        new_progress = st.slider("İlerleme (%)", min_value=0, max_value=100, value=project["İlerleme"], step=1)
        if st.button(f"Proje {project_id} İlerleme Güncelle"):
            project["İlerleme"] = new_progress
            st.success(f"Proje {project_id} ilerlemesi başarıyla güncellendi.")
        return project
    else:
        st.error(f"Proje ID {project_id} bulunamadı.")
        return None

# Tüm Projeleri Görüntüleme
def view_all_projects(projects):
    st.subheader("Tüm Projeleri Görüntüle")
    df = pd.DataFrame(projects)
    st.write(df)

# Proje Arşivleme
def archive_project(project_id, projects):
    project = next((item for item in projects if item["ID"] == project_id), None)
    if project:
        project["Durum"] = "Arşivlendi"
        st.success(f"Proje {project_id} başarıyla arşivlendi.")
    else:
        st.error(f"Proje ID {project_id} bulunamadı.")

# 3D Görselleştirme ve Üretim Adımları
def manufacturing_steps():
    st.subheader("Üretim Adımları ve 3D Görselleştirme")
    st.write("Burada üretim adımları görselleştirilecektir.")
    st.write("Örnek olarak: Panel montajı, aksesuar yerleştirme ve montaj sonrası testler gibi.")
    st.write("3D görselleştirmeler burada yer tutucu olarak eklenmiştir.")
    
# Ana Ekran ve Menü
def main_ui(projects):
    st.title("📋 Dolap Üretim Programı")
    
    # Kullanıcı ve Rol Yönetimi
    user_role_management()

    # Projeleri Görüntüleme
    if st.button("Tüm Projeleri Görüntüle"):
        view_all_projects(projects)

    # Proje Güncelleme ve Arşivleme
    project_id_to_update = st.number_input("Güncellemek veya Arşivlemek için Proje ID girin", min_value=1)
    if project_id_to_update:
        updated_project = update_project(project_id_to_update, projects)
        updated_project = update_progress(project_id_to_update, projects)
    
        if st.button(f"Proje {project_id_to_update} Arşivle"):
            archive_project(project_id_to_update, projects)
    
        # Güncellenmiş projeyi görüntüleyelim
        if updated_project:
            st.write(f"Güncellenmiş Proje: {updated_project}")

    # Üretim Adımları
    manufacturing_steps()

# Ana program çalıştırma
if __name__ == "__main__":
    main_ui(projects)
