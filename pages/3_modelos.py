import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.title("🤖 Modelos predictivos")

# =========================
# CARGA DATOS
# =========================
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

df = cargar_datos()

# =========================
# MÉTRICAS MODELOS (HARDCODEADAS)
# =========================
st.markdown("### Comparación de modelos")

metricas = pd.DataFrame({
    "Modelo": ["Regresión Lineal", "Efectos Fijos", "Random Forest"],
    "MAE": [454, 377, 270],
    "RMSE": [560, 496, 386],
    "R2": [0.78, 0.83, 0.897]
})

st.markdown("#### Métricas principales")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Mejor MAE", "270", "Random Forest")

with col2:
    st.metric("Mejor RMSE", "386", "Random Forest")

with col3:
    st.metric("Mejor R²", "0.897", "Random Forest")

metricas_long = metricas.melt(
    id_vars="Modelo",
    value_vars=["MAE", "RMSE", "R2"],
    var_name="Métrica",
    value_name="Valor"
)

fig_metricas = make_subplots(specs=[[{"secondary_y": True}]])

fig_metricas.add_trace(
    go.Bar(
        x=metricas["Modelo"],
        y=metricas["MAE"],
        name="MAE",
        text=metricas["MAE"],
        textposition="outside"
    ),
    secondary_y=False
)

fig_metricas.add_trace(
    go.Bar(
        x=metricas["Modelo"],
        y=metricas["RMSE"],
        name="RMSE",
        text=metricas["RMSE"],
        textposition="outside"
    ),
    secondary_y=False
)

fig_metricas.add_trace(
    go.Scatter(
        x=metricas["Modelo"],
        y=metricas["R2"],
        name="R²",
        mode="lines+markers+text",
        text=metricas["R2"],
        textposition="top center",
        line=dict(width=3)
    ),
    secondary_y=True
)

fig_metricas.update_layout(
    title="Comparación general de desempeño de modelos",
    title_x=0.5,
    barmode="group",
    xaxis_title="Modelo",
    legend_title="Métrica",
    margin=dict(l=20, r=20, t=70, b=60)
)

fig_metricas.update_yaxes(
    title_text="MAE / RMSE",
    secondary_y=False
)

fig_metricas.update_yaxes(
    title_text="R²",
    range=[0, 1],
    secondary_y=True
)

st.plotly_chart(fig_metricas, use_container_width=True)
# =========================
# INTERPRETACIÓN
# =========================
st.markdown("### Interpretación")

st.write("""
- El modelo Random Forest presenta el mejor desempeño.
- Se observa una fuerte persistencia temporal (tasa_lag1).
- La densidad poblacional tiene un impacto relevante.
- Las variables económicas presentan menor peso explicativo.
""")

# =========================
# IMPORTANCIA DE VARIABLES
# =========================
st.markdown("### Importancia de variables (Random Forest)")

@st.cache_resource
def cargar_modelo():
    modelo = joblib.load("models/random_forest.pkl")
    features = joblib.load("models/features_modelo.pkl")
    return modelo, features

modelo, features = cargar_modelo()

importancias = pd.DataFrame({
    "feature": features,
    "importancia": modelo.feature_importances_
}).sort_values(by="importancia", ascending=False)

fig_imp = px.bar(
    importancias.head(10),
    x="importancia",
    y="feature",
    orientation="h",
    title="Top variables más importantes"
)

fig_imp.update_layout(title_x=0.5,
                      yaxis=dict(autorange="reversed"))

st.plotly_chart(fig_imp, use_container_width=True)