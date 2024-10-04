import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data
@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')  # Ganti dengan path file Anda
    return df

df = load_data()

# Cleaning data
def clean_data(df):
    # Menghapus duplikat
    df.drop_duplicates(inplace=True)
    
    # Mengatasi missing values
    if df.isnull().sum().sum() > 0:
        st.warning('Missing values found! Cleaning data...')
        df.fillna(method='ffill', inplace=True)  # Ganti dengan metode yang sesuai
    
    return df

df_clean = clean_data(df)

# Analisis Cuaca
st.header('Analisis Pengaruh Cuaca Terhadap Penyewaan Sepeda')

# Visualisasi pengaruh cuaca
def weather_analysis(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='weathersit', y='cnt', data=df)
    plt.title('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(plt)

weather_analysis(df_clean)

# Penggunaan berdasarkan hari libur dan hari kerja
st.header('Analisis Pengaruh Hari Libur dan Hari Kerja')

def holiday_analysis(df):
    df['holiday'] = df['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
    plt.figure(figsize=(10, 6))
    sns.countplot(x='holiday', data=df, hue='casual', alpha=0.6)
    plt.title('Pola Penggunaan Pengguna Kasual pada Hari Libur dan Hari Kerja')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

holiday_analysis(df_clean)

# Kesimpulan
st.header('Kesimpulan')
st.write("""
- **Cuaca Cerah Meningkatkan Jumlah Rental Sepeda**: Cuaca cerah menunjukkan jumlah rental sepeda tertinggi.
- **Hujan Berat Mengurangi Jumlah Rental Sepeda**: Hujan berat menunjukkan jumlah rental sepeda yang jauh lebih rendah.
- **Dampak Hari Libur dan Hari Kerja**: Pengguna kasual lebih banyak menggunakan sepeda pada hari libur dibandingkan pengguna terdaftar.
""")

# Menjalankan Streamlit
if __name__ == '__main__':
    st.title('Dashboard Penyewaan Sepeda')
    st.write('Visualisasi dan analisis data penyewaan sepeda berdasarkan cuaca dan hari.')
