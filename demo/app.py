import streamlit as st
import pandas as pd
from db_connection import connect_to_mongo
from model_demand_predictor import predict_demand
import plotly.express as px

st.set_page_config(page_title="SmartRetail", layout="wide")

st.title("SmartRetail - Dashboard Avanzado para Retail de Moda")

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

# Filtros globales
st.sidebar.header("Filtros")
location_filter = st.sidebar.selectbox("Ubicación", ["Todas"] + sorted(data["location"].unique()))
category_filter = st.sidebar.selectbox("Categoría", ["Todas"] + sorted(data["category"].unique()))
date_range = st.sidebar.date_input("Rango de fechas", [])

filtered_data = data.copy()
if location_filter != "Todas":
    filtered_data = filtered_data[filtered_data["location"] == location_filter]
if category_filter != "Todas":
    filtered_data = filtered_data[filtered_data["category"] == category_filter]
if date_range and len(date_range) == 2:
    filtered_data["date"] = pd.to_datetime(filtered_data["date"])
    filtered_data = filtered_data[
        (filtered_data["date"] >= pd.to_datetime(date_range[0])) &
        (filtered_data["date"] <= pd.to_datetime(date_range[1]))
    ]

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Tendencias", "Reposición", "Predicción"])

with tab1:
    st.header("Resumen de Ventas")
    st.metric("Total Ventas", int(filtered_data["units_sold"].sum()))
    st.metric("Promedio por Registro", round(filtered_data["units_sold"].mean(), 2))
    st.metric("Productos distintos", filtered_data["product"].nunique())
    st.dataframe(filtered_data)

with tab2:
    st.header("Unidades vendidas por ciudad")
    region_data = filtered_data.groupby("location").agg({"units_sold": "sum"}).reset_index()
    fig = px.bar(region_data, x="location", y="units_sold", title="Ventas por ciudad")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Productos con bajo inventario")
    st.caption("Estos productos necesitan reposición en almacén o tienda.")
    low_stock = filtered_data[filtered_data["inventory"] < 50]
    st.dataframe(low_stock[["product", "location", "inventory"]])
    st.dataframe(low_stock.sort_values(by="inventory"))
    csv = low_stock.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", csv, "bajo_stock.csv", "text/csv")

with tab4:
    st.header("Predicción de Demanda")
    try:
        days, preds, r2, mae, rmse, historic_df = predict_demand(filtered_data)
        pred_df = pd.DataFrame({"Día del año": days, "Demanda estimada": preds})
        fig = px.line(pred_df, x="Día del año", y="Demanda estimada", title="Predicción próxima semana")
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"R²: {r2:.2f} | MAE: {mae:.2f} | RMSE: {rmse:.2f}")
        st.subheader("Histórico de ventas agregadas")
        st.line_chart(historic_df.set_index("day_of_year")["units_sold"])
    except Exception as e:
        st.error(f"No se pudo generar la predicción: {e}")
