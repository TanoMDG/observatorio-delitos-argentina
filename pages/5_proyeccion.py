import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("🔮 Proyección con escenarios")

st.write("""
Esta sección permite estimar tasas futuras de delitos contra la propiedad bajo distintos escenarios.
Las proyecciones son exploratorias y dependen de los supuestos definidos.
""")

st.warning("""
Las proyecciones no deben interpretarse como predicciones determinísticas.
Representan simulaciones agregadas bajo supuestos de escenario.
""")

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

@st.cache_resource
def cargar_modelo():
    modelo = joblib.load("models/random_forest.pkl")
    features = joblib.load("models/features_modelo.pkl")
    return modelo, features

df = cargar_datos()
modelo, features = cargar_modelo()

st.markdown("### Selección base")

col1, col2, col3 = st.columns(3)

with col1:
    anios = sorted(df["anio"].dropna().unique())
    anio_base = st.selectbox("Año base", anios, index=len(anios) - 1)

with col2:
    provincia = st.selectbox(
        "Provincia",
        sorted(df["provincia_nombre"].dropna().unique())
    )

df_prov = df[
    (df["anio"] == anio_base) &
    (df["provincia_nombre"] == provincia)
].copy()

with col3:
    departamentos = sorted(df_prov["departamento_nombre"].dropna().unique())
    departamento = st.selectbox("Departamento", departamentos)

fila = df_prov[df_prov["departamento_nombre"] == departamento].copy()

st.markdown("### Datos base seleccionados")

if fila.empty:
    st.warning("No hay datos disponibles.")
    st.stop()

tasa_base = fila["tasa_delitos_propiedad_100k_v2"].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric("Tasa base", f"{tasa_base:,.2f}")

with col2:
    st.metric("Año base", anio_base)

st.markdown("### Escenario de simulación")

col1, col2 = st.columns(2)

with col1:
    escenario = st.selectbox(
        "Escenario",
        ["Base", "Optimista", "Pesimista"]
    )

with col2:
    horizonte = st.slider(
        "Años a proyectar",
        min_value=1,
        max_value=3,
        value=2
    )

st.markdown("#### Supuestos del escenario")

if escenario == "Optimista":
    st.success("↑ salarios, ↑ empleo, ↓ presión económica (CBT)")
elif escenario == "Pesimista":
    st.error("↓ salarios, ↓ empleo, ↑ presión económica (CBT)")
else:
    st.info("Se mantienen condiciones del año base")


def ajustar_variables(fila_base, escenario_seleccionado):
    fila_adj = fila_base.copy()

    if escenario_seleccionado == "Optimista":
        fila_adj["variacion_anual_salarios_pct"] *= 1.2
        fila_adj["variacion_empleo_const_pct"] *= 1.2
        fila_adj["variacion_anual_cbt"] *= 0.8

    elif escenario_seleccionado == "Pesimista":
        fila_adj["variacion_anual_salarios_pct"] *= 0.8
        fila_adj["variacion_empleo_const_pct"] *= 0.8
        fila_adj["variacion_anual_cbt"] *= 1.2

    return fila_adj


st.markdown("### Resultado de la proyección")

if st.button("Generar proyección"):
    resultados = []

    fila_actual = fila.copy()
    tasa_lag = tasa_base

    for i in range(1, horizonte + 1):
        anio_proyectado = anio_base + i

        fila_escenario = ajustar_variables(fila_actual, escenario)

        fila_escenario["tasa_lag1"] = tasa_lag

        for col in features:
            if col not in fila_escenario.columns:
                fila_escenario[col] = 0

        X_future = fila_escenario[features]

        pred = modelo.predict(X_future)[0]

        resultados.append({
            "anio": anio_proyectado,
            "tipo": "Proyectado",
            "tasa": pred
        })

        tasa_lag = pred
        fila_actual = fila_escenario.copy()

    df_resultados = pd.DataFrame(resultados)

    df_base = pd.DataFrame([{
        "anio": anio_base,
        "tipo": "Real base",
        "tasa": tasa_base
    }])

    df_plot = pd.concat([df_base, df_resultados], ignore_index=True)

    st.markdown("### Tabla de resultados")
    st.dataframe(df_plot, use_container_width=True)

    st.info(
        "La proyección utiliza la tasa estimada de cada año como tasa rezagada para el año siguiente. "
        "Las demás variables se ajustan según el escenario seleccionado."
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_base["anio"],
        y=df_base["tasa"],
        mode="markers",
        name="Real base",
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=df_resultados["anio"],
        y=df_resultados["tasa"],
        mode="lines+markers",
        name="Proyectado",
        line=dict(width=3, dash="dash")
    ))

    fig.add_vline(
        x=anio_base,
        line_width=2,
        line_dash="dot",
        annotation_text="Inicio proyección",
        annotation_position="top"
    )

    fig.update_layout(
        title=f"Proyección de tasa - {departamento}, {provincia}",
        title_x=0.5,
        xaxis_title="Año",
        yaxis_title="Tasa cada 100.000 habitantes"
    )

    st.plotly_chart(fig, use_container_width=True)