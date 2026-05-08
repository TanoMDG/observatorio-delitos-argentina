import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Observatorio de Delitos",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
/* Contenedor */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Títulos */
h1, h2, h3 {
    letter-spacing: 0.5px;
}

/* Cards */
.card {
    padding: 1.2rem;
    border-radius: 12px;
    background: linear-gradient(145deg, #111827, #1f2937);
    border: 1px solid rgba(255,255,255,0.05);
}

/* Botones */
.stButton>button {
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}

/* Inputs */
.stNumberInput input {
    text-align: center;
}

/* Alertas */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Observatorio de Delitos contra la Propiedad")

st.markdown("""
Aplicación interactiva para el análisis territorial, temporal y predictivo
de delitos contra la propiedad en Argentina a nivel departamento–año.
""")

st.warning("""
Este modelo no predice delitos individuales. 
Las estimaciones representan tasas agregadas cada 100.000 habitantes.
""")

# =========================
# CARGA DE DATOS
# =========================

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/final/dataset_mapa_sup_final.csv")

with st.spinner("Cargando datos..."):
    df = cargar_datos()

# =========================
# MÉTRICAS PRINCIPALES
# =========================

st.markdown("## 📌 Resumen general")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Registros", f"{df.shape[0]:,}")

with col2:
    st.metric("Variables", df.shape[1])

with col3:
    st.metric("Período", f"{df['anio'].min()} - {df['anio'].max()}")

with col4:
    st.metric("Departamentos", df['departamento_nombre'].nunique())

st.markdown("---")

# =========================
# INDICADORES
# =========================

st.markdown("## 📈 Indicadores clave")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Tasa promedio",
        f"{df['tasa_delitos_propiedad_100k_v2'].mean():,.0f}"
    )

with col2:
    st.metric(
        "Tasa máxima",
        f"{df['tasa_delitos_propiedad_100k_v2'].max():,.0f}"
    )

with col3:
    st.metric(
        "Tasa mínima",
        f"{df['tasa_delitos_propiedad_100k_v2'].min():,.0f}"
    )

st.markdown("---")

# =========================
# SECCIONES DE LA APP
# =========================

st.markdown("## 🧭 Secciones disponibles")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📍 Exploración territorial</h3>
        <p>Mapas interactivos y análisis espacial de delitos.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>📈 Evolución temporal</h3>
        <p>Análisis histórico y tendencias entre 2017–2024.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🤖 Modelos predictivos</h3>
        <p>Comparación entre regresión, panel y Random Forest.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>🎯 Simulador</h3>
        <p>Estimación interactiva de tasas bajo distintas condiciones.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🔮 Proyección</h3>
        <p>Simulación de escenarios futuros optimistas y pesimistas.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>📚 Metodología</h3>
        <p>Proceso completo de construcción, EDA y modelado.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.caption(
    "Proyecto de Ciencia de Datos aplicado al análisis territorial del delito en Argentina."
)