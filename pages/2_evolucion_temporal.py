import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.caption("Proyecto de análisis y modelado de delitos - Argentina (2017–2024)")

st.title("📈 Evolución temporal")

st.write("""
Esta sección permite analizar la evolución anual de la tasa de delitos contra la propiedad,
tanto a nivel nacional como por provincia.
""")

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

with st.spinner("Cargando datos..."):
    df = cargar_datos()

provincia = st.selectbox(
    "Seleccionar provincia",
    ["Total país"] + sorted(df["provincia_nombre"].dropna().unique())
)

if provincia == "Total país":
    df_grouped = df.groupby("anio")["tasa_delitos_propiedad_100k_v2"].mean().reset_index()
else:
    df_grouped = (
        df[df["provincia_nombre"] == provincia]
        .groupby("anio")["tasa_delitos_propiedad_100k_v2"]
        .mean()
        .reset_index()
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tasa promedio", f"{df_grouped['tasa_delitos_propiedad_100k_v2'].mean():,.0f}")

with col2:
    st.metric("Máxima anual", f"{df_grouped['tasa_delitos_propiedad_100k_v2'].max():,.0f}")

with col3:
    st.metric("Mínima anual", f"{df_grouped['tasa_delitos_propiedad_100k_v2'].min():,.0f}")

fig = px.line(
    df_grouped,
    x="anio",
    y="tasa_delitos_propiedad_100k_v2",
    markers=True,
    title=f"Evolución de la tasa de delitos - {provincia}"
)

fig.update_layout(
    template="plotly_dark",
    title_x=0.5,
    xaxis_title="Año",
    yaxis_title="Tasa cada 100.000 habitantes",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### Comparación entre provincias")

provincias = sorted(df["provincia_nombre"].dropna().unique())

provincias_sel = st.multiselect(
    "Seleccionar provincias",
    provincias,
    default=provincias[:3]
)

if provincias_sel:
    df_multi = (
        df[df["provincia_nombre"].isin(provincias_sel)]
        .groupby(["anio", "provincia_nombre"])["tasa_delitos_propiedad_100k_v2"]
        .mean()
        .reset_index()
    )

    fig2 = px.line(
        df_multi,
        x="anio",
        y="tasa_delitos_propiedad_100k_v2",
        color="provincia_nombre",
        markers=True,
        title="Comparación de evolución por provincia"
    )

    fig2.update_layout(
        template="plotly_dark",
        title_x=0.5,
        xaxis_title="Año",
        yaxis_title="Tasa cada 100.000 habitantes",
        hovermode="x unified",
        legend_title="Provincia"
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Seleccioná al menos una provincia para mostrar la comparación.")