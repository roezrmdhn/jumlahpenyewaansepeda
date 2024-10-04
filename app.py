import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Penyewaan Sepeda")


# Membaca Data
@st.cache
def load_data():
    df = pd.read_csv("day.csv")
    return df


df = load_data()

# Menampilkan Data
st.subheader("Data Penyewaan Sepeda")
st.write(df.head())

# Menampilkan ringkasan statistik
st.subheader("Statistik Deskriptif")
st.write(df[["temp", "hum", "windspeed"]].describe())

# Cek rentang nilai untuk setiap kolom
temp_min, temp_max = df["temp"].min(), df["temp"].max()
hum_min, hum_max = df["hum"].min(), df["hum"].max()
windspeed_min, windspeed_max = df["windspeed"].min(), df["windspeed"].max()

# Print rentang nilai untuk debugging
st.write(f"Range Temperature: {temp_min} - {temp_max}")
st.write(f"Range Humidity: {hum_min} - {hum_max}")
st.write(f"Range Windspeed: {windspeed_min} - {windspeed_max}")

# Binning
# Definisikan bins dan labels
temp_bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
temp_labels = ["Very Low", "Low", "Medium", "High", "Very High"]

hum_bins = [0, 0.3, 0.6, 0.9, 1]
hum_labels = ["Very Low", "Low", "High", "Very High"]

windspeed_bins = [0, 5, 10, 15, 20]
windspeed_labels = ["Very Low", "Low", "Medium", "High"]

# Cek panjang bins dan labels
if len(temp_bins) - 1 == len(temp_labels):
    df["temp_binned"] = pd.cut(
        df["temp"], bins=temp_bins, labels=temp_labels, include_lowest=True
    )

if len(hum_bins) - 1 == len(hum_labels):
    df["hum_binned"] = pd.cut(
        df["hum"], bins=hum_bins, labels=hum_labels, include_lowest=True
    )

if len(windspeed_bins) - 1 == len(windspeed_labels):
    df["windspeed_binned"] = pd.cut(
        df["windspeed"],
        bins=windspeed_bins,
        labels=windspeed_labels,
        include_lowest=True,
    )

# Menghapus baris NaN setelah binning
df.dropna(subset=["temp_binned", "hum_binned", "windspeed_binned"], inplace=True)

# Analisis Cuaca
st.subheader("Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
weather_count = df.groupby("weathersit")["cnt"].agg(["mean", "median", "count"])
st.bar_chart(weather_count["mean"])

# Insight
st.subheader("Insight")
st.write("1. Cuaca Cerah Meningkatkan Jumlah Rental Sepeda.")
st.write("2. Hujan Berat Mengurangi Jumlah Rental Sepeda.")

# Menyajikan Analisis Musiman
st.subheader("Analisis Musiman")
season_count = df.groupby("season")["cnt"].agg(["mean", "median"])
st.line_chart(season_count["mean"])

# Analisis Clustering berdasarkan Binning
st.subheader("Analisis Clustering berdasarkan Binned Data")
grouped_data = df.groupby(["temp_binned", "hum_binned"])["cnt"].mean().reset_index()

# Tampilkan hasil pengelompokan
st.write("Grouped Data:", grouped_data)

# Periksa jika ada data yang unik
if not grouped_data.empty and grouped_data["cnt"].nunique() == grouped_data.shape[0]:
    # Pivot table untuk visualisasi heatmap
    pivot_table = grouped_data.pivot_table(
        index="temp_binned", columns="hum_binned", values="cnt", aggfunc="mean"
    )

    # Visualisasi hasil clustering
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, cmap="coolwarm")
    plt.title("Jumlah Rata-rata Penyewaan Sepeda berdasarkan Temperatur dan Kelembaban")
    st.pyplot(plt)

    # Visualisasi dengan barplot untuk kecepatan angin
    plt.figure(figsize=(10, 6))
    sns.barplot(x="windspeed_binned", y="cnt", hue="temp_binned", data=grouped_data)
    plt.title(
        "Jumlah Rata-rata Penyewaan Sepeda berdasarkan Kecepatan Angin dan Temperatur"
    )
    st.pyplot(plt)
else:
    st.write("Tidak ada data unik untuk ditampilkan dalam heatmap.")
