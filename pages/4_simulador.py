import streamlit as st
import pandas as pd
import joblib

st.set_page_config(layout="wide")

st.caption("Proyecto de análisis y modelado de delitos - Argentina (2017–2024)")

st.title("🎯 Simulador predictivo")

st.write("""
Esta sección permite seleccionar un departamento y estimar su tasa de delitos contra la propiedad
utilizando el modelo XGBoost entrenado. La predicción se compara con la tasa real observada
para el año seleccionado.
""")

st.info("""
La simulación utiliza las variables reales disponibles para el departamento y año seleccionados.
No permite predecir un departamento inexistente ni cargar valores manuales en esta sección.
""")

st.warning("""
El modelo estima tasas agregadas cada 100.000 habitantes. 
No predice delitos individuales.
""")

# =========================
# CARGA MODELO
# =========================
@st.cache_resource
def cargar_modelo():
    modelo = joblib.load("models/xgboost.pkl")
    features = joblib.load("models/features_modelo.pkl")
    return modelo, features

# =========================
# CARGA DATASET
# =========================
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

with st.spinner("Cargando modelo y datos..."):
    modelo, features = cargar_modelo()
    df = cargar_datos()

# =========================
# SELECCIÓN TERRITORIAL
# =========================
st.markdown("### Selección territorial")

col1, col2, col3 = st.columns(3)

with col1:
    anios = sorted(df["anio"].dropna().unique())
    anio = st.selectbox(
        "Año",
        anios,
        index=len(anios) - 1
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
    departamentos = sorted(df_provincia["departamento_nombre"].dropna().unique())
    departamento = st.selectbox(
        "Departamento",
        departamentos
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
    st.stop()

fila_modelo = fila.copy()

# Agregar columnas faltantes si el modelo las requiere
for col in features:
    if col not in fila_modelo.columns:
        fila_modelo[col] = 0

# Ordenar columnas igual que en entrenamiento
X_pred = fila_modelo[features]

if st.button("Estimar tasa"):
    try:
        pred = modelo.predict(X_pred)[0]

        tasa_real = fila["tasa_delitos_propiedad_100k_v2"].iloc[0]
        diferencia = pred - tasa_real

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Tasa estimada", f"{pred:,.2f}")

        with col2:
            st.metric("Tasa real observada", f"{tasa_real:,.2f}")

        with col3:
            st.metric(
                "Diferencia",
                f"{diferencia:,.2f}",
                delta=f"{diferencia:,.2f}"
            )

        q1 = df["tasa_delitos_propiedad_100k_v2"].quantile(0.33)
        q2 = df["tasa_delitos_propiedad_100k_v2"].quantile(0.66)

        if pred < q1:
            st.success("Nivel bajo relativo")
        elif pred < q2:
            st.warning("Nivel medio relativo")
        else:
            st.error("Nivel alto relativo")

        if diferencia > 0:
            st.info("El modelo estimó una tasa superior a la observada.")
        elif diferencia < 0:
            st.info("El modelo estimó una tasa inferior a la observada.")
        else:
            st.info("La predicción coincide con la tasa observada.")

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

        tabla_variables = (
            fila[variables_disponibles]
            .T
            .rename(columns={fila.index[0]: "valor"})
        )

        st.dataframe(tabla_variables, width="stretch")

    except Exception as e:
        st.error("No se pudo generar la predicción.")
        st.exception(e)