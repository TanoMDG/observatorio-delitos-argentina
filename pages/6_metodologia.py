import streamlit as st

st.set_page_config(layout="wide")

st.caption("Proyecto de análisis y modelado de delitos - Argentina (2017–2024)")

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
    
    - **SNIC:** registros de delitos contra la propiedad.
    - **INDEC:** IPC, salarios, CBT, empleo, IPIM e internet.
    - **Redatam / Censo 2022:** población departamental.
    - **GeoRef:** coordenadas y referencias geográficas.
    """)

with st.expander("🧱 3. Construcción del dataset"):
    st.write("""
    Se construyó un dataset consolidado con unidad de análisis **departamento–año**.
    Para ello se normalizaron claves territoriales, se resolvieron inconsistencias 
    entre fuentes, se integró población anual y se calcularon tasas comparables.
    """)
    
    st.code(
        "tasa_delitos_propiedad_100k_v2 = (delitos_propiedad_hechos / población_anual) * 100.000",
        language="text"
    )

with st.expander("⚙️ 4. Feature engineering"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Variables estructurales**")
        st.write("""
        - densidad_poblacion
        - log_densidad
        - superficie departamental
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
        - IPIM
        """)

with st.expander("📊 5. Hallazgos del análisis exploratorio"):
    st.write("""
    El análisis exploratorio mostró una fuerte persistencia temporal del fenómeno, 
    evidenciada por la alta correlación entre la tasa actual y la tasa rezagada.
    """)
    
    st.markdown("""
    - `tasa_lag1`: correlación aproximada de 0.92.
    - `log_densidad`: correlación aproximada de 0.47.
    - Variables económicas: correlaciones bajas, cercanas a 0.1.
    - Acceso a internet: asociación prácticamente nula.
    """)

with st.expander("🤖 6. Modelado"):
    st.write("""
    Se implementaron tres enfoques complementarios para comparar interpretabilidad,
    control territorial y capacidad predictiva.
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
    
    st.write("""
    La importancia de variables confirma que `tasa_lag1` domina la predicción,
    seguida por `log_densidad`, mientras que las variables económicas presentan
    menor peso relativo.
    """)

with st.expander("🔁 8. Flujo metodológico"):
    st.markdown("""
    1. Comprensión del problema.
    2. Recolección de fuentes oficiales.
    3. Limpieza y normalización territorial.
    4. Integración de población, superficie y variables socioeconómicas.
    5. Construcción de tasas comparables.
    6. Feature engineering.
    7. EDA territorial y temporal.
    8. Modelado explicativo y predictivo.
    9. Desarrollo de aplicación interactiva.
    """)

with st.expander("⚠️ 9. Limitaciones"):
    st.warning("""
    El modelo no predice delitos individuales. Estima tasas agregadas a nivel territorial.
    Además, la predicción futura depende de la disponibilidad de variables exógenas
    y de los supuestos definidos en los escenarios.
    """)

with st.expander("🧠 10. Uso responsable"):
    st.write("""
    La aplicación debe entenderse como una herramienta analítica y exploratoria. 
    Sus resultados no deben utilizarse como base única para decisiones operativas, 
    policiales o judiciales.
    """)

with st.expander("📚 11. Referencias principales"):
    st.markdown("""
    - Ministerio de Seguridad de la Nación. Estadísticas criminales.
    - Instituto Nacional de Estadística y Censos (INDEC).
    - Datos Argentina. API GeoRef.
    - Breiman, L. (2001). Random forests.
    - Wooldridge, J. (2010). Econometric Analysis of Cross Section and Panel Data.
    """)