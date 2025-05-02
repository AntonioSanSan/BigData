from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def predict_demand(df):
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.dayofyear
    grouped = df.groupby('day').agg({'units_sold': 'sum'}).reset_index()

    X = grouped[['day']]
    y = grouped['units_sold']

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.array([[day] for day in range(X['day'].max() + 1, X['day'].max() + 8)])
    predictions = model.predict(future_days)

    return future_days.flatten(), predictions