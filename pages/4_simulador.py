import streamlit as st
import pandas as pd
import joblib

st.set_page_config(layout="wide")

st.title("🎯 Simulador predictivo")

st.write("""
Estimación de la tasa de delitos contra la propiedad (cada 100.000 habitantes)
utilizando el modelo Random Forest entrenado.
""")

st.warning("""
El modelo estima tasas agregadas. 
No predice delitos individuales.
""")

# =========================
# CARGA MODELO
# =========================
@st.cache_resource
def cargar_modelo():
    modelo = joblib.load("models/random_forest.pkl")
    features = joblib.load("models/features_modelo.pkl")
    return modelo, features

modelo, features = cargar_modelo()

# =========================
# CARGA DATASET (para referencia)
# =========================
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

df = cargar_datos()

# =========================
# INPUTS DEL USUARIO
# =========================
# =========================
# SELECCIÓN TERRITORIAL
# =========================

st.markdown("### Selección territorial")

col1, col2, col3 = st.columns(3)

with col1:
    anio = st.selectbox(
        "Año",
        sorted(df["anio"].dropna().unique()),
        index=len(sorted(df["anio"].dropna().unique())) - 1
    )

with col2:
    provincia = st.selectbox(
        "Provincia",
        sorted(df["provincia_nombre"].dropna().unique())
    )

df_provincia = df[
    (df["anio"] == anio) &
    (df["provincia_nombre"] == provincia)
].copy()

with col3:
    departamento = st.selectbox(
        "Departamento",
        sorted(df_provincia["departamento_nombre"].dropna().unique())
    )

fila = df_provincia[
    df_provincia["departamento_nombre"] == departamento
].copy()

# =========================
# PREDICCIÓN
# =========================
st.markdown("### Resultado")

if fila.empty:
    st.warning("No hay datos disponibles para la selección realizada.")
else:
    fila_modelo = fila.copy()

    # Agregar columnas faltantes si el modelo las requiere
    for col in features:
        if col not in fila_modelo.columns:
            fila_modelo[col] = 0

    # Ordenar columnas igual que en entrenamiento
    X_pred = fila_modelo[features]

    if st.button("Predecir tasa"):
        pred = modelo.predict(X_pred)[0]

        tasa_real = fila["tasa_delitos_propiedad_100k_v2"].iloc[0]
        diferencia = pred - tasa_real

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Tasa estimada", f"{pred:,.2f}")

        with col2:
            st.metric("Tasa real observada", f"{tasa_real:,.2f}")

        with col3:
            st.metric("Diferencia", f"{diferencia:,.2f}")

        q1 = df["tasa_delitos_propiedad_100k_v2"].quantile(0.33)
        q2 = df["tasa_delitos_propiedad_100k_v2"].quantile(0.66)

        if pred < q1:
            st.info("Nivel bajo relativo")
        elif pred < q2:
            st.warning("Nivel medio relativo")
        else:
            st.error("Nivel alto relativo")

        st.markdown("### Variables utilizadas por el modelo")

        variables_visibles = [
            "tasa_lag1",
            "log_densidad",
            "Indice_IPC",
            "variacion_anual_cbt",
            "variacion_anual_salarios_pct",
            "variacion_empleo_const_pct",
            "variacion_acceso_internet_pct"
        ]

        variables_disponibles = [
            col for col in variables_visibles if col in fila.columns
        ]

        st.dataframe(
            fila[variables_disponibles].T.rename(columns={fila.index[0]: "valor"})
        )