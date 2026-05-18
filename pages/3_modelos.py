import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(layout="wide")

st.caption("Proyecto de análisis y modelado de delitos - Argentina (2017–2024)")

st.title("🤖 Modelos predictivos")

st.write("""
Esta sección compara los modelos entrenados para estimar la tasa de delitos contra la propiedad,
incorporando Regresión Lineal, Efectos Fijos, Random Forest y XGBoost. Además, incluye explicabilidad
con SHAP y validación temporal mediante rolling/expanding window.
""")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Comparación",
    "🧠 Explicabilidad",
    "⏳ Robustez",
    "⚠️ Sensibilidad"
])

# =========================
# CARGA DE ARTEFACTOS
# =========================
@st.cache_data
def cargar_metricas():
    metricas = pd.read_csv("models/metricas_modelos.csv")

    # Normalizar nombre de columna R2
    if "R2" in metricas.columns:
        metricas = metricas.rename(columns={"R2": "R²"})

    return metricas


@st.cache_data
def cargar_importancias():
    imp_rf = pd.read_csv("models/importancias_rf.csv")
    imp_xgb = pd.read_csv("models/importancias_xgb.csv")

    imp_rf = imp_rf.rename(columns={"variable": "Variable", "importancia": "Importancia"})
    imp_xgb = imp_xgb.rename(columns={"variable": "Variable", "importancia": "Importancia"})

    return imp_rf, imp_xgb


@st.cache_data
def cargar_rolling():
    return pd.read_csv("models/rolling_temporal_resultados.csv")

@st.cache_data
def cargar_robustez_temporal():
    return pd.read_csv("models/robustez_temporal_resumen.csv")


@st.cache_data
def cargar_robustez_lag():
    return pd.read_csv("models/robustez_lag_comparacion.csv")


@st.cache_resource
def cargar_shap():
    modelo_ganador_nombre = joblib.load("models/modelo_ganador_nombre.pkl")
    X_shap = joblib.load("models/X_shap_sample.pkl")
    shap_values = joblib.load("models/shap_values.pkl")
    return modelo_ganador_nombre, X_shap, shap_values


with st.spinner("Cargando métricas y artefactos del modelo..."):
    metricas = cargar_metricas()
    imp_rf, imp_xgb = cargar_importancias()
    robustez_temporal = cargar_robustez_temporal()
    robustez_lag = cargar_robustez_lag()

# =========================
# COMPARACIÓN DE MODELOS
# =========================

