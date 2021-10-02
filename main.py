import requests
import urllib.parse
import hashlib
import hmac
import base64
import time

API_KEY = 'lWr1ajj72dxsxPkNVyQKNum3iNHs9Jx1GAmCsABUxjwWBF1rpuDSyo03'
API_SEC = 'KSMkkRkDsJnOeRrIs5JlkTwPgStNEwlzSq0PFPu4DMeFlLY7k24YsM2mAfuhQ8NuoQ77KfC/50+1Bj89UYlxOg=='


def get_kraken_signature(url_path, data, secret):
    post_data = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + post_data).encode()
    message = url_path.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sig_digest = base64.b64encode(mac.digest())
    return sig_digest.decode()


class KrakenAPI:
    # API Constants
    API = 'https://api.kraken.com'
    API_SERVER_TIME = API + '/0/public/Time'
    API_SYSTEM_STATUS = API + '/0/public/SystemStatus'
    API_ASSETS = API + '/0/public/Assets'
    API_ASSET_PAIRS = API + '/0/public/AssetPairs?pair='  # Get Tradable Asset Pair - XXBTZUSD,XETHXXBT
    API_TICKER = API + '/0/public/Ticker?pair='  # Get Ticker Information - pair of assets eg: XXBTZUSD,XETHXXBT
    API_OHLC = API + '/0/public/OHLC?pair='
    API_ORDER_BOOK = API + '/0/public/Depth?pair='
    API_RECENT_TRADES = API + '/0/public/Trades?pair='
    API_RECENT_SPREAD = API + '/0/public/Spread?pair='
    API_BALANCE = '/0/private/Balance'
    API_TRADE_BALANCE = '/0/private/TradeBalance'
    API_OPEN_ORDERS = '/0/private/OpenOrders'

    def kraken_request(self, uri_path, data, api_key, api_sec):
        """Attaches auth headers and returns results of a POST request"""
        headers = {'API-Key': api_key, 'API-Sign': get_kraken_signature(uri_path, data, api_sec)}
        req = requests.post((self.API + uri_path), headers=headers, data=data)
        return req

    # ----------------
    # Public Endpoints
    # ----------------
    def get_server_time(self):
        """Gets server time in a Unix timestamp and RFC1123 time format"""
        return requests.get(self.API_SERVER_TIME)

    def get_system_status(self):
        """Get server status with timestamp in RFC3339 format"""
        return requests.get(self.API_SYSTEM_STATUS)

    def list_assets(self):
        """Gets a list of all the assets"""
        return requests.get(self.API_ASSETS)

    def get_asset_pairs(self, pairs: str):
        """Gets information on tradable asset pairs

        :parameter pairs: str - Example: pair=XXBTCZUSD,XETHXXBT Asset pairs to get data for
        """
        return requests.get(self.API_ASSET_PAIRS + pairs)

    def get_tickers(self, pair: str):
        """ Gets information on tradable asset tickers

        :parameter pair: str - pair=XBTUSD Asset pair to get data for
        """
        return requests.get(self.API_TICKER + pair)

    def get_ohlc_data(self, pair: str):
        """Gets a list of tick data:

        :parameter pair: str - pair=XBTUSD Asset pair to get data for
        """
        return requests.get(self.API_OHLC + pair)

    def get_order_book(self, pair):
        """Get asset pair order book entries

        :parameter pair: str - pair=XBTUSD Asset pair to get data for
        """
        return requests.get(self.API_ORDER_BOOK + pair)

    def get_recent_trades(self, pair: str):
        """Gets Array of trade entries:

        :parameter pair: str - pair=XBTUSD Asset pair to get data for
        """
        return requests.get(self.API_RECENT_TRADES + pair)

    def get_recent_spread(self, pair: str):
        """Get Array of spread entries:

        :parameter pair: str - pair=XBTUSD Asset pair to get data for
        """
        return requests.get(self.API_RECENT_SPREAD + pair)

    # -----------------------
    # Authenticated Endpoints
    # -----------------------
    # TODO Authenticated Endpoints
    def get_account_balance(self):
        """Retrieve all cash balances, net of pending withdrawals:"""
        return self.kraken_request(self.API_BALANCE, {
            "nonce": str(int(1000 * time.time()))
        }, API_KEY, API_SEC)

    def get_trade_balance(self, asset: str):
        """Retrieve a summary of collateral balances, margin position valuations, equity and margin level.
           :parameter asset: str - Base asset used to determine balance"""
        return self.kraken_request(self.API_TRADE_BALANCE, {
            "nonce": str(int(1000 * time.time())),
            "asset": asset
        }, API_KEY, API_SEC)

    def get_open_orders(self, trades: bool):
        """ Retrieve information about currently open orders.
        :parameter trades: bool - Whether or not to include trades related to position in output
        """
        return self.kraken_request(self.API_OPEN_ORDERS, {
            "nonce": str(int(1000 * time.time())),
            "trades": trades
        }, API_KEY, API_SEC)


kraken = KrakenAPI()
