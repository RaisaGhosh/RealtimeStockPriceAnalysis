import dash
from dash import dcc, html
import yfinance as yf

# Fetch stock price data
def fetch_stock_data(symbol):
    data = yf.download(symbol, start='2020-01-01', end='2022-01-01')
    return data

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Stock Price Analysis Dashboard'),
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
    fig = {
        'data': [
            {'x': data.index, 'y': data['Close'], 'type': 'line', 'name': symbol}
        ],
        'layout': {
            'title': f'Stock Price for {symbol}',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'}
        }
    }
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

