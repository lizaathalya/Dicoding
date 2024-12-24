import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Tema untuk visualisasi
sns.set_palette("pastel")

# Judul Aplikasi
st.title("📊 **Dashboard Analisis E-Commerce**")
st.markdown("**Dashboard ini menampilkan analisis dari data e-commerce untuk menjawab pertanyaan bisnis utama.**")

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
st.sidebar.title("🗓 **Filter Data**")
st.sidebar.markdown("Gunakan filter untuk mempersempit analisis sesuai kebutuhan Anda.")

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Filter rentang tanggal
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date
)

# Info tambahan di sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**📊 Data Summary**\n\n- Total Orders: `{}`\n- Total Payment: `{:.2f}`".format(
        len(all_df), all_df["payment_value"].sum()
    )
)

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
    'review_score': ['mean', 'std']  # Skor ulasan rata-rata dan standar deviasi
}).reset_index()

# Menyesuaikan kolom
category_analysis.columns = ['product_category_name_english', 'order_count', 'average_review_score', 'std_review_score']

# Mengurutkan berdasarkan jumlah pesanan dan memilih Top 10
category_analysis = category_analysis.sort_values(by='order_count', ascending=False).head(10)

# Statistik utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Kategori Terlaris", value=category_analysis.iloc[0]["product_category_name_english"])
with col2:
    st.metric(label="Jumlah Pesanan Tertinggi", value=category_analysis.iloc[0]["order_count"])
with col3:
    st.metric(label="Rata-rata Skor Ulasan", value=f"{category_analysis.iloc[0]['average_review_score']:.2f}")

# Visualisasi: Jumlah pesanan dan skor ulasan rata-rata dengan standar deviasi
fig2, ax = plt.subplots(1, 2, figsize=(18, 8))

# Bar chart untuk jumlah pesanan
ax[0].barh(category_analysis['product_category_name_english'], category_analysis['order_count'], color='lightgreen')
ax[0].set_xlabel("Order Count", fontsize=12)
ax[0].set_ylabel("Product Category", fontsize=12)
ax[0].set_title("Top 10 Product Categories by Order Count", fontsize=16)
ax[0].invert_yaxis()  # Membalikkan sumbu Y agar kategori terpopuler berada di atas

# Bar chart untuk skor ulasan rata-rata dengan standar deviasi
ax[1].barh(category_analysis['product_category_name_english'], category_analysis['average_review_score'], 
           color='lightblue', alpha=0.7, label='Average Review Score')
ax[1].errorbar(category_analysis['average_review_score'], category_analysis['product_category_name_english'],
               xerr=category_analysis['std_review_score'], fmt='o', color='red', label='Std. Dev. of Review Score')
ax[1].set_xlabel("Review Score", fontsize=12)
ax[1].set_title("Top 10 Product Categories by Review Score", fontsize=16)
ax[1].legend()

# Menyesuaikan layout secara manual
plt.tight_layout()

st.pyplot(fig2)

# --------------------- Kesimpulan dan Rekomendasi ---------------------
st.markdown("---")
st.header("📚 **Kesimpulan dan Rekomendasi**")

st.markdown(
    """
    ### 1. **Negara Bagian Pelanggan dan Distribusi Pesanan**
    - **SP (São Paulo)** menyumbang pendapatan terbesar dengan jumlah pesanan yang signifikan, menjadikannya pasar yang strategis.
    - Terdapat hubungan positif antara jumlah pesanan dan total pendapatan di semua negara bagian.
    - **Mengapa ini penting?**  
      SP menunjukkan potensi besar untuk peningkatan penjualan, sementara RJ dan MG juga memiliki peluang untuk dikembangkan lebih lanjut.
    - **Rekomendasi:**  
      - Fokuskan kampanye pemasaran di SP untuk menarik lebih banyak pelanggan.  
      - Tingkatkan layanan logistik dan pengalaman pelanggan di SP.  
      - Identifikasi peluang pasar di RJ dan MG untuk meningkatkan kontribusi mereka.

    ### 2. **Pengaruh Kategori Produk pada Pesanan dan Skor Ulasan**
    - Kategori **"bed_bath_table"** dan **"health_beauty"** memiliki jumlah pesanan tertinggi, menunjukkan popularitas tinggi di kalangan pelanggan.
    - Kategori populer memiliki skor ulasan yang lebih stabil dibanding kategori lain yang memiliki variasi lebih besar.
    - **Mengapa ini penting?**  
      Kategori populer adalah aset strategis, sementara variasi skor di kategori lain mengindikasikan potensi masalah layanan atau kualitas.
    - **Rekomendasi:**  
      - Pertahankan kualitas di kategori populer untuk menjaga stabilitas ulasan.  
      - Lakukan survei pelanggan pada kategori dengan variasi skor ulasan besar untuk mengidentifikasi masalah dan memperbaikinya.  
      - Gunakan data ulasan untuk menciptakan produk yang lebih sesuai dengan preferensi pelanggan.
    """
)