with tab1:
    st.markdown("### Comparación de modelos")

    mejor_mae = metricas.loc[metricas["MAE"].idxmin()]
    mejor_rmse = metricas.loc[metricas["RMSE"].idxmin()]
    mejor_r2 = metricas.loc[metricas["R²"].idxmax()]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Menor MAE", f"{mejor_mae['MAE']:,.2f}", mejor_mae["Modelo"])

    with col2:
        st.metric("Menor RMSE", f"{mejor_rmse['RMSE']:,.2f}", mejor_rmse["Modelo"])

    with col3:
        st.metric("Mayor R²", f"{mejor_r2['R²']:,.3f}", mejor_r2["Modelo"])

    st.dataframe(metricas, width="stretch")

    fig_metricas = make_subplots(specs=[[{"secondary_y": True}]])

    fig_metricas.add_trace(
        go.Bar(
            x=metricas["Modelo"],
            y=metricas["MAE"],
            name="MAE",
            text=metricas["MAE"].round(2),
            textposition="outside"
        ),
        secondary_y=False
    )

    fig_metricas.add_trace(
        go.Bar(
            x=metricas["Modelo"],
            y=metricas["RMSE"],
            name="RMSE",
            text=metricas["RMSE"].round(2),
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
            text=metricas["R²"].round(3),
            textposition="top center",
            line=dict(width=3)
        ),
        secondary_y=True
    )

    fig_metricas.update_layout(
        template="plotly_dark",
        title="Comparación general de desempeño de modelos",
        title_x=0.5,
        barmode="group",
        xaxis_title="Modelo",
        legend_title="Métrica",
        margin=dict(l=20, r=20, t=70, b=60),
        hovermode="x unified"
    )

    fig_metricas.update_yaxes(title_text="MAE / RMSE", secondary_y=False)
    fig_metricas.update_yaxes(title_text="R²", range=[0, 1], secondary_y=True)

    st.plotly_chart(fig_metricas, width="stretch")

    st.info("""
    MAE y RMSE se expresan en unidades de tasa cada 100.000 habitantes.
    R² se representa con eje secundario porque su escala va de 0 a 1.
    """)

    # =========================
    # INTERPRETACIÓN
    # =========================
    st.markdown("### Interpretación general")

    st.markdown(f"""
    - El modelo con menor **MAE** fue **{mejor_mae['Modelo']}**.
    - El modelo con menor **RMSE** fue **{mejor_rmse['Modelo']}**.
    - El modelo con mayor **R²** fue **{mejor_r2['Modelo']}**.
    - La comparación permite evaluar no solo precisión, sino también estabilidad y capacidad explicativa.
    """)

    # =========================
    # IMPORTANCIA DE VARIABLES
    # =========================

    with tab2:
        st.markdown("---")
        st.markdown("### Importancia de variables")

        modelo_importancia = st.selectbox(
            "Seleccionar modelo",
            ["Random Forest", "XGBoost"]
        )

        if modelo_importancia == "Random Forest":
            importancias = imp_rf.copy()
        else:
            importancias = imp_xgb.copy()

        importancias_top = (
            importancias
            .sort_values(by="Importancia", ascending=False)
            .head(10)
            .sort_values(by="Importancia", ascending=True)
        )

        fig_imp = px.bar(
            importancias_top,
            x="Importancia",
            y="Variable",
            orientation="h",
            text="Importancia",
            title=f"Top 10 variables más importantes - {modelo_importancia}"
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
        La importancia de variables permite identificar qué predictores aportan más al modelo.
        En este proyecto, la persistencia temporal representada por `tasa_lag1` suele tener un peso dominante.
        """)

        # =========================
        # SHAP
        # =========================
        st.markdown("---")
        st.markdown("### Explicabilidad con SHAP")

        st.write("""
        SHAP permite interpretar el aporte promedio de cada variable al modelo ganador.
        A diferencia de la importancia tradicional, SHAP estima cuánto contribuye cada variable
        a mover la predicción respecto del valor esperado del modelo.
        """)

        try:
            modelo_ganador_nombre, X_shap, shap_values = cargar_shap()

            st.info(f"Modelo explicado con SHAP: **{modelo_ganador_nombre}**")

            shap_array = np.array(shap_values)

            if shap_array.ndim == 3:
                shap_array = shap_array[:, :, 0]

            shap_importance = pd.DataFrame({
                "Variable": X_shap.columns,
                "SHAP medio absoluto": np.abs(shap_array).mean(axis=0)
            }).sort_values(by="SHAP medio absoluto", ascending=False)

            fig_shap = px.bar(
                shap_importance.head(10).sort_values(by="SHAP medio absoluto", ascending=True),
                x="SHAP medio absoluto",
                y="Variable",
                orientation="h",
                text="SHAP medio absoluto",
                title=f"Importancia SHAP - {modelo_ganador_nombre}"
            )

            fig_shap.update_traces(
                texttemplate="%{text:.3f}",
                textposition="outside"
            )

            fig_shap.update_layout(
                template="plotly_dark",
                title_x=0.5,
                xaxis_title="Impacto medio absoluto sobre la predicción",
                yaxis_title="Variable",
                margin=dict(l=20, r=20, t=70, b=40)
            )

            st.plotly_chart(fig_shap, width="stretch")

        except Exception as e:
            st.warning("No se pudieron cargar los artefactos SHAP. Verificá que existan los archivos guardados en /models.")
            st.exception(e)

    # =========================
    # VALIDACIÓN TEMPORAL
    # =========================

    with tab3:
        st.markdown("---")
        st.markdown("### Validación temporal")

        st.write("""
        La validación temporal permite evaluar la estabilidad del desempeño respetando el orden cronológico.
        Esto evita entrenar con información futura para predecir años anteriores.
        """)

        try:
            rolling = cargar_rolling()

            st.dataframe(rolling, width="stretch")

            metrica_rolling = st.selectbox(
                "Métrica temporal",
                ["MAE", "RMSE", "R2"] if "R2" in rolling.columns else ["MAE", "RMSE", "R²"]
            )

            fig_rolling = px.line(
                rolling,
                x="anio_test",
                y=metrica_rolling,
                color="modelo",
                markers=True,
                title=f"Validación temporal - {metrica_rolling}"
            )

            fig_rolling.update_layout(
                template="plotly_dark",
                title_x=0.5,
                xaxis_title="Año evaluado",
                yaxis_title=metrica_rolling,
                hovermode="x unified",
                legend_title="Modelo"
            )

            st.plotly_chart(fig_rolling, width="stretch")

            st.info("""
            Si las métricas se mantienen relativamente estables entre años, el modelo muestra mejor robustez temporal.
            Si varían demasiado, puede existir sensibilidad al período evaluado.
            """)

        except Exception as e:
            st.warning("No se pudo cargar la validación temporal. Verificá que exista rolling_temporal_resultados.csv.")
            st.exception(e)

        # =========================
        # ROBUSTEZ TEMPORAL
        # =========================
        st.markdown("---")
        st.markdown("### Robustez temporal")

        st.write("""
        Esta sección resume la estabilidad del desempeño de los modelos a través de los años evaluados.
        La desviación estándar permite observar qué tan variable fue el error entre períodos.
        """)

        try:
            st.dataframe(robustez_temporal, width="stretch")

            fig_robustez = px.bar(
                robustez_temporal,
                x="modelo",
                y="RMSE_mean",
                error_y="RMSE_std",
                text="RMSE_mean",
                title="Robustez temporal — RMSE promedio y variabilidad"
            )

            fig_robustez.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside"
            )

            fig_robustez.update_layout(
                template="plotly_dark",
                title_x=0.5,
                xaxis_title="Modelo",
                yaxis_title="RMSE promedio",
                showlegend=False
            )

            st.plotly_chart(fig_robustez, width="stretch")

            st.info("""
            Random Forest presenta menor RMSE promedio, mientras que XGBoost muestra menor variabilidad temporal.
            Esto permite analizar el equilibrio entre precisión promedio y estabilidad entre años.
            """)

        except Exception as e:
            st.warning("No se pudo mostrar la robustez temporal.")
            st.exception(e)

    # =========================
    # SENSIBILIDAD A tasa_lag1
    # =========================

    with tab4:
        st.markdown("---")
        st.markdown("### Sensibilidad a variables temporales")

        st.write("""
        Para evaluar la dependencia temporal del fenómeno, se entrenaron nuevamente los modelos
        eliminando la variable `tasa_lag1`.

        Esto permite analizar cuánto depende la capacidad predictiva de la persistencia histórica del delito.
        """)

        try:
            st.dataframe(robustez_lag, width="stretch")

            fig_lag = px.bar(
                robustez_lag,
                x="Modelo",
                y="R2",
                color="Escenario",
                barmode="group",
                text="R2",
                title="Impacto de eliminar tasa_lag1 sobre el desempeño"
            )

            fig_lag.update_traces(
                texttemplate="%{text:.3f}",
                textposition="outside"
            )

            fig_lag.update_layout(
                template="plotly_dark",
                title_x=0.5,
                xaxis_title="Modelo",
                yaxis_title="R²",
                legend_title="Escenario"
            )

            st.plotly_chart(fig_lag, width="stretch")

            st.warning("""
            La fuerte caída del R² al eliminar `tasa_lag1` evidencia una alta persistencia temporal
            en los delitos contra la propiedad.

            Esto sugiere que las tasas históricas contienen una parte importante de la señal predictiva.
            """)

        except Exception as e:
            st.warning("No se pudo mostrar el análisis de sensibilidad temporal.")
            st.exception(e)

# =========================
# INTERPRETACIÓN
# =========================

modelo_ganador = mejor_r2["Modelo"]

if modelo_ganador == "XGBoost":

    st.success(f"""
    El modelo con mejor desempeño general fue **{modelo_ganador}**.

    XGBoost logró el mayor R² y los menores errores promedio,
    mostrando buena capacidad para capturar relaciones no lineales complejas.

    Además, presentó un comportamiento temporal relativamente estable
    durante la validación rolling/expanding.
    """)

elif modelo_ganador == "Random Forest":

    st.success(f"""
    El modelo con mejor desempeño general fue **{modelo_ganador}**.

    Random Forest obtuvo las mejores métricas promedio,
    mostrando alta capacidad predictiva y robustez general.

    El modelo evidenció una fuerte dependencia temporal asociada a `tasa_lag1`,
    lo que sugiere persistencia estructural del fenómeno.
    """)

else:

    st.info(f"""
    El modelo con mejor desempeño fue **{modelo_ganador}**.
    """)

st.markdown("""
### Hallazgos metodológicos

- La persistencia temporal tiene un peso dominante.
- Las variables socioeconómicas aportan señal complementaria.
- XGBoost y Random Forest muestran mejor desempeño que modelos lineales.
- La validación temporal permitió evaluar estabilidad entre períodos.
- SHAP permitió interpretar el impacto promedio de las variables.
""")