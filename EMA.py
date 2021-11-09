import pandas as pd


def exponential_moving_average(values, period, span):
    data = pd.DataFrame({'period': period, 'price': values})
    data['mva'] = data['price'].ewm(span=span, adjust=False).mean()
    newData = data['mva'].tail(1).values
    if len(newData) == 1:
        return newData[0]
