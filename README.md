# 📊 Observatorio de Delitos contra la Propiedad en Argentina

Aplicación interactiva desarrollada en **Python + Streamlit** para el análisis territorial, temporal y predictivo de delitos contra la propiedad en Argentina a nivel **departamento–año**.

El proyecto combina:

- análisis exploratorio de datos (EDA),
- integración de variables socioeconómicas,
- modelado estadístico,
- machine learning,
- visualización geoespacial,
- simulación de escenarios futuros,
- y despliegue web interactivo.

---

# 🌎 Aplicación online

🔗 https://observatorio-delitos-argentina.streamlit.app/

---

# 🎯 Objetivo del proyecto

Analizar la distribución territorial y la evolución temporal de los delitos contra la propiedad en Argentina entre 2017 y 2024, incorporando variables socioeconómicas y modelos predictivos para enriquecer la interpretación del fenómeno.

---

# 🧠 Alcance conceptual

El proyecto NO predice delitos individuales.

El modelo estima:

- tasas agregadas,
- patrones territoriales,
- persistencia temporal,
- y relaciones estadísticas a nivel departamento–año.

La aplicación debe entenderse como una herramienta analítica y exploratoria.

---

# 📦 Tecnologías utilizadas

## Lenguaje principal

- Python 3

## Librerías principales

- pandas
- numpy
- scikit-learn
- statsmodels
- plotly
- folium
- streamlit
- streamlit-folium
- joblib

---

# 🗂️ Estructura del proyecto

```text
Copia_pre_proyecto/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── final/
│
├── models/
│   ├── random_forest.pkl
│   └── features_modelo.pkl
│
├── notebooks/
│   ├── 01_exploracion_delitos.ipynb
│   ├── 02_dataset_final.ipynb
│   ├── 04_procesamiento_indec.ipynb
│   ├── 05_georef_mapas.ipynb
│   ├── 06_eda_delitos_propiedad.ipynb
│   ├── 07_entrega_inicial_pf.ipynb
│   └── 08_modelado.ipynb
│
├── pages/
│   ├── 1_exploracion_territorial.py
│   ├── 2_evolucion_temporal.py
│   ├── 3_modelos.py
│   ├── 4_simulador.py
│   ├── 5_proyeccion.py
│   └── 6_metodologia.py
│
└── dashboard/
```

# 🗃️ Dataset

## Unidad de análisis

- Departamento–año

## Período analizado

- 2017–2024

## Dataset principal

El dataset final utilizado por la aplicación es:

```plaintext
data/final/dataset_mapa_sup_final.csv
```

## Variables principales

### Variables delictivas

- `delitos_propiedad_hechos`
- `tasa_delitos_propiedad_100k_v2`
- `tasa_lag1`
- `tasa_yoy`

### Variables estructurales

- `poblacion_anual`
- `superficie_km2`
- `densidad_poblacion`
- `log_densidad`

### Variables socioeconómicas

- `Indice_IPC`
- `variacion_anual_cbt`
- `variacion_anual_salarios_pct`
- `variacion_empleo_const_pct`
- `variacion_acceso_internet_pct`
- `variacion_anual_ipim`

---

# ⚙️ Feature Engineering

El proyecto incorpora múltiples transformaciones y variables derivadas:

- cálculo de tasas comparables cada 100.000 habitantes,
- normalización de claves territoriales,
- integración de población anual,
- incorporación de superficie departamental,
- cálculo de densidad poblacional,
- transformación logarítmica de densidad,
- construcción de variables rezagadas,
- cálculo de variaciones interanuales,
- integración de fuentes socioeconómicas externas,
- consolidación geográfica para visualización territorial.

## Variable objetivo principal

```python
tasa_delitos_propiedad_100k_v2 = (
    delitos_propiedad_hechos / poblacion_anual
) * 100000
```

---

# 📊 Análisis exploratorio

## Principales hallazgos del EDA

- fuerte persistencia temporal del fenómeno,
- elevada correlación de `tasa_lag1` con la variable objetivo,
- relevancia de `log_densidad` como variable estructural,
- menor peso de variables económicas,
- asociación casi nula del acceso a internet,
- heterogeneidad territorial significativa,
- diferencias claras entre provincias y departamentos.

---

# 🤖 Modelado

Se implementaron cuatro enfoques principales.

## 1. Regresión Lineal

Modelo baseline interpretable para analizar relaciones lineales entre las variables explicativas y la tasa de delitos.

## 2. Modelo de Efectos Fijos

Modelo orientado a capturar heterogeneidad territorial entre departamentos, controlando diferencias estructurales persistentes.

## 3. Random Forest

Modelo no lineal con mejor capacidad predictiva y mayor flexibilidad para capturar relaciones complejas entre variables.

## 4. XGBoost

Modelo de boosting basado en árboles de decisión que optimiza secuencialmente los errores de predicción. Obtuvo el mejor desempeño global del proyecto, superando levemente a Random Forest en las métricas de evaluación.

---

# 📈 Resultados

El modelo con mejor desempeño general fue **XGBoost**.

| Modelo           |    MAE |   RMSE |    R² |
| ---------------- | -----: | -----: | ----: |
| Regresión Lineal | 453.93 | 559.61 | 0.784 |
| Efectos Fijos    | 377.60 | 496.36 | 0.833 |
| Random Forest    | 269.36 | 386.05 | 0.897 |
| XGBoost          | 266.08 | 380.44 | 0.900 |

# 🔍 Interpretabilidad del modelo

