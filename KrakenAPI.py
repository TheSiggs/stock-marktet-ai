from typing import TypedDict

import requests
import urllib.parse
import hashlib
import hmac
import base64
import time

from QueryObject import QueryObject

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
    """See https://docs.kraken.com/rest/ for information on the API"""
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
    API_CLOSED_ORDERS = '/0/private/ClosedOrders'
    API_QUERY_ORDERS = '/0/private/QueryOrders'
    API_TRADE_HISTORY = '/0/private/TradesHistory'
    API_TRADE_INFO = '/0/private/QueryTrades'
    API_OPEN_POSITIONS = '/0/private/OpenPositions'
    API_LEDGERS_INFO = '/0/private/Ledgers'

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

    def get_asset_pairs(self, params: dict[str, str]):
        """Gets information on tradable asset pairs
         usage: {
             pair: string - Asset pairs to get data for example pair=XXBTCZUSD,XETHXXBT
             info: string - Info to retrieve. (optional). Default "info", Enum "info" "leverage" "fees" "margin"
         }
        """
        query = QueryObject(params)
        return requests.get(self.API_ASSET_PAIRS + query.str())

    def get_tickers(self, pair: str):
        """ Gets information on tradable asset tickers

        :parameter pair: str - pair=XBTUSD Asset pair to get data for
        """
        return requests.get(self.API_TICKER + pair)

    def get_ohlc_data(self, params: dict):
        """Gets a list of tick data:
        usage: {
            pair: string - Asset pair to get data for (required) Example: pair=XBTUSD
            interval: integer - Time frame interval in minutes, Default: 1 Enum: 1 5 15 30 60 240 1440 10080 21600
            since: integer - Return committed OHLC data since given ID Example: since=1548111600
        }
        """
        query = QueryObject(params)
        return requests.get(self.API_OHLC + query.str())

    def get_order_book(self, params: dict):
        """Get asset pair order book entries
        usage: {
            pair: string - Asset pair to get data for (required) Example: pair=XBTUSD
            count: integer - maximum number of asks/bids Default: 100 Example: count=2
        }
        """
        query = QueryObject(params)
        return requests.get(self.API_ORDER_BOOK + query.str())

    def get_recent_trades(self, params: dict):
        """Gets Array of trade entries:
        usage: {
            pair: string - Asset pair to get data for (required) Example: pair=XBTUSD
            since: string - Return trade data since given timestamp Example: since=1616663618
        }
        """
        query = QueryObject(params)
        return requests.get(self.API_RECENT_TRADES + query.str())

    def get_recent_spread(self, params: dict):
        """Get Array of spread entries:
        usage: {
            pair: string - Asset pair to get data Example: pair=XBTUSD
            since: integer - Return spread data since given
        }
        """
        query = QueryObject(params)
        return requests.get(self.API_RECENT_SPREAD + query.str())

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

    def get_open_orders(self, params: dict):
        """ Retrieve information about currently open orders.
        usage: {
            trades: boolean - Whether or not to include trades related to position in output Default: false
            userref: integer <int32> - Restrict results to given user reference id
        }
        """
        return self.kraken_request(self.API_OPEN_ORDERS, {
            "nonce": str(int(1000 * time.time())), **params
        }, API_KEY, API_SEC)

    def get_closed_orders(self, user_ref: int, start: int, end: int, ofs: int, close_time: str = 'both',
                          trades: bool = False):
        """ Retrieve information about orders that have been closed (filled or cancelled).
            50 results are returned at a time, the most recent by default.
            :parameter trades: bool - Whether or not to include trades related to position in output. Default: False, Enum: True, False
            :parameter user_ref: int - Restrict results to given user reference id
            :parameter start: int - Starting unix timestamp or order tx ID of results (exclusive)
            :parameter end: int - Ending unix timestamp or order tx ID of results (inclusive)
            :parameter ofs: int - Result offset for pagination
            :parameter close_time: str - Which time to use to search. Default: 'both', Enum: 'open', 'close', 'both'
        :return: Closed Orders
        """
        return self.kraken_request(self.API_CLOSED_ORDERS, {
            "nonce": str(int(1000 * time.time())),
            "user_ref": user_ref,
            "trades": trades,
            "start": start,
            "end": end,
            "ofs": ofs,
            "closetime": close_time
        }, API_KEY, API_SEC)

    def query_orders_info(self, txid: str, user_ref: int, trades: bool = False):
        """ Retrieve information about specific orders.
        :param txid: (required) Comma delimited list of transaction IDs to query info about (20 maximum)
        :param user_ref: Restrict results to given user reference id
        :param trades: Whether or not to include trades related to position in output
        :return:
        """
        return self.kraken_request(self.API_QUERY_ORDERS, {
            "nonce": str(int(1000 * time.time())),
            "txid": txid,
            "trades": trades,
            "userref": user_ref,
        }, API_KEY, API_SEC)

    def get_trades_history(self, start: int, end: int, ofs: int, trade_type: str = 'all', trades: bool = False):
        """ Retrieve information about trades/fills. 50 results are returned at a time, the most recent by default.
            Unless otherwise stated, costs, fees, prices, and volumes are specified with the precision for the
            asset pair (pair_decimals and lot_decimals), not the individual assets' precision (decimals).
        :param start: Starting unix timestamp or trade tx ID of results (exclusive)
        :param end: Ending unix timestamp or trade tx ID of results (inclusive)
        :param ofs: Result offset for pagination
        :param trade_type: Whether or not to include trades related to position in output. Default: False
        :param trades: Type of trade. Default: 'all' Enum: 'all', 'any position', 'closed position', 'closing position', 'no position'
        :return:
        """
        return self.kraken_request(self.API_TRADE_HISTORY, {
            "nonce": str(int(1000 * time.time())),
            "trades": trades,
            "type": trade_type,
            "start": start,
            "end": end,
            "ofs": ofs,
        }, API_KEY, API_SEC)

    def query_trade_info(self, txid: str, trades: bool = False):
        """ Retrieve information about specific trades/fills.
        :param txid: Comma delimited list of transaction IDs to query info about (20 maximum)
        :param trades: Whether or not to include trades related to position in output. Default: False
        :return:
        """
        self.kraken_request(self.API_TRADE_INFO, {
            "nonce": str(int(1000 * time.time())),
            "txid": txid,
            "trades": trades
        }, API_KEY, API_SEC)

    def get_open_positions(self, txid: str, consolidation: str, docalcs: bool = False):
        """ Get information about open margin positions.
        :param txid: Comma delimited list of txids to limit output to
        :param consolidation: Consolidate positions by market/pair. Value: 'market'
        :param docalcs: Whether to include P&L calculations. Default: False
        :return:
        """
        self.kraken_request(self.API_OPEN_POSITIONS, {
            "nonce": str(int(1000 * time.time())),
            "txid": txid,
            "consolidation": consolidation,
            "docalcs": docalcs
        }, API_KEY, API_SEC)

    def get_ledgers_info(self, start: int, end: int, ofs: str, asset: str = 'all', asset_class: str = 'currency',
                         ledger_type: str = 'all'):
        """ Retrieve information about ledger entries. 50 results are returned at a time, the most recent by default.
        :param start: Starting unix timestamp or ledger ID of results (exclusive)
        :param end: Ending unix timestamp or ledger ID of results (inclusive)
        :param ofs: Result offset for pagination
        :param asset: Comma delimited list of assets to restrict output to. Default: 'all'
        :param asset_class: Asset class. Default: 'currency'
        :param ledger_type: Type of ledger to retrieve. Default: 'all' Enum: 'all', 'deposit', 'withdrawal', 'trade', 'margin'
        :return: Response
        """
        return self.kraken_request(self.API_LEDGERS_INFO, {
            'nonce': str(int(1000 * time.time())),
            'asset': asset,
            'aclass': asset_class,
            'type': ledger_type,
            'start': start,
            'end': end,
            'ofs': ofs,
        }, API_KEY, API_SEC)


kraken = KrakenAPI()
