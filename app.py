import streamlit as st
import pandas as pd

# URLs de las hojas de Google Sheets en CSV
URL_LESSONS = "https://docs.google.com/spreadsheets/d/1R8GzRVL58XxheG0FRtSRfE6Ib5E_GcZh1Ws_iaDOpbk/export?format=csv&gid=106910283"
URL_HISTORIAL = "https://docs.google.com/spreadsheets/d/1R8GzRVL58XxheG0FRtSRfE6Ib5E_GcZh1Ws_iaDOpbk/export?format=csv&gid=1305291435"

st.title("Latam Queue: Evaluación de Lecciones")
st.write("📋 Sistema de Gestión de QA para formatos RR y QR")

@st.cache_data
def load_data():
    try:
        df_lessons = pd.read_csv(URL_LESSONS, dtype=str)
    except Exception as e:
        st.error(f"Error cargando lecciones: {e}")
        df_lessons = pd.DataFrame()

    try:
        df_hist = pd.read_csv(URL_HISTORIAL, dtype=str)
    except Exception as e:
        st.error(f"Error cargando historial: {e}")
        df_hist = pd.DataFrame()

    return df_lessons, df_hist

df_lessons, df_hist = load_data()

st.subheader("📘 Lecciones LATAM")
st.write(f"Filas cargadas: {len(df_lessons)}")
st.dataframe(df_lessons)

st.subheader("📜 Historial de Revisiones")
st.write(f"Filas cargadas: {len(df_hist)}")
st.dataframe(df_hist)
