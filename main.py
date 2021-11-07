import now as now

from KrakenAPI import KrakenAPI
from datetime import datetime
from termcolor import colored
import pandas as pd
import time

kraken = KrakenAPI()
interval = 1


def exponential_moving_average(values, period, span, default):
    data = pd.DataFrame({'period': period, 'price': values})
    data['mva'] = data['price'].ewm(span=span, adjust=False).mean()
    newData = data['mva'].tail(1).values
    if len(newData) == 1:
        return newData[0]
    else:
        return default


ohlc = kraken.get_ohlc_data({'pair': 'XXBTZUSD', 'interval': interval})['result']['XXBTZUSD']

ohlc_formatted = [
    {
        'Unix Timestamp': data[0],
        'Readable Time': datetime.utcfromtimestamp(data[0]).strftime('%d-%m-%Y %H:%M:%S'),
        'Open Price': data[1],
        'Close Price': data[4],
        'Highest Price': data[2],
        'Lowest Price': data[3],
        'Volume Weighted Average Price': data[5],
        'Volume Traded': data[6],
        'Count': data[7],
        'Description': 'Bearish' if data[1] > data[4] else 'Bullish',
        '3 Period EMA': exponential_moving_average([value[5] for value in ohlc[0: index]],
                                                   [value[0] for value in ohlc[0: index]], 3,
                                                   data[5]),
        '6 Period EMA': exponential_moving_average([value[5] for value in ohlc[0: index]],
                                                   [value[0] for value in ohlc[0: index]], 6,
                                                   data[5]),
        '9 Period EMA': exponential_moving_average([value[5] for value in ohlc[0: index]],
                                                   [value[0] for value in ohlc[0: index]], 9,
                                                   data[5]),
    } for index, data in enumerate(ohlc)]

for data in ohlc_formatted:
    colour = 'red' if data['Description'] == 'Bearish' else 'green'
    print(colored(data, colour))

while True:
    time.sleep(10)
    ohlc = kraken.get_ohlc_data(
        {'pair': 'XXBTZUSD', 'interval': interval, 'since': ohlc_formatted[-1]['Unix Timestamp']})
    if len(ohlc['error']) > 0:
        print(ohlc['error'])
    new_ohlc = ohlc['result']['XXBTZUSD']
    temp_ohlc = {}
    prev = ohlc_formatted[-1]['Unix Timestamp']
    for data in new_ohlc:
        if data[0] > ohlc_formatted[-1]['Unix Timestamp']:
            new_entry = {
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
                '3 Period EMA': exponential_moving_average(
                    [value['Volume Weighted Average Price'] for value in ohlc_formatted],
                    [value['Unix Timestamp'] for value in ohlc_formatted], 3,
                    data[5]),
                '6 Period EMA': exponential_moving_average(
                    [value['Volume Weighted Average Price'] for value in ohlc_formatted],
                    [value['Unix Timestamp'] for value in ohlc_formatted], 6,
                    data[5]),
                '9 Period EMA': exponential_moving_average(
                    [value['Volume Weighted Average Price'] for value in ohlc_formatted],
                    [value['Unix Timestamp'] for value in ohlc_formatted], 9,
                    data[5]),
            }

            temp_ohlc[new_entry['Unix Timestamp']] = new_entry
            if len(temp_ohlc) == 1:
                prev = new_entry['Unix Timestamp']
            if len(temp_ohlc) == 2:
                ohlc_formatted.append(temp_ohlc[prev])
                del temp_ohlc[prev]
                prev = new_entry['Unix Timestamp']
                print(colored(ohlc_formatted[-1], 'red' if ohlc_formatted[-1]['Description'] == 'Bearish' else 'green'))

# Check when 3 period ema is moving through the 6 and 9 EMA
# If it's going up, buy
# If it's going down, sell
