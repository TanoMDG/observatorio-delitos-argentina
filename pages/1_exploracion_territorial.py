import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import branca.colormap as cm
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("📍 Exploración territorial")

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

df = cargar_datos()

# =========================
# FILTROS
# =========================
st.markdown("### Filtros")

col1, col2 = st.columns(2)

with col1:
    anio = st.selectbox(
        "Año",
        sorted(df["anio"].unique()),
        index=len(sorted(df["anio"].unique())) - 1
    )

with col2:
    provincia = st.selectbox(
        "Provincia",
        ["Todas"] + sorted(df["provincia_nombre"].dropna().unique())
    )

# =========================
# FILTRADO
# =========================
df_filtrado = df[df["anio"] == anio]

if provincia != "Todas":
    df_filtrado = df_filtrado[df_filtrado["provincia_nombre"] == provincia]

# =========================
# TOP DEPARTAMENTOS
# =========================
st.markdown("### Top departamentos")

top_df = df_filtrado.sort_values(
    by="tasa_delitos_propiedad_100k_v2",
    ascending=False
).head(15)

fig = px.bar(
    top_df,
    x="departamento_nombre",
    y="tasa_delitos_propiedad_100k_v2",
    color="provincia_nombre",
    title="Top 15 departamentos con mayor tasa de delitos"
)

fig.update_layout(
    title_x=0.5,
    xaxis_tickangle=-45,
    margin=dict(l=20, r=20, t=60, b=120)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MAPA PROFESIONAL
# =========================
st.markdown("### Mapa de delitos")

def calcular_radio(valor, vmin, vmax, rmin=4, rmax=16):
    if vmax == vmin:
        return (rmin + rmax) / 2
    return rmin + ((valor - vmin) / (vmax - vmin)) * (rmax - rmin)

def formatear_numero(valor, decimales=2):
    return f"{valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")

df_mapa = df_filtrado.dropna(
    subset=["lat", "lon", "tasa_delitos_propiedad_100k_v2"]
)

if df_mapa.empty:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
else:
    center_lat = df_mapa["lat"].mean()
    center_lon = df_mapa["lon"].mean()

    zoom_base = 4 if provincia == "Todas" else 6

    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_base,
        tiles="CartoDB dark_matter",
        control_scale=True
    )

    tasa_min = df_mapa["tasa_delitos_propiedad_100k_v2"].min()
    tasa_max = df_mapa["tasa_delitos_propiedad_100k_v2"].max()

    colormap = cm.LinearColormap(
        colors=["#ffe082", "#ffb74d", "#ff7043", "#f4511e", "#d32f2f", "#8e0038"],
        vmin=tasa_min,
        vmax=tasa_max
    )
    colormap.add_to(mapa)

    for _, row in df_mapa.iterrows():
        tasa = row["tasa_delitos_propiedad_100k_v2"]
        radio = calcular_radio(tasa, tasa_min, tasa_max)

        popup_html = f"""
        <b>{row['departamento_nombre']}</b><br>
        Provincia: {row['provincia_nombre']}<br>
        Tasa: {formatear_numero(tasa)}
        """

        tooltip = f"{row['departamento_nombre']} | Tasa: {formatear_numero(tasa)}"

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radio,
            popup=popup_html,
            tooltip=tooltip,
            color="#111",
            fill=True,
            fill_color=colormap(tasa),
            fill_opacity=0.8
        ).add_to(mapa)

    st_folium(mapa, width=1200, height=650)