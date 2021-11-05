from KrakenAPI import KrakenAPI
from datetime import datetime
from termcolor import colored

kraken = KrakenAPI()

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
        'Description': 'Bearish' if data[1] > data[4] else 'Bullish'
    } for data in ohlc]

for data in ohlc_formatted:
    print(colored(data, 'red') if data['Description'] == 'Bearish' else colored(data, 'green'))


