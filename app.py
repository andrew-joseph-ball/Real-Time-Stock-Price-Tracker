from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from stock_data import get_stock_price, get_historical_stock_data, plot_stock_trend
import threading
import time
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)
socketio = SocketIO(app)

tracked_stocks = ['AAPL', 'GOOGL', 'MSFT']  

@app.route('/')
def index():
    initial_prices = {ticker: get_stock_price(ticker) for ticker in tracked_stocks}
    return render_template('index.html', prices=initial_prices)

@app.route('/plot/<ticker>')
def plot_stock(ticker):
    stock_data = get_historical_stock_data(ticker, period='5d', interval='1h')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=ticker))


    fig.update_layout(
        title=f'{ticker} Stock Price Over Time',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark'
    )

    graph_html = pio.to_html(fig, full_html=False)

    return render_template('plot.html', ticker=ticker, graph_html=graph_html)


@app.route('/get_initial_prices')
def get_initial_prices():
    prices = {ticker: get_stock_price(ticker) for ticker in tracked_stocks}
    return jsonify(prices)

def stock_price_tracker():
    while True:
        stock_prices = {ticker: get_stock_price(ticker) for ticker in tracked_stocks}
        print(f"Emitting stock prices: {stock_prices}")
        socketio.emit('stock_price_update', stock_prices, broadcast=True)
        time.sleep(60)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    thread = threading.Thread(target=stock_price_tracker)
    thread.daemon = True
    thread.start()

    socketio.run(app, debug=True)
