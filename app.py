import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Observatorio de Delitos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Observatorio de Delitos contra la Propiedad en Argentina")

st.markdown("""
Aplicación interactiva para el análisis territorial y temporal de delitos contra la propiedad a nivel departamento–año.
""")

st.warning("""
Este modelo no predice delitos individuales. 
Estima tasas agregadas cada 100.000 habitantes.
""")

# Cargar dataset (solo para métricas generales)
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

df = cargar_datos()

st.markdown("### Resumen del dataset")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Filas", f"{df.shape[0]:,}")

with col2:
    st.metric("Columnas", df.shape[1])

with col3:
    st.metric("Años", f"{df['anio'].min()} - {df['anio'].max()}")

with col4:
    st.metric("Departamentos", df['departamento_nombre'].nunique())

st.markdown("---")

st.markdown("### Indicadores generales")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tasa promedio", f"{df['tasa_delitos_propiedad_100k_v2'].mean():,.0f}")

with col2:
    st.metric("Máxima", f"{df['tasa_delitos_propiedad_100k_v2'].max():,.0f}")

with col3:
    st.metric("Mínima", f"{df['tasa_delitos_propiedad_100k_v2'].min():,.0f}")

st.markdown("### Navegación")

st.write("""
Utilizá el menú lateral para explorar:

- 📍 Exploración territorial
- 📈 Evolución temporal
- 🤖 Modelos predictivos
- 🎯 Simulador
- 📚 Metodología
""")