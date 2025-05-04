from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pandas as pd
import numpy as np
import math

def predict_demand(df):
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df['date'].dt.dayofyear
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.weekday

    # Codificación simple de variables categóricas
    df['location'] = df['location'].astype("category").cat.codes
    df['category'] = df['category'].astype("category").cat.codes

    grouped = df.groupby(['day_of_year', 'location', 'category', 'month', 'weekday']).agg({
        'units_sold': 'sum'
    }).reset_index()

    features = ['day_of_year', 'location', 'category', 'month', 'weekday']
    X = grouped[features]
    y = grouped['units_sold']

    model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=1, max_features='sqrt')
    model.fit(X, y)

    # Predicción para los próximos 7 días
    last_day = df['day_of_year'].max()
    future_days = np.array([
        [last_day + i, 0, 0, ((df['month'].max()+1+i)//12)%12 or 1, (df['weekday'].max()+i)%7]
        for i in range(1, 8)
    ])
    preds = model.predict(future_days)

    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    rmse = math.sqrt(mean_squared_error(y, y_pred))

    return future_days[:, 0], preds, r2, mae, rmse, grouped
