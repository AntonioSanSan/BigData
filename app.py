import streamlit as st
import pandas as pd
from db_connection import connect_to_mongo
from model_demand_predictor import predict_demand
import plotly.express as px

db = connect_to_mongo()
sales_col = db["sales"]

st.title("🛍️ SmartRetail - Demo Big Data")

# Load data
data = pd.DataFrame(list(sales_col.find()))

st.sidebar.title("Opciones de análisis")
option = st.sidebar.radio("Selecciona análisis", ["Tendencias por región", "Reposición de inventario", "Predicción de demanda"])

if option == "Tendencias por región":
    region_data = data.groupby("location").agg({"units_sold": "sum"}).reset_index()
    fig = px.bar(region_data, x="location", y="units_sold", title="Unidades vendidas por ciudad")
    st.plotly_chart(fig)

elif option == "Reposición de inventario":
    low_stock = data[data["inventory"] < 50]
    st.subheader("Productos con bajo inventario")
    st.dataframe(low_stock[["product", "location", "inventory"]])

elif option == "Predicción de demanda":
    st.subheader("Demanda prevista (siguiente semana)")
    days, preds = predict_demand(data)
    pred_df = pd.DataFrame({"Día del año": days, "Demanda estimada": preds})
    fig = px.line(pred_df, x="Día del año", y="Demanda estimada", title="Predicción de unidades vendidas")
    st.plotly_chart(fig)