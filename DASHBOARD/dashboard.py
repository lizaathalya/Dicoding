import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_palette("pink")
plt.style.use("seaborn-darkgrid")

# Dataset
all_df = pd.read_csv("https://raw.githubusercontent.com/lizaathalya/Dicoding/main/dashboard/df.csv")

# Filter datetime columns
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

# Filter date range for analysis
min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

st.sidebar.title("📅 Filter")
start_date, end_date = st.sidebar.date_input(
    label="Pilih Rentang Tanggal",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Main filtered dataset
filtered_df = all_df[(all_df["order_approved_at"] >= str(start_date)) &
                     (all_df["order_approved_at"] <= str(end_date))]

# Streamlit App Title
st.title("📊 **Dashboard Analisis E-Commerce**")
st.markdown("💖 **Dashboard untuk menjawab submission BANGKIT 2024**")

# --------------------- Pertanyaan 1 ---------------------
st.subheader("📍 **Pertanyaan 1: Negara bagian pelanggan mana yang menyumbang pendapatan terbesar?**")

# Data untuk analisis negara bagian
state_revenue = filtered_df.groupby("customer_state").agg({
    "order_id": "nunique",  # Jumlah pesanan unik
    "payment_value": "sum"  # Total pembayaran
}).reset_index().sort_values(by="payment_value", ascending=False)

# Statistik utama
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Negara Bagian Tertinggi", value=state_revenue.iloc[0]["customer_state"])
with col2:
    st.metric(label="Pendapatan Tertinggi", value=f"${state_revenue.iloc[0]['payment_value']:,.2f}")

# Grafik negara bagian
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=state_revenue,
    x="customer_state",
    y="payment_value",
    palette="pink"
)
ax1.set_title("Pendapatan Total per Negara Bagian", fontsize=16, color="darkred")
ax1.set_xlabel("Negara Bagian", fontsize=12)
ax1.set_ylabel("Pendapatan Total", fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig1)

# --------------------- Pertanyaan 2 ---------------------
st.subheader("📦 **Pertanyaan 2: Apakah kategori produk memengaruhi jumlah pesanan dan skor ulasan?**")

# Data untuk analisis kategori produk
category_analysis = filtered_df.groupby("product_category_name_english").agg({
    "order_id": "nunique",  # Jumlah pesanan unik
    "review_score": ["min", "max"]  # Skor ulasan minimum dan maksimum
}).reset_index()

# Kolom kategori
category_analysis.columns = ["product_category_name_english", "order_count", "min_review_score", "max_review_score"]
category_analysis = category_analysis.sort_values(by="order_count", ascending=False)

# Statistik utama
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Kategori Terlaris", value=category_analysis.iloc[0]["product_category_name_english"])
with col2:
    st.metric(label="Jumlah Pesanan Tertinggi", value=category_analysis.iloc[0]["order_count"])

# Grafik kategori produk
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.barplot(
    data=category_analysis.head(10),
    x="order_count",
    y="product_category_name_english",
    palette="pink"
)
ax2.set_title("Jumlah Pesanan per Kategori Produk", fontsize=16, color="darkred")
ax2.set_xlabel("Jumlah Pesanan", fontsize=12)
ax2.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig2)

# Footer
st.caption("💖 Dibuat dengan cinta untuk analisis yang mendalam dan estetis.")
