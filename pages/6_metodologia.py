import streamlit as st

st.set_page_config(layout="wide")

st.title("📚 Metodología")

st.info(
    "Esta sección resume el proceso metodológico utilizado para construir, analizar "
    "y modelar el dataset de delitos contra la propiedad en Argentina."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unidad de análisis", "Departamento–año")

with col2:
    st.metric("Período", "2017–2024")

with col3:
    st.metric("Modelo principal", "Random Forest")

st.markdown("---")

with st.expander("🎯 1. Objetivo del proyecto", expanded=True):
    st.write("""
    Analizar la distribución territorial y la evolución temporal de los delitos contra 
    la propiedad en Argentina, incorporando variables socioeconómicas para enriquecer 
    la interpretación del fenómeno.
    """)

with st.expander("🗂️ 2. Fuentes de datos"):
    st.write("""
    El proyecto integra datos provenientes de distintas fuentes oficiales:
    
    - SNIC: registros de delitos contra la propiedad.
    - INDEC: IPC, salarios, CBT, empleo, IPIM e internet.
    - Redatam / Censo 2022: población departamental.
    - GeoRef: coordenadas y referencias geográficas.
    """)

with st.expander("🧱 3. Construcción del dataset"):
    st.write("""
    Se construyó un dataset consolidado con unidad de análisis departamento–año.
    Para ello se normalizaron claves territoriales, se resolvieron inconsistencias 
    entre fuentes y se calcularon tasas comparables.
    """)
    
    st.code(
        "tasa_delitos_propiedad_100k_v2 = (delitos / población anual) * 100.000",
        language="text"
    )

with st.expander("⚙️ 4. Feature engineering"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Variables estructurales**")
        st.write("""
        - densidad_poblacion
        - log_densidad
        """)

    with col2:
        st.markdown("**Variables temporales**")
        st.write("""
        - tasa_lag1
        - tasa_yoy
        - variables rezagadas
        """)

    with col3:
        st.markdown("**Variables socioeconómicas**")
        st.write("""
        - IPC
        - CBT
        - salarios
        - empleo
        - internet
        """)

with st.expander("📊 5. Hallazgos del análisis exploratorio"):
    st.write("""
    El análisis exploratorio mostró una fuerte persistencia temporal del fenómeno, 
    evidenciada por la alta correlación entre la tasa actual y la tasa rezagada.
    """)
    
    st.markdown("""
    - `tasa_lag1`: correlación aproximada de 0.92.
    - `log_densidad`: correlación aproximada de 0.47.
    - Variables económicas: correlaciones bajas.
    - Acceso a internet: asociación casi nula.
    """)

with st.expander("🤖 6. Modelado"):
    st.write("""
    Se implementaron tres enfoques complementarios:
    """)
    
    st.markdown("""
    - **Regresión Lineal:** modelo baseline interpretable.
    - **Efectos Fijos:** captura heterogeneidad territorial.
    - **Random Forest:** mejora predictiva y captura relaciones no lineales.
    """)

with st.expander("📈 7. Resultados"):
    st.success("""
    El modelo Random Forest obtuvo el mejor desempeño general, con MAE aproximado de 270, 
    RMSE aproximado de 386 y R² cercano a 0.897.
    """)

with st.expander("⚠️ 8. Limitaciones"):
    st.warning("""
    El modelo no predice delitos individuales. Estima tasas agregadas a nivel territorial.
    Además, la predicción futura depende de la disponibilidad de variables exógenas.
    """)

with st.expander("🧠 9. Uso responsable"):
    st.write("""
    La aplicación debe entenderse como una herramienta analítica y exploratoria. 
    Sus resultados no deben utilizarse como base única para decisiones operativas, 
    policiales o judiciales.
    """)