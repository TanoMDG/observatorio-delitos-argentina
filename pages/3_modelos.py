import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.caption("Proyecto de análisis y modelado de delitos - Argentina (2017–2024)")

st.title("🤖 Modelos predictivos")

st.write("""
Esta sección compara los modelos entrenados para estimar la tasa de delitos contra la propiedad
y permite interpretar qué variables tuvieron mayor peso en el modelo Random Forest.
""")

# =========================
# CARGA DATOS
# =========================
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

with st.spinner("Cargando datos..."):
    df = cargar_datos()

# =========================
# MÉTRICAS MODELOS
# =========================
st.markdown("### Comparación de modelos")

metricas = pd.DataFrame({
    "Modelo": ["Regresión Lineal", "Efectos Fijos", "Random Forest"],
    "MAE": [454, 377, 270],
    "RMSE": [560, 496, 386],
    "R²": [0.78, 0.83, 0.897]
})

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Menor MAE", "270", "Random Forest")

with col2:
    st.metric("Menor RMSE", "386", "Random Forest")

with col3:
    st.metric("Mayor R²", "0.897", "Random Forest")

st.dataframe(metricas, width="stretch")

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
        y=metricas["R²"],
        name="R²",
        mode="lines+markers+text",
        text=metricas["R²"],
        textposition="top center",
        line=dict(width=3)
    ),
    secondary_y=True
)

fig_metricas.update_layout(
    template="plotly_dark",
    title="Comparación general / desempeño de modelos",
    title_x=0.5,
    barmode="group",
    xaxis_title="Modelo",
    legend_title="Métrica",
    margin=dict(l=20, r=20, t=70, b=60),
    hovermode="x unified"
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

st.plotly_chart(fig_metricas, width="stretch")

st.info("""
MAE y RMSE se expresan en unidades de tasa cada 100.000 habitantes.
R² se representa con eje secundario porque su escala va de 0 a 1.
""")

# =========================
# INTERPRETACIÓN
# =========================
st.markdown("### Interpretación")

st.markdown("""
- **Random Forest** presenta el mejor desempeño global.
- La reducción de MAE y RMSE indica menor error predictivo.
- El aumento de R² muestra mayor capacidad explicativa.
- La mejora del modelo no lineal sugiere que el fenómeno presenta relaciones complejas.
""")

# =========================
# IMPORTANCIA DE VARIABLES
# =========================
st.markdown("### Importancia de variables")

@st.cache_resource
def cargar_modelo():
    modelo = joblib.load("models/random_forest.pkl")
    features = joblib.load("models/features_modelo.pkl")
    return modelo, features

modelo, features = cargar_modelo()

importancias = (
    pd.DataFrame({
        "Variable": features,
        "Importancia": modelo.feature_importances_
    })
    .sort_values(by="Importancia", ascending=False)
    .head(10)
)

fig_imp = px.bar(
    importancias.sort_values(by="Importancia", ascending=True),
    x="Importancia",
    y="Variable",
    orientation="h",
    text="Importancia",
    title="Top 10 variables más importantes - Random Forest"
)

fig_imp.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)

fig_imp.update_layout(
    template="plotly_dark",
    title_x=0.5,
    xaxis_title="Importancia relativa",
    yaxis_title="Variable",
    margin=dict(l=20, r=20, t=70, b=40)
)

st.plotly_chart(fig_imp, width="stretch")

st.success("""
El resultado confirma que la variable `tasa_lag1` domina la predicción, 
lo que refuerza la hipótesis de fuerte persistencia temporal del fenómeno.
""")