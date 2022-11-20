import yfinance as yf
import plotly.graph_objs as go

# the name of the stock
tickers = ['INTC']
# ticks to buy
buy_threshold = 3
# ticks to sell
sell_threshold = 1
# percentage profit target
profit_target = 0.007
choice = tickers[0]

url = "https://www.earningswhispers.com/calendar?sb=p&d=0&t=all&v=t"
buy_price = -1
sell_price = 0
global_counter = 0
decrease_counter = 0
increase_counter = 0
correct_counter = 0
incorrect_counter = 0
prev = -1
period = '60d'
interval = '5m'

data = yf.download(tickers=tickers, period=period, interval=interval, rounding=True)
period = int(period[0])
if(interval.__sizeof__()) > 51:
    interval = int(interval[0] + interval[1])
else:
    interval = int(interval[0])
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

    if global_counter == 0:
        global_counter += 1
        prev = price
        continue
    if price < prev:
        if increase_counter >= sell_threshold:
            # print(stored_datetime[global_counter], "buy command was incorrect")
            incorrect_counter += 1
        increase_counter = 0
        decrease_counter += 1
    if price > prev:
        if decrease_counter >= buy_threshold:
            # print(stored_datetime[global_counter], "sell command was incorrect")
            incorrect_counter += 1
        increase_counter += 1
        decrease_counter = 0

    if decrease_counter == buy_threshold:
        print(stored_datetime[global_counter], "Stock is going down, buy!")
        buy_price = price

    if price >= buy_price * (1 + profit_target) and buy_price != -1:
        print(stored_datetime[global_counter], "Stock is going down, sell!")
        sell_price = price
        print("buy price was: ", buy_price, " sell price was: ", sell_price, " profit is: "
              , (sell_price - buy_price) / buy_price * 100, "%")
    if increase_counter > buy_threshold:
        # print(stored_datetime[global_counter], "buy command was correct")
        correct_counter += 1

    if decrease_counter > sell_threshold:
        # print(stored_datetime[global_counter], "sell command was correct")
        correct_counter += 1

    global_counter += 1

# print("correct_counter == ", correct_counter)
# print("incorrect_counter == ", incorrect_counter)
