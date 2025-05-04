# BigData

Desarrollado por:

* Jorge Burgos Ortega
* Antonio Sánchez Sánchez

Universidad de Castilla-La Mancha (UCLM)
Curso 2024/2025 – Asignatura: Bases de Datos Avanzadas

## SmartRetail - Dashboard Avanzado para Retail de Moda

SmartRetail es una aplicación interactiva de análisis Big Data diseñada para mejorar la toma de decisiones en el sector minorista de moda. Permite analizar ventas, gestionar inventario y predecir demanda, todo sobre una base de datos NoSQL (MongoDB) y con visualización en tiempo real vía Streamlit.

## Funcionalidades

* **Dashboard interactivo** con métricas clave, resumen de ventas y filtros dinámicos.
* **Tendencias por ciudad** y **por tipo de producto**.
* **Detección automática de productos con bajo inventario**.
* **Predicción de demanda para los próximos 7 días** mediante Machine Learning.
* Visualización del histórico de ventas + métricas del modelo (R², MAE, RMSE).
* Exportación de productos en riesgo como CSV.

## Tecnologías utilizadas

* **Python** + **Streamlit**
* **MongoDB** (NoSQL)
* **Scikit-learn** (RandomForest)
* **Plotly** (gráficas interactivas)
* **Pandas, Numpy**

## Requisitos

* Python 3.8+
* MongoDB (local)
* Instalar dependencias:

```bash
pip install -r requirements.txt
````

## Ejecución

1. Inicia MongoDB localmente.
2. Carga los datos:

```bash
python populate.py
```

> Asegúrate de que el archivo `seed_data.json` esté en la misma carpeta del script.

3. Lanza la demo:

```bash
streamlit run app.py
```

## Visualizaciones principales

### Dashboard

* Total ventas, promedio por registro, productos únicos

### Tendencias

* Ventas por ciudad (barras)
* Ventas por categoría en cada ciudad (barras agrupadas)

### Reposición

* Productos con inventario < 50 unidades
* Exportación en CSV

### Predicción

* Gráfico de demanda para 7 días futuros
* Métricas de precisión del modelo
* Histórico de ventas agregadas

## 🧪 Dataset

El archivo `seed_data.json` contiene más de 5.000 registros simulados realistas. Incluye productos, ciudades, fechas, inventario y unidades vendidas.
