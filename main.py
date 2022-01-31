from EMA import exponential_moving_average
from KrakenAPI import KrakenAPI
from datetime import datetime
import time
from termcolor import colored
from evaluateMovement import evaluate_movement

kraken = KrakenAPI()

currency = 'ETHUSD'
pair = 'XETHZUSD'
wallet_coin = 'XETH'
wallet_fiat = 'ZUSD'
interval = 1
index = -1
did_price_action = False
last_timestamp = 0

prev = {}
while True
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
                try:
                    # Get account balance
                    wallet = kraken.get_account_balance()['result']
                    crypto_coin = wallet[wallet_coin]
                    dollar_coin = wallet[wallet_fiat]

                    # Calculate percentage of wallet
                    crypto_coin_usage = round((float(crypto_coin) * 0.2), 4)
                    crypto_coin_usage = crypto_coin_usage if crypto_coin_usage >= 0.004 else 0.004
                    if action == 'BUY':
                        print('Buying Asset')
                        # Place Order
                        print({'ordertype': 'market', 'type': 'buy', 'pair': pair, 'volume': crypto_coin_usage})
                        resp = kraken.add_order(
                            {'ordertype': 'market', 'type': 'buy', 'pair': pair, 'volume': crypto_coin_usage})
                        print('Return:', resp)
                    elif action == 'SELL':
                        print('Selling Asset')
                        # Place Order
                        print({'ordertype': 'market', 'type': 'sell', 'pair': pair, 'volume': crypto_coin_usage})
                        resp = kraken.add_order(
                            {'ordertype': 'market', 'type': 'sell', 'pair': pair, 'volume': crypto_coin_usage})
                        print('Return:', resp)
                except e:
                    print(e)