Para interpretar el comportamiento del modelo ganador se utilizó SHAP (SHapley Additive exPlanations), una metodología basada en teoría de juegos que permite cuantificar la contribución de cada variable a las predicciones.

Los resultados mostraron que:

- `tasa_lag1` es el predictor dominante.
- Variables socioeconómicas como `variacion_anual_cbt` y `variacion_anual_salarios_pct` aportan información complementaria.
- `log_densidad` conserva relevancia como variable estructural territorial.

El uso de SHAP permitió complementar la capacidad predictiva de XGBoost con un análisis transparente e interpretable.

# ⏳ Validación temporal

Se implementó una estrategia de validación temporal tipo rolling/expanding window.

En cada iteración los modelos fueron entrenados utilizando únicamente información disponible hasta un determinado año y evaluados sobre períodos posteriores.

Los resultados mostraron:

- estabilidad temporal del desempeño,
- capacidad de generalización fuera de muestra,
- consistencia entre Random Forest y XGBoost,
- mejora progresiva a medida que aumenta la información disponible para entrenamiento.

## Interpretación general

Los resultados indican que:

- `tasa_lag1` es la variable más importante del modelo,
- existe una fuerte persistencia temporal del fenómeno,
- `log_densidad` aporta información relevante,
- las variables económicas muestran menor peso relativo,
- Random Forest mejora el desempeño al capturar relaciones no lineales.

# 🛡️ Análisis de robustez

Se realizó una prueba de sensibilidad eliminando la variable `tasa_lag1`.

Resultados:

| Modelo | Escenario | R² |
|----------|----------|----------:|
| Random Forest | Con tasa_lag1 | 0.897 |
| Random Forest | Sin tasa_lag1 | 0.330 |
| XGBoost | Con tasa_lag1 | 0.900 |
| XGBoost | Sin tasa_lag1 | 0.442 |

La fuerte caída del desempeño confirma que la persistencia temporal constituye el principal componente explicativo del fenómeno.

---

# 🧭 Funcionalidades de la aplicación

# 📍 Exploración territorial

Permite:

- filtrar por año,
- filtrar por provincia,
- visualizar ranking de departamentos,
- explorar mapa interactivo,
- consultar popups y tooltips por departamento.

---

# 📈 Evolución temporal

Permite:

- analizar evolución nacional,
- analizar evolución por provincia,
- comparar múltiples provincias,
- observar tendencias anuales.

---

# 🤖 Modelos predictivos

Permite:

- comparar Regresión Lineal, Efectos Fijos, Random Forest y XGBoost,
- visualizar métricas de desempeño,
- analizar importancia de variables,
- interpretar resultados mediante SHAP,
- evaluar estabilidad temporal,
- analizar robustez del modelo.

---

# 🎯 Simulador predictivo

Permite:

- seleccionar año, provincia y departamento,
- estimar tasa esperada con el modelo Random Forest,
- comparar predicción contra valor real observado,
- visualizar variables utilizadas por el modelo.

---

# 🔮 Proyección con escenarios

Permite simular tasas futuras bajo tres escenarios:

- escenario base,
- escenario optimista,
- escenario pesimista.

## La proyección utiliza

- tasa rezagada,
- ajustes socioeconómicos,
- simulación iterativa año a año.

---

# 📚 Metodología

Resume:

- fuentes de datos,
- construcción del dataset,
- feature engineering,
- análisis exploratorio,
- modelado,
- resultados,
- limitaciones,
- uso responsable.

---

# 🌐 Despliegue

La aplicación fue desplegada utilizando:

- GitHub
- Streamlit Cloud

## Link de acceso

```plaintext
https://observatorio-delitos-argentina.streamlit.app/
```

---

# 🚀 Ejecución local

## 1. Clonar repositorio

```bash
git clone https://github.com/TanoMDG/observatorio-delitos-argentina.git
```

## 2. Entrar al proyecto

```bash
cd observatorio-delitos-argentina
```

## 3. Crear entorno virtual

```bash
python -m venv .venv
```

## 4. Activar entorno virtual

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

## 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 6. Ejecutar aplicación

```bash
streamlit run app.py
```

---

# 🏆 Principales aportes

- Construcción de un dataset integrado departamento–año para Argentina.
- Incorporación de variables socioeconómicas y territoriales.
- Comparación de modelos lineales y no lineales.
- Implementación de XGBoost como modelo de mejor desempeño.
- Aplicación de SHAP para interpretabilidad.
- Validación temporal mediante rolling windows.
- Pruebas de robustez eliminando variables rezagadas.
- Desarrollo de una aplicación web interactiva para exploración, simulación y análisis territorial.

# 📌 Consideraciones

- El proyecto tiene fines académicos y analíticos.
- No reemplaza análisis criminológicos especializados.
- Las predicciones dependen de la calidad de los datos.
- Las proyecciones futuras dependen de los supuestos definidos.
- Los resultados deben interpretarse a nivel agregado y territorial.

---

# ⚠️ Uso responsable

Esta aplicación no debe utilizarse para:

- predecir delitos individuales,
- tomar decisiones judiciales,
- tomar decisiones policiales directas,
- clasificar personas o grupos,
- reemplazar análisis institucional especializado.

Debe entenderse como una herramienta de análisis exploratorio y apoyo interpretativo.

---

# 👨‍💻 Autor

**Marcos**

Estudiante de Ciencia de Datos e Inteligencia Artificial.

---

# 📄 Licencia

Proyecto académico con fines educativos y de portfolio.