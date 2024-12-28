import streamlit as st
import pandas as pd


# Fungsi menghitung BMR dan TDEE
def calculate_bmr_and_tdee(age, weight, height, gender, activity_level):
    if gender == 'pria':
        bmr = 66 + (13.75 * weight) + (5.003 * height) - (6.75 * age)
    else:
        bmr = 655 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
    
    activity_factors = {
        'sangat aktif': 1.9,
        'aktif': 1.725,
        'sedang': 1.55,
        'ringan': 1.375,
        'tidak aktif': 1.2
    }
    tdee = bmr * activity_factors[activity_level]
    return bmr, tdee

# Fungsi untuk memuat dataset
@st.cache_data
def load_data():
    return pd.read_csv("nutrisi.csv", delimiter=";")

# Halaman utama
st.title("Pemodelan Kebutuhan Kalori dan Rekomendasi Makanan Sehat")
st.subheader("Profil Pengguna")

# Input data pengguna
age = st.number_input("Umur (tahun):", min_value=1, max_value=120, step=1)
weight = st.number_input("Berat Badan (kg):", min_value=1.0, max_value=200.0, step=0.1)
height = st.number_input("Tinggi Badan (cm):", min_value=50.0, max_value=250.0, step=0.1)
gender = st.selectbox("Jenis Kelamin:", ["pria", "wanita"])
activity_level = st.selectbox("Tingkat Aktivitas:", ["tidak aktif", "ringan", "sedang", "aktif", "sangat aktif"])

# Perhitungan BMR dan TDEE
if st.button("Hitung Kebutuhan Kalori"):
    bmr, tdee = calculate_bmr_and_tdee(age, weight, height, gender, activity_level)
    # st.write(f"**BMR Anda:** {bmr:.2f} kcal/hari")
    st.write(f"**Kebutuhan Kalori Anda:** {tdee:.2f} kcal/hari")

    # Memuat dataset
    df = load_data()

    # Menambahkan kolom status
    df["status"] = ((df["Protein_g"] >= 20) & 
                    (df["Fat_g"] <= 22) & 
                    (df["Carb_g"] <= 50) & 
                    (df["Sugar_g"] <= 16)).astype(int)

    # Filter makanan sehat
    makanan_sehat = df[df["status"] == 1].copy()
    makanan_sehat["adjusted_weight"] = (tdee / makanan_sehat["Energy_kcal"]) * 100
    makanan_sehat_teratas = makanan_sehat.sort_values(by="Energy_kcal", ascending=False).head(10)

    # Menampilkan rekomendasi makanan
    st.subheader("Rekomendasi Makanan Sehat")
    if not makanan_sehat_teratas.empty:
        for _, row in makanan_sehat_teratas.iterrows():
            st.write(f"- **{row['Descrip']}** ({row['FoodGroup']}) - {row['Energy_kcal']:.1f} kcal/100g, "
                     f"Jumlah disarankan: {row['adjusted_weight']:.2f} gram.")
    else:
        st.write("Tidak ada makanan yang memenuhi kriteria.")
