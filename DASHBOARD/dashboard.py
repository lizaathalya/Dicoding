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
@st.cache_data
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
st.subheader("📍 **Negara Bagian Pelanggan dan Distribusi Pesanan**")

# Mengelompokkan berdasarkan negara bagian pelanggan
state_revenue = filtered_df.groupby('customer_state').agg({
    'order_id': 'nunique',  # Jumlah pesanan unik
    'payment_value': 'sum'  # Total nilai pembayaran
}).reset_index()

# Mengurutkan berdasarkan total pembayaran
state_revenue = state_revenue.sort_values(by='payment_value', ascending=False)

# Visualisasi data
fig1, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(state_revenue['customer_state'], state_revenue['payment_value'], color='skyblue', label='Total Payment')
ax1.set_xlabel('Customer State', fontsize=12)
ax1.set_ylabel('Total Payment Value', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.set_title('Total Payment and Order Count by Customer State', fontsize=16)

# Overlay jumlah pesanan
ax2 = ax1.twinx()
ax2.plot(state_revenue['customer_state'], state_revenue['order_id'], color='orange', marker='o', label='Order Count')
ax2.set_ylabel('Order Count', fontsize=12)

# Tambahkan legenda
fig1.legend(loc="upper right", bbox_to_anchor=(0.85, 0.9), fontsize=10)
plt.tight_layout()

st.pyplot(fig1)

# --------------------- Pertanyaan 2 ---------------------
st.subheader("📦 **Apakah kategori produk memengaruhi jumlah pesanan dan skor ulasan?**")

# Mengelompokkan berdasarkan kategori produk
category_analysis = filtered_df.groupby('product_category_name_english').agg({
    'order_id': 'nunique',  # Jumlah pesanan unik
    'review_score': 'mean'  # Rata-rata skor ulasan
}).reset_index()

# Menyesuaikan kolom
category_analysis.columns = ['product_category_name_english', 'order_count', 'average_review_score']

# Mengurutkan berdasarkan jumlah pesanan dan memilih Top 10
category_analysis = category_analysis.sort_values(by='order_count', ascending=False).head(10)

# Statistik utama
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Kategori Terlaris", value=category_analysis.iloc[0]["product_category_name_english"])
with col2:
    st.metric(label="Jumlah Pesanan Tertinggi", value=category_analysis.iloc[0]["order_count"])

# Visualisasi data
fig2, ax = plt.subplots(figsize=(14, 8))

# Bar chart untuk jumlah pesanan
sns.barplot(
    data=category_analysis,
    x="order_count",
    y="product_category_name_english",
    palette="lightgreen",
    ax=ax
)
ax.set_title('Top 10 Product Categories by Order Count', fontsize=16)
ax.set_xlabel('Order Count', fontsize=12)
ax.set_ylabel('Product Category', fontsize=12)

st.pyplot(fig2)

# Rata-rata skor ulasan
st.write("📋 **Rata-rata Skor Ulasan (Review Score) untuk Top 10 Kategori Produk:**")
st.table(category_analysis[['product_category_name_english', 'average_review_score']].set_index('product_category_name_english'))
