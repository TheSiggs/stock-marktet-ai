from KrakenAPI import KrakenAPI
from datetime import datetime
from termcolor import colored
import pandas as pd
import time

from Point import Point, do_intersect

kraken = KrakenAPI()
interval = 1
currency = 'BTC/USD' or 'XXBTZUSD'


def exponential_moving_average(values, period, span, default):
    data = pd.DataFrame({'period': period, 'price': values})
    data['mva'] = data['price'].ewm(span=span, adjust=False).mean()
    newData = data['mva'].tail(1).values
    if len(newData) == 1:
        return newData[0]
    else:
        return default


def evaluate_movement(data):
    EMAP3 = Point(data[-2]['Unix Timestamp'], data[-2]['3 Period EMA'])
    EMAQ3 = Point(data[-1]['Unix Timestamp'], data[-1]['3 Period EMA'])
    EMAP6 = Point(data[-2]['Unix Timestamp'], data[-2]['6 Period EMA'])
    EMAQ6 = Point(data[-1]['Unix Timestamp'], data[-1]['6 Period EMA'])
    EMAP9 = Point(data[-2]['Unix Timestamp'], data[-2]['9 Period EMA'])
    EMAQ9 = Point(data[-1]['Unix Timestamp'], data[-1]['9 Period EMA'])

    if do_intersect(EMAP3, EMAQ3, EMAP6, EMAQ6) or do_intersect(EMAP3, EMAQ3, EMAP9, EMAQ9):
        print('3P EMA intersected with 6P EMA')
        if data[-1]['3 Period EMA'] > data[-2]['6 Period EMA']:
            print("3P EMA is above 6P EMA")
        if data[-1]['3 Period EMA'] < data[-2]['6 Period EMA']:
            print("3P EMA is below 6P EMA")
        if data[-1]['3 Period EMA'] > data[-2]['9 Period EMA']:
            print("3P EMA is above 9P EMA")
        if data[-1]['3 Period EMA'] < data[-2]['9 Period EMA']:
            print("3P EMA is below 9P EMA")
        # Check if the 3 Period EMA is going below the 6 and 9 Period EMA
        # Also check if the last two candles are bearish
        # If both are the case, it's a good time to sell
        if data[-1]['3 Period EMA'] < data[-2]['9 Period EMA'] \
                and data[-1]['3 Period EMA'] < data[-2]['6 Period EMA']:
                # and data[-1]['Description'] == 'Bearish' \
                # and data[-2]['Description'] == 'Bearish':
            print('3EMA Going BELOW 6EMA and 9EMA and both candles are Bearish - SELL')
        # Check if the 3 Period EMA is going above the 6 and 9 Period EMA
        # Also check if the last two candles are bullish
        # If both are the case, it's a good time to buy
        if data[-1]['3 Period EMA'] > data[-2]['9 Period EMA'] \
                and data[-1]['3 Period EMA'] > data[-2]['6 Period EMA']:
                # and data[-1]['Description'] == 'Bullish' \
                # and data[-2]['Description'] == 'Bullish':
            print('3EMA Going ABOVE 6EMA and 9EMA and both candles are Bullish - BUY')


ohlc = kraken.get_ohlc_data({'pair': currency, 'interval': interval})
try:
    ohlc = ohlc['result'][currency]
except KeyError:
    print(ohlc)

ohlc_formatted = [
    {
        'Currency': currency,
        'Unix Timestamp': data[0],
        'Readable Time': datetime.utcfromtimestamp(data[0]).strftime('%d-%m-%Y %H:%M:%S'),
        'Open Price': float(data[1]),
        'Close Price': float(data[4]),
        'Highest Price': float(data[2]),
        'Lowest Price': float(data[3]),
        'Volume Weighted Average Price': float(data[5]),
        'Volume Traded': float(data[6]),
        'Count': data[7],
        'Description': 'Bullish' if float(data[4]) > float(data[1]) else 'Bearish',
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
        {'pair': currency, 'interval': interval, 'since': ohlc_formatted[-1]['Unix Timestamp']})
    try:
        new_ohlc = ohlc['result'][currency]
        prev = ohlc_formatted[-1]['Unix Timestamp']
        for data in new_ohlc:
            if data[0] > ohlc_formatted[-1]['Unix Timestamp']:
                new_entry = {
                    'Currency': currency,
                    'Unix Timestamp': data[0],
                    'Readable Time': datetime.utcfromtimestamp(data[0]).strftime('%d-%m-%Y %H:%M:%S'),
                    'Open Price': float(data[1]),
                    'Close Price': float(data[4]),
                    'Highest Price': float(data[2]),
                    'Lowest Price': float(data[3]),
                    'Volume Weighted Average Price': float(data[5]),
                    'Volume Traded': float(data[6]),
                    'Count': data[7],
                    'Description': 'Bullish' if float(data[4]) > float(data[1]) else 'Bearish',
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
                if float(new_entry['Volume Weighted Average Price']) > 0.0:
                    ohlc_formatted.append(new_entry)
                    # evaluate_movement
                    print(colored(ohlc_formatted[-1],
                                  'red' if ohlc_formatted[-1]['Description'] == 'Bearish' else 'green'))

                # temp_ohlc[new_entry['Unix Timestamp']] = new_entry
                # if len(temp_ohlc) == 1:
                #     prev = new_entry['Unix Timestamp']
                # if len(temp_ohlc) == 2:
                #     ohlc_formatted.append(temp_ohlc[prev])
                #     del temp_ohlc[prev]
                #     prev = new_entry['Unix Timestamp']
                #     # evaluate_movement
                #     evaluate_movement(ohlc_formatted)
                #     print(colored(ohlc_formatted[-1],
                #                   'red' if ohlc_formatted[-1]['Description'] == 'Bearish' else 'green'))
    except KeyError:
        print(ohlc)
