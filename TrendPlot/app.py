import dash
from dash import dcc, html
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Fetch historical stock price data
def fetch_stock_data(symbol):
    data = yf.download(symbol, start='2020-01-01', end='2022-01-01')
    return data

# Train a simple linear regression model to predict future prices
def train_model(data):
    X = np.arange(len(data)).reshape(-1, 1)
    y = data['Close']

    model = LinearRegression()
    model.fit(X, y)

    return model

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Stock Price Analysis and Prediction Dashboard'),
    dcc.Input(id='input-symbol', type='text', value='AAPL', debounce=True),
    dcc.Graph(id='price-chart'),
])

# Define callback to update the chart based on user input
@app.callback(
    dash.dependencies.Output('price-chart', 'figure'),
    [dash.dependencies.Input('input-symbol', 'value')]
)
def update_chart(symbol):
    data = fetch_stock_data(symbol)
    model = train_model(data)

    # Predict future prices
    future_dates = pd.date_range(start=data.index[-1], periods=30, closed='right')
    future_dates = future_dates[1:]  # Exclude the last date (already in historical data)
    future_indices = np.arange(len(data), len(data) + len(future_dates)).reshape(-1, 1)
    future_prices = model.predict(future_indices)

    # Concatenate historical and future prices
    all_dates = pd.to_datetime(np.concatenate([data.index, future_dates]))
    all_prices = np.concatenate([data['Close'].values, future_prices])

    fig = {
        'data': [
            {'x': all_dates, 'y': all_prices, 'type': 'line', 'name': 'Historical Prices'},
            {'x': future_dates, 'y': future_prices, 'type': 'line', 'name': 'Future Predictions', 'line': {'dash': 'dash'}}
        ],
        'layout': {
            'title': f'Stock Price for {symbol} with Future Predictions',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'}
        }
    }
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
