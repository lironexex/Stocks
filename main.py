import yfinance as yf
import plotly.graph_objs as go

tickers = ['INTC']
threshold = 3
choice = tickers[0]

url = "https://www.earningswhispers.com/calendar?sb=p&d=0&t=all&v=t"
buy_price = 0
sell_price = 0
global_counter = 0
decrease_counter = 0
increase_counter = 0
correct_counter = 0
incorrect_counter = 0
prev = -1
period = '60d'
interval = '15m'

data = yf.download(tickers=tickers, period=period, interval=interval, rounding=True)
period = int(period[0])
interval = int(interval[0] + interval[1])
# print(period, interval)

# print(data)

fig = go.Figure()

fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                             name='market data'))
fig.update_layout(title=choice + 'share price', yaxis_title='Stock Price (USD)')
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label='15m', step="minute", stepmode="backward"),
            dict(count=45, label='45m', step="minute", stepmode="backward"),
            dict(count=1, label='1h', step="hour", stepmode="backward"),
            dict(count=6, label='6h', step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)
# fig.show()

stored_datetime = data.index
# print(stored_datetime)

print(data['Close'])

for price in data['Close']:
    # print(price)

    if prev == -1:
        prev = price
        continue
    if price < prev:
        if increase_counter >= threshold:
            # print(stored_datetime[global_counter], "buy command was incorrect")
            incorrect_counter += 1
        increase_counter = 0
        decrease_counter += 1
    if price > prev:
        if decrease_counter >= threshold:
            # print(stored_datetime[global_counter], "sell command was incorrect")
            incorrect_counter += 1
        increase_counter += 1
        decrease_counter = 0

    if increase_counter == threshold:
        print(stored_datetime[global_counter], "Stock is going up, buy!")
        buy_price = price

    if decrease_counter == threshold:
        print(stored_datetime[global_counter], "Stock is going down, sell!")
        sell_price = price
        print("buy price was: ", buy_price, " sell price was: ", sell_price, " profit is: "
              , (sell_price-buy_price) / buy_price * 100, "%")
    if increase_counter > threshold:
        # print(stored_datetime[global_counter], "buy command was correct")
        correct_counter += 1

    if decrease_counter > threshold:
        # print(stored_datetime[global_counter], "sell command was correct")
        correct_counter += 1

    global_counter += 1

# print("correct_counter == ", correct_counter)
# print("incorrect_counter == ", incorrect_counter)
