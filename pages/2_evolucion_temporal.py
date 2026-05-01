import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📈 Evolución temporal")

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

df = cargar_datos()

# =========================
# FILTRO PROVINCIA
# =========================
provincia = st.selectbox(
    "Seleccionar provincia",
    ["Total país"] + sorted(df["provincia_nombre"].dropna().unique())
)

# =========================
# AGRUPACIÓN
# =========================
if provincia == "Total país":
    df_grouped = df.groupby("anio")["tasa_delitos_propiedad_100k_v2"].mean().reset_index()
else:
    df_grouped = df[df["provincia_nombre"] == provincia] \
        .groupby("anio")["tasa_delitos_propiedad_100k_v2"].mean().reset_index()

# =========================
# GRÁFICO PRINCIPAL
# =========================
fig = px.line(
    df_grouped,
    x="anio",
    y="tasa_delitos_propiedad_100k_v2",
    markers=True,
    title="Evolución de la tasa de delitos"
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Año",
    yaxis_title="Tasa cada 100.000 habitantes"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# COMPARACIÓN MULTI-PROVINCIA
# =========================
st.markdown("### Comparación entre provincias")

provincias_sel = st.multiselect(
    "Seleccionar provincias",
    sorted(df["provincia_nombre"].dropna().unique()),
    default=sorted(df["provincia_nombre"].dropna().unique())[:3]
)

df_multi = df[df["provincia_nombre"].isin(provincias_sel)] \
    .groupby(["anio", "provincia_nombre"])["tasa_delitos_propiedad_100k_v2"] \
    .mean().reset_index()

fig2 = px.line(
    df_multi,
    x="anio",
    y="tasa_delitos_propiedad_100k_v2",
    color="provincia_nombre",
    markers=True,
    title="Comparación de evolución por provincia"
)

fig2.update_layout(
    title_x=0.5,
    xaxis_title="Año",
    yaxis_title="Tasa cada 100.000 habitantes"
)

st.plotly_chart(fig2, use_container_width=True)