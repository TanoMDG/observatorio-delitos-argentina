import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.caption("Proyecto de análisis y modelado de delitos - Argentina (2017–2024)")

st.title("📚 Metodología")

st.info(
    "Esta sección resume el proceso metodológico utilizado para construir, analizar, "
    "modelar e interpretar el dataset de delitos contra la propiedad en Argentina."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unidad de análisis", "Departamento–año")

with col2:
    st.metric("Período", "2017–2024")

with col3:
    st.metric("Modelo principal", "XGBoost")

st.markdown("---")

with st.expander("🎯 1. Objetivo del proyecto", expanded=True):
    st.write("""
    Analizar la distribución territorial y la evolución temporal de los delitos contra 
    la propiedad en Argentina, incorporando variables socioeconómicas, modelos predictivos 
    e interpretabilidad para enriquecer la comprensión del fenómeno.
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
    Se implementaron cuatro enfoques complementarios para comparar interpretabilidad,
    control territorial, capacidad predictiva y estabilidad temporal.
    """)
    
    st.markdown("""
    - **Regresión Lineal:** modelo baseline interpretable.
    - **Efectos Fijos:** captura heterogeneidad territorial.
    - **Random Forest:** modelo no lineal basado en árboles.
    - **XGBoost:** modelo de boosting secuencial con mejor desempeño global.
    """)

with st.expander("📈 7. Resultados"):
    st.success("""
    XGBoost obtuvo el mejor desempeño global del proyecto, alcanzando
    un MAE aproximado de 266, un RMSE cercano a 380 y un R² de 0.900.

    Random Forest presentó resultados muy similares, con un R² aproximado de 0.897,
    mientras que los modelos lineales mostraron menor capacidad predictiva.
    """)

    metricas = pd.DataFrame({
        "Modelo": [
            "Regresión Lineal",
            "Efectos Fijos",
            "Random Forest",
            "XGBoost"
        ],
        "MAE": [453.93, 377.60, 269.36, 266.08],
        "RMSE": [559.61, 496.36, 386.05, 380.44],
        "R²": [0.784, 0.833, 0.897, 0.900]
    })

    st.dataframe(metricas, width="stretch")
    
    st.write("""
    La comparación confirma que los modelos basados en árboles capturan mejor las relaciones
    no lineales e interacciones complejas presentes en el fenómeno.
    """)

with st.expander("🔍 8. Interpretabilidad (SHAP)"):
    st.write("""
    Para interpretar el comportamiento del modelo ganador se utilizó
    **SHAP (SHapley Additive exPlanations)**, una metodología basada en
    teoría de juegos que permite cuantificar el aporte de cada variable
    sobre las predicciones.
    """)

    st.markdown("""
    - `tasa_lag1` es el predictor dominante.
    - `variacion_anual_cbt` aporta información complementaria.
    - `variacion_anual_salarios_pct` contribuye moderadamente.
    - `log_densidad` mantiene relevancia estructural.
    - Las restantes variables presentan impactos reducidos.
    """)

with st.expander("⏳ 9. Validación temporal"):
    st.write("""
    Se implementó una estrategia **rolling / expanding window**, donde los modelos
    fueron entrenados utilizando únicamente información disponible hasta cada período
    de evaluación.
    """)

    st.markdown("""
    - estabilidad temporal del desempeño,
    - capacidad de generalización fuera de muestra,
    - consistencia entre Random Forest y XGBoost,
    - mejora gradual al incorporar más información histórica.
    """)

with st.expander("🛡️ 10. Análisis de robustez"):
    st.write("""
    Se evaluó la sensibilidad de los modelos eliminando la variable `tasa_lag1`,
    que representa la persistencia temporal del fenómeno.
    """)

    robustez = pd.DataFrame({
        "Modelo": [
            "Random Forest",
            "Random Forest",
            "XGBoost",
            "XGBoost"
        ],
        "Escenario": [
            "Con tasa_lag1",
            "Sin tasa_lag1",
            "Con tasa_lag1",
            "Sin tasa_lag1"
        ],
        "R²": [0.897, 0.330, 0.900, 0.442]
    })

    st.dataframe(robustez, width="stretch")

    st.info("""
    La fuerte caída del desempeño al eliminar `tasa_lag1` confirma que la persistencia
    temporal constituye el principal determinante de los delitos contra la propiedad.
    """)

with st.expander("🔁 11. Flujo metodológico"):
    st.markdown("""
    1. Comprensión del problema.
    2. Recolección de fuentes oficiales.
    3. Limpieza y normalización territorial.
    4. Integración de población, superficie y variables socioeconómicas.
    5. Construcción de tasas comparables.
    6. Feature engineering.
    7. EDA territorial y temporal.
    8. Modelado explicativo y predictivo.
    9. Interpretabilidad con SHAP.
    10. Validación temporal.
    11. Análisis de robustez.
    12. Desarrollo de aplicación interactiva.
    """)

with st.expander("⚠️ 12. Limitaciones"):
    st.warning("""
    El modelo no predice delitos individuales. Estima tasas agregadas a nivel territorial.
    Además, la predicción futura depende de la disponibilidad de variables exógenas,
    de los supuestos definidos en los escenarios y de la persistencia histórica observada.
    """)

with st.expander("🧠 13. Uso responsable"):
    st.write("""
    La aplicación debe entenderse como una herramienta analítica y exploratoria. 
    Sus resultados no deben utilizarse como base única para decisiones operativas, 
    policiales o judiciales.
    """)

with st.expander("📚 14. Referencias principales"):
    st.markdown("""
    - Ministerio de Seguridad de la Nación. Estadísticas criminales.
    - Instituto Nacional de Estadística y Censos (INDEC).
    - Datos Argentina. API GeoRef.
    - Breiman, L. (2001). Random forests.
    - Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system.
    - Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions.
    - Wooldridge, J. (2010). Econometric Analysis of Cross Section and Panel Data.
    """)