from KrakenAPI import KrakenAPI
from datetime import datetime
from termcolor import colored
import pandas as pd
import numpy as np

kraken = KrakenAPI()


def exponential_moving_average(values, period, span):
    data = pd.DataFrame({'period': period, 'price': values})
    data['mva'] = data['price'].ewm(span=span, adjust=False).mean()
    newData = data['mva'].tail(1)
    print('data: ', newData,  'type: ', type(newData))
    # return data['mva'][-1]


ohlc = kraken.get_ohlc_data({'pair': 'XXBTZUSD', 'interval': 5})['result']['XXBTZUSD']

ohlc_formatted = [
    {
        'Unix Timestamp': data[0],
        'Readable Time': datetime.utcfromtimestamp(data[0]).strftime('%d-%m-%Y %H:%M:%S'),
        'Open Price': data[1],
        'Highest Price': data[2],
        'Lowest Price': data[3],
        'Close Price': data[4],
        'Volume Weighted Average Price': data[5],
        'Volume Traded': data[6],
        'Count': data[7],
        'Description': 'Bearish' if data[1] > data[4] else 'Bullish',
        'Volume Weighted Moving Average': weighted_moving_average([value[5] for value in ohlc[0: index]],
                                                                  [value[0] for value in ohlc[0: index]], 5)
    } for index, data in enumerate(ohlc)]

# for data in ohlc_formatted:
#     print(colored(data, 'red') if data['Description'] == 'Bearish' else colored(data, 'green'))
