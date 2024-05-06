from flask import Flask, render_template, request
import yfinance as yf
from sklearn.linear_model import LinearRegression
import pandas as pd

app = Flask(__name__)

# Fetch historical stock data
def get_stock_data(symbol, period='1y'):
    stock_data = yf.download(symbol, period=period)
    return stock_data

# Simple linear regression model for stock price prediction
def predict_stock_price(symbol, period='1y'):
    stock_data = get_stock_data(symbol, period)
    stock_data['Date'] = pd.to_datetime(stock_data.index)
    stock_data['OrdinalDate'] = stock_data['Date'].apply(lambda date: date.toordinal())
    
    X = stock_data[['OrdinalDate']].values
    y = stock_data['Close'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    last_date = stock_data['OrdinalDate'].iloc[-1]
    next_date = last_date + 1
    next_price = model.predict([[next_date]])
    
    return next_price[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    symbol = request.form['symbol']
    predicted_price = predict_stock_price(symbol)
    return render_template('prediction.html', symbol=symbol, predicted_price=predicted_price)

if __name__ == '__main__':
    app.run(debug=True)
