# Construcción del Dataset de Delitos en Argentina

## 1. Fuentes de datos

Se utilizaron las siguientes fuentes:

- Dataset de delitos del SNIC (Sistema Nacional de Información Criminal)
- Base geográfica de departamentos (Redatam / INDEC)
- Base de población por departamento (Censo 2022)

---

## 2. Construcción del dataset de delitos

Se partió de un dataset a nivel departamento-año que contiene múltiples tipos de delitos.

Se realizó:

- Filtrado de delitos contra la propiedad
- Agregación por:
  - provincia
  - departamento
  - año

---

## 3. Limpieza y normalización

Se aplicaron los siguientes pasos:

- Conversión a minúsculas
- Eliminación de tildes (normalización Unicode)
- Eliminación de espacios redundantes
- Creación de claves:
  - `provincia_key`
  - `departamento_key`

Esto permitió realizar el matching entre datasets heterogéneos.

---

## 4. Integración geográfica

Se integró el dataset de delitos con la base geográfica mediante:

- Matching por provincia y departamento normalizados
- Uso de técnicas de fuzzy matching (difflib)
- Correcciones manuales en casos específicos

---

## 5. Casos no reconciliados

Se identificaron casos sin correspondencia:

- "Departamento sin determinar"
- Regiones administrativas de La Pampa:
  - Centro (Santa Rosa)
  - Norte (General Pico)
  - Oeste (25 de Mayo)
  - Sur (General Acha)

### Decisión metodológica

Estos casos:

- Se conservaron en el dataset de delitos reales
- Se excluyeron del dataset de tasas por falta de correspondencia geográfica válida

---

## 6. Integración de población

Se incorporó la población del Censo 2022 por departamento.

### Nota metodológica

Se utilizó población fija (2022) para todos los años, lo que introduce una aproximación en las tasas.

---

## 7. Construcción del dataset de tasas

Se calcularon:

- Tasa por 100.000 habitantes:

  tasa = delitos / población * 100000

- Tasa porcentual:

  tasa = delitos / población * 100

---

## 8. Datasets finales

### A. Dataset de delitos reales

Ruta:data/processed/delitos_propiedad_departamento_anual_tasas.csv


Contiene:
- Solo departamentos con correspondencia geográfica válida
- Población asociada
- Tasas calculadas

---

## 9. Limitaciones

- Uso de población fija (2022) para todos los años
- Diferencias en nomenclatura geográfica entre fuentes
- Exclusión de algunos casos no reconciliables

---

## 10. Resultado

Se obtuvo un dataset consistente y apto para:

- análisis exploratorio
- comparación territorial
- modelado predictivo