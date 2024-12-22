import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Tema untuk visualisasi
sns.set_palette("pink")

# Judul Aplikasi
st.title("📊 **Dashboard Analisis E-Commerce**")
st.markdown("💻 **Dashboard ini dibuat berdasarkan notebook analisis e-commerce.**")

# Dataset
@st.cache
def load_data():
    # Dataset dari GitHub
    url = "https://raw.githubusercontent.com/lizaathalya/Dicoding/main/DASHBOARD/df.csv"
    df = pd.read_csv(url)
    
    # Konversi kolom waktu ke format datetime
    datetime_cols = [
        "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date",
        "order_purchase_timestamp", "shipping_limit_date"
    ]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])
    
    return df

# Memuat data
all_df = load_data()

# Sidebar untuk filter rentang tanggal
min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()
st.sidebar.title("📅 Filter Rentang Tanggal")
start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

# Dataset yang difilter
filtered_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & (all_df["order_approved_at"] <= str(end_date))]

# --------------------- Pertanyaan 1 ---------------------
st.subheader("📍 **Negara bagian pelanggan mana yang menyumbang pendapatan terbesar?**")

# Mengelompokkan berdasarkan negara bagian pelanggan
state_revenue = filtered_df.groupby('customer_state').agg({
    'order_id': 'nunique',  # Jumlah pesanan unik
    'payment_value': 'sum'  # Total nilai pembayaran
}).reset_index().sort_values(by='payment_value', ascending=False)

# Statistik utama
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Negara Bagian Tertinggi", value=state_revenue.iloc[0]["customer_state"])
with col2:
    st.metric(label="Pendapatan Tertinggi", value=f"${state_revenue.iloc[0]['payment_value']:,.2f}")

# Visualisasi
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=state_revenue,
    x="customer_state",
    y="payment_value",
    palette="pink"
)
ax1.set_title("Pendapatan Total per Negara Bagian", fontsize=16)
ax1.set_xlabel("Negara Bagian", fontsize=12)
ax1.set_ylabel("Pendapatan Total", fontsize=12)
plt.xticks(rotation=45)

st.pyplot(fig1)

# --------------------- Pertanyaan 2 ---------------------
st.subheader("📦 **Apakah kategori produk memengaruhi jumlah pesanan dan skor ulasan?**")

# Mengelompokkan berdasarkan kategori produk
category_analysis = filtered_df.groupby('product_category_name_english').agg({
    'order_id': 'nunique',  # Jumlah pesanan unik
    'review_score': ['mean', 'min', 'max']  # Skor ulasan rata-rata, minimum, dan maksimum
}).reset_index()

# Menyesuaikan kolom
category_analysis.columns = ['product_category_name_english', 'order_count', 'avg_review_score', 'min_review_score', 'max_review_score']
category_analysis = category_analysis.sort_values(by='order_count', ascending=False).head(10)

# Statistik utama
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Kategori Terlaris", value=category_analysis.iloc[0]["product_category_name_english"])
with col2:
    st.metric(label="Jumlah Pesanan Tertinggi", value=category_analysis.iloc[0]["order_count"])

# Visualisasi Jumlah Pesanan dan Skor Ulasan
fig2, ax2 = plt.subplots(figsize=(14, 8))
sns.barplot(
    data=category_analysis,
    x="order_count",
    y="product_category_name_english",
    palette="pink"
)
ax2.set_title("Top 10 Kategori Produk berdasarkan Jumlah Pesanan", fontsize=16)
ax2.set_xlabel("Jumlah Pesanan", fontsize=12)
ax2.set_ylabel("Kategori Produk", fontsize=12)

# Tambahkan skor ulasan rata-rata sebagai overlay
for index, row in category_analysis.iterrows():
    ax2.text(row['order_count'] + 2, index, f"Avg: {row['avg_review_score']:.1f}", 
             fontsize=10, color='black')

st.pyplot(fig2)

# --------------------- Pertanyaan 3 ---------------------
st.subheader("⭐ **Bagaimana distribusi skor ulasan secara keseluruhan?**")

# Visualisasi Distribusi Skor Ulasan
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.histplot(filtered_df['review_score'], bins=10, kde=True, color="pink", ax=ax3)
ax3.set_title("Distribusi Skor Ulasan", fontsize=16)
ax3.set_xlabel("Skor Ulasan", fontsize=12)
ax3.set_ylabel("Frekuensi", fontsize=12)

st.pyplot(fig3)

# --------------------- Footer ---------------------
st.caption("💖 Dibuat untuk memastikan konsistensi antara notebook dan dashboard.")
