import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import StockPrice
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot


engine = create_engine('sqlite:///stock.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period='1d', interval='1m') 
    current_price = stock_info['Close'].iloc[-1]
    
    stock_entry = StockPrice(ticker=ticker, price=current_price, timestamp=datetime.now())
    session.add(stock_entry)
    session.commit()

    return current_price

def get_historical_stock_data(ticker, period='1d', interval='1m'):
    stock = yf.Ticker(ticker)
    # Fetch historical data for the specified period and interval
    stock_data = stock.history(period=period, interval=interval)
    return stock_data 


def plot_stock_trend(ticker, period='1d'):
    stock_history = get_historical_stock_data(ticker, period)
    
    fig = go.Figure([go.Scatter(x=stock_history.index, y=stock_history['Close'], mode='lines', name='Stock Price')])
    fig.update_layout(title=f'{ticker} Stock Price Trend', xaxis_title='Time', yaxis_title='Price')

    return plot(fig, output_type='div')
