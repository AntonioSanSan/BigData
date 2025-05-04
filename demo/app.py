import streamlit as st
import pandas as pd
from db_connection import connect_to_mongo
from model_demand_predictor import predict_demand
import plotly.express as px

st.set_page_config(page_title="SmartRetail Demo", layout="wide")

st.title("SmartRetail - Análisis de Datos para Retail de Moda")

# Conexión con MongoDB
st.info("Conectando con la base de datos...")
try:
    db = connect_to_mongo()
    sales_col = db["sales"]
    data = pd.DataFrame(list(sales_col.find()))
    data.drop(columns=["_id"], inplace=True, errors="ignore")
except Exception as e:
    st.error(f"Error al conectar con MongoDB: {e}")
    st.stop()

if data.empty:
    st.warning("No se encontraron datos en la base de datos.")
    st.stop()

# Filtros
st.sidebar.header("Filtros")
unique_locations = data["location"].unique().tolist()
unique_categories = data["category"].unique().tolist()

selected_location = st.sidebar.selectbox("Selecciona ubicación", ["Todas"] + unique_locations)
selected_category = st.sidebar.selectbox("Selecciona categoría", ["Todas"] + unique_categories)
date_range = st.sidebar.date_input("Rango de fechas", [])

# Aplicar filtros
if selected_location != "Todas":
    data = data[data["location"] == selected_location]
if selected_category != "Todas":
    data = data[data["category"] == selected_category]
if date_range and len(date_range) == 2:
    data["date"] = pd.to_datetime(data["date"])
    data = data[(data["date"] >= pd.to_datetime(date_range[0])) & (data["date"] <= pd.to_datetime(date_range[1]))]

st.sidebar.title("Opciones de análisis")
option = st.sidebar.radio("Selecciona análisis", ["Resumen de ventas", "Tendencias por región", "Reposición de inventario", "Predicción de demanda"])

if option == "Resumen de ventas":
    st.subheader("Resumen general")
    st.write(data.describe(include="all"))
    st.dataframe(data)

elif option == "Tendencias por región":
    st.subheader("Unidades vendidas por ciudad")
    region_data = data.groupby("location").agg({"units_sold": "sum"}).reset_index()
    fig = px.bar(region_data, x="location", y="units_sold", title="Unidades vendidas por ciudad")
    st.plotly_chart(fig)

elif option == "Reposición de inventario":
    st.subheader("Productos con bajo inventario (< 50 unidades)")
    low_stock = data[data["inventory"] < 50]
    st.dataframe(low_stock[["product", "location", "inventory"]])
    csv = low_stock.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar CSV", csv, "bajo_stock.csv", "text/csv")

elif option == "Predicción de demanda":
    st.subheader("Predicción de demanda (siguiente semana)")
    try:
        days, preds, model_score, historic_df = predict_demand(data)
        pred_df = pd.DataFrame({"Día del año": days, "Demanda estimada": preds})
        fig = px.line(pred_df, x="Día del año", y="Demanda estimada", title="Predicción de unidades vendidas")
        st.plotly_chart(fig)
        st.success(f"Precisión del modelo (R²): {model_score:.2f}")
        st.subheader("Histórico de ventas agregadas")
        st.line_chart(historic_df.set_index("day")["units_sold"])
    except Exception as e:
        st.error(f"No se pudo generar la predicción: {e}")
