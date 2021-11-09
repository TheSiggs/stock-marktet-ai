from EMA import exponential_moving_average
from KrakenAPI import KrakenAPI
from datetime import datetime
import time
from termcolor import colored

from evaluateMovement import evaluate_movement

kraken = KrakenAPI()

currency = 'ETHUSD'
pair = 'XETHZUSD'
interval = 1
index = -1
did_price_action = False
last_timestamp = 0

# while True:
#     time.sleep(3)
#     tickers = kraken.get_tickers(currency)
#     tickers = tickers['result'][pair]
#     ticker_data = {
#         'ask': {'price': tickers['a'][0], 'whole lot volume': tickers['a'][1], 'lot volume': tickers['a'][2]},
#         'bid': {'price': tickers['b'][0], 'whole lot volume': tickers['b'][1], 'lot volume': tickers['b'][2]},
#         'last trade': {'price': tickers['c'][0], 'lot volume': tickers['c'][1]},
#         'volume': {'today': tickers['v'][0], 'last 24 hours': tickers['v'][1]},
#         'VWAP': {'today': tickers['p'][0], 'last 24 hours': tickers['p'][1]},
#         'Number of trades': {'today': tickers['t'][0], 'last 24 hours': tickers['t'][1]},
#         'lows': {'today': tickers['l'][0], 'last 24 hours': tickers['l'][1]},
#         'highs': {'today': tickers['h'][0], 'last 24 hours': tickers['h'][1]},
#         'todays opening price': tickers['o']
#     }
#     print(ticker_data)
prev = {}
while True:
    time.sleep(5)
    ohlc = kraken.get_ohlc_data({'pair': currency, 'interval': interval})
    try:
        ohlc = ohlc['result'][pair]
    except KeyError:
        print(ohlc['error'])
    prev_ohlc = {
        'Unix Timestamp': ohlc[-2][0],
        'Readable Time': datetime.utcfromtimestamp(ohlc[-2][0]).strftime('%d-%m-%Y %H:%M:%S'),
        'Open Price': float(ohlc[-2][1]),
        'Close Price': float(ohlc[-2][4]),
        'Highest Price': float(ohlc[-2][2]),
        'Lowest Price': float(ohlc[-2][3]),
        'Volume Weighted Average Price': float(ohlc[-2][5]),
        'Volume Traded': float(ohlc[-2][6]),
        'Count': ohlc[-2][7],
        'Description': 'Bullish' if float(ohlc[-2][4]) >= float(ohlc[-2][1]) else 'Bearish',
        '3 Period EMA': exponential_moving_average([value[4] for value in ohlc[0: -2]],
                                                   [value[0] for value in ohlc[0: -2]], 3),
        '6 Period EMA': exponential_moving_average([value[4] for value in ohlc[0: -2]],
                                                   [value[0] for value in ohlc[0: -2]], 6),
        '9 Period EMA': exponential_moving_average([value[4] for value in ohlc[0: -2]],
                                                   [value[0] for value in ohlc[0: -2]], 9),
    }
    ohlc = {
        'Unix Timestamp': ohlc[-1][0],
        'Readable Time': datetime.utcfromtimestamp(ohlc[-1][0]).strftime('%d-%m-%Y %H:%M:%S'),
        'Open Price': float(ohlc[-1][1]),
        'Close Price': float(ohlc[-1][4]),
        'Highest Price': float(ohlc[-1][2]),
        'Lowest Price': float(ohlc[-1][3]),
        'Volume Weighted Average Price': float(ohlc[-1][5]),
        'Volume Traded': float(ohlc[-1][6]),
        'Count': ohlc[-1][7],
        'Description': 'Bullish' if float(ohlc[-1][4]) > float(ohlc[-1][1]) else 'Bearish',
        '3 Period EMA': exponential_moving_average([value[4] for value in ohlc[0: -1]],
                                                   [value[0] for value in ohlc[0: -1]], 3),
        '6 Period EMA': exponential_moving_average([value[4] for value in ohlc[0: -1]],
                                                   [value[0] for value in ohlc[0: -1]], 6),
        '9 Period EMA': exponential_moving_average([value[4] for value in ohlc[0: -1]],
                                                   [value[0] for value in ohlc[0: -1]], 9),
    }
    if ohlc['Unix Timestamp'] > last_timestamp:
        last_timestamp = ohlc['Unix Timestamp']
        did_price_action = False
    if len(prev) == 0:
        print(ohlc)
        prev = ohlc
    else:
        if ohlc['Count'] != prev['Count']:
            prev = ohlc
            print()
            print(colored(prev_ohlc, 'red' if prev_ohlc['Description'] == 'Bearish' else 'green'))
            print(colored(ohlc, 'red' if ohlc['Description'] == 'Bearish' else 'green'))
            if not did_price_action:
                action = evaluate_movement(ohlc, prev_ohlc)
                did_price_action = action == 'BUY' or action == 'SELL'
                if action == 'BUY':
                    print('Buying Asset')
                if action == 'SELL':
                    print('Selling Asset')
