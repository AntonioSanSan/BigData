from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
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

    y_pred = model.predict(X)
    model_score = r2_score(y, y_pred)

    future_days = np.array([[day] for day in range(X['day'].max() + 1, X['day'].max() + 8)])
    predictions = model.predict(future_days)

    return future_days.flatten(), predictions, model_score, grouped
