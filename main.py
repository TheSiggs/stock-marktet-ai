from KrakenAPI import KrakenAPI

kraken = KrakenAPI()
print(kraken.get_open_orders({'trades': True}).json())
