import streamlit as st
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(page_title="Üretim Paneli", layout="wide")

st.title("🛠️ Üretim Takip Paneli")

# Örnek sipariş verileri
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame([
        {"ID": 1, "Ürün": "Mutfak Dolabı", "Durum": "Beklemede"},
        {"ID": 2, "Ürün": "TV Ünitesi", "Durum": "Üretimde"},
    ])

statuses = ["Beklemede", "Üretimde", "Tamamlandı", "Teslim Edildi"]

# Sipariş Ekleme
with st.expander("➕ Yeni Sipariş Ekle"):
    with st.form("siparis_form"):
        urun = st.text_input("Ürün Adı")
        durum = st.selectbox("Durum", statuses)
        submitted = st.form_submit_button("Ekle")
        if submitted and urun:
            new_id = st.session_state.orders["ID"].max() + 1 if not st.session_state.orders.empty else 1
            new_row = {"ID": new_id, "Ürün": urun, "Durum": durum}
            st.session_state.orders.loc[len(st.session_state.orders)] = new_row
            st.success("Sipariş eklendi!")

# Duruma göre siparişleri göster
tabs = st.tabs(statuses)
for i, durum in enumerate(statuses):
    with tabs[i]:
        df = st.session_state.orders[st.session_state.orders["Durum"] == durum]
        st.subheader(f"{durum} Siparişler")
        st.dataframe(df, use_container_width=True)

# Durum Güncelleme
st.subheader("🔄 Sipariş Durumu Güncelle")
selected_id = st.number_input("Sipariş ID", min_value=1, step=1)
new_status = st.selectbox("Yeni Durum", statuses, key="update")
if st.button("Güncelle"):
    idx = st.session_state.orders[st.session_state.orders["ID"] == selected_id].index
    if not idx.empty:
        st.session_state.orders.at[idx[0], "Durum"] = new_status
        st.success("Durum güncellendi.")
    else:
        st.error("Bu ID'ye sahip sipariş bulunamadı.")
