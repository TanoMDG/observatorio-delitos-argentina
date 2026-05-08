import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import branca.colormap as cm
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.caption("Proyecto de análisis y modelado de delitos - Argentina (2017–2024)")

st.title("📍 Exploración territorial")

st.write("""
Esta sección permite analizar la distribución territorial de los delitos contra la propiedad,
identificando departamentos con mayor tasa relativa y visualizando patrones espaciales en el mapa.
""")

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

with st.spinner("Cargando datos..."):
    df = cargar_datos()

st.markdown("### Filtros")

col1, col2 = st.columns(2)

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
        ["Todas"] + sorted(df["provincia_nombre"].dropna().unique())
    )

df_filtrado = df[df["anio"] == anio].copy()

if provincia != "Todas":
    df_filtrado = df_filtrado[df_filtrado["provincia_nombre"] == provincia].copy()

st.markdown("### Resumen del filtro seleccionado")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Departamentos", df_filtrado["departamento_nombre"].nunique())

with col2:
    st.metric(
        "Tasa promedio",
        f"{df_filtrado['tasa_delitos_propiedad_100k_v2'].mean():,.0f}"
    )

with col3:
    st.metric(
        "Tasa máxima",
        f"{df_filtrado['tasa_delitos_propiedad_100k_v2'].max():,.0f}"
    )

st.markdown("---")

st.markdown("### Top departamentos por tasa")

top_df = (
    df_filtrado
    .sort_values(by="tasa_delitos_propiedad_100k_v2", ascending=False)
    .head(15)
    .sort_values(by="tasa_delitos_propiedad_100k_v2", ascending=True)
)

fig = px.bar(
    top_df,
    x="tasa_delitos_propiedad_100k_v2",
    y="departamento_nombre",
    color="provincia_nombre",
    orientation="h",
    text="tasa_delitos_propiedad_100k_v2",
    title=f"Top 15 departamentos con mayor tasa - {anio}"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    title_x=0.5,
    xaxis_title="Tasa cada 100.000 habitantes",
    yaxis_title="Departamento",
    legend_title="Provincia",
    margin=dict(l=20, r=20, t=70, b=40)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### Mapa de delitos")

def calcular_radio(valor, vmin, vmax, rmin=4, rmax=16):
    if vmax == vmin:
        return (rmin + rmax) / 2
    return rmin + ((valor - vmin) / (vmax - vmin)) * (rmax - rmin)

def formatear_numero(valor, decimales=2):
    return f"{valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")

df_mapa = df_filtrado.dropna(
    subset=["lat", "lon", "tasa_delitos_propiedad_100k_v2"]
).copy()

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

    colormap.caption = "Tasa cada 100.000 habitantes"
    colormap.add_to(mapa)

    for _, row in df_mapa.iterrows():
        tasa = row["tasa_delitos_propiedad_100k_v2"]
        radio = calcular_radio(tasa, tasa_min, tasa_max)

        hechos = row["delitos_propiedad_hechos"] if "delitos_propiedad_hechos" in row else None

        popup_html = f"""
        <div style="font-family: Arial; font-size: 13px; width: 260px;">
            <b>{row['departamento_nombre']}</b><br>
            Provincia: {row['provincia_nombre']}<br>
            Año: {row['anio']}<br>
            Tasa: {formatear_numero(tasa)}<br>
            Hechos registrados: {formatear_numero(hechos, 0) if pd.notna(hechos) else 'N/D'}
        </div>
        """

        tooltip = (
            f"{row['departamento_nombre']} | "
            f"{row['provincia_nombre']} | "
            f"Tasa: {formatear_numero(tasa)}"
        )

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radio,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=tooltip,
            color="#111",
            weight=0.7,
            fill=True,
            fill_color=colormap(tasa),
            fill_opacity=0.8
        ).add_to(mapa)

    st_folium(mapa, use_container_width=True, height=650)