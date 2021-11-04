import requests
import urllib.parse
import hashlib
import hmac
import base64
import time

# Pandas Documentation Guide: https://pandas.pydata.org/docs/development/contributing_docstring.html#parameter-types
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

    def __init__(self):
        """See https://docs.kraken.com/rest/ for information on the API"""
        self.API = 'https://api.kraken.com'

        # API Constants
        self.API_SERVER_TIME = self.API + '/0/public/Time'
        self.API_SYSTEM_STATUS = self.API + '/0/public/SystemStatus'
        self.API_ASSETS = self.API + '/0/public/Assets'
        self.API_ASSET_PAIRS = self.API + '/0/public/AssetPairs?pair='  # Get Tradable Asset Pair - XXBTZUSD,XETHXXBT
        self.API_TICKER = self.API + '/0/public/Ticker?pair='  # Get Ticker Information - pair of assets eg: XXBTZUSD,XETHXXBT
        self.API_OHLC = self.API + '/0/public/OHLC?pair='
        self.API_ORDER_BOOK = self.API + '/0/public/Depth?pair='
        self.API_RECENT_TRADES = self.API + '/0/public/Trades?pair='
        self.API_RECENT_SPREAD = self.API + '/0/public/Spread?pair='
        self.API_BALANCE = '/0/private/Balance'
        self.API_TRADE_BALANCE = '/0/private/TradeBalance'
        self.API_OPEN_ORDERS = '/0/private/OpenOrders'
        self.API_CLOSED_ORDERS = '/0/private/ClosedOrders'
        self.API_QUERY_ORDERS = '/0/private/QueryOrders'
        self.API_TRADE_HISTORY = '/0/private/TradesHistory'
        self.API_TRADE_INFO = '/0/private/QueryTrades'
        self.API_OPEN_POSITIONS = '/0/private/OpenPositions'
        self.API_LEDGERS_INFO = '/0/private/Ledgers'
        self.API_QUERY_LEDGERS = '/0/private/QueryLedgers'
        self.API_TRADE_VOLUME = '/0/private/TradeVolume'
        self.API_ADD_EXPORT = '/0/private/AddExport'
        self.API_EXPORT_STATUS = '/0/private/ExportStatus'
        self.API_RETRIEVE_EXPORT = '/0/private/RetrieveExport'
        self.API_REMOVE_EXPORT = '/0/private/RemoveExport'
        self.API_ADD_ORDER = '/0/private/AddOrder'
        self.API_CANCEL_ORDER = '/0/private/CancelOrder'
        self.API_CANCEL_ALL_ORDERS = '/0/private/CancelAll'
        self.API_CANCEL_ORDERS_AFTER_TIME = '/0/private/CancelAllOrdersAfter'
        self.API_DEPOSIT_METHODS = '/0/private/DepositMethods'
        self.API_DEPOSIT_ADDRESSES = '/0/private/DepositAddresses'
        self.API_DEPOSIT_STATUS = '/0/private/DepositStatus'
        self.API_WITHDRAWAL_INFO = '/0/private/WithdrawInfo'
        self.API_WITHDRAW_FUNDS = '/0/private/Withdraw'
        self.API_WITHDRAW_STATUS = '/0/private/WithdrawStatus'
        self.API_WITHDRAW_CANCEL = '/0/private/WithdrawCancel'
        self.API_WALLET_TRANSFER = '/0/private/WalletTransfer'
        self.API_STAKE_ASSET = '/0/private/Stake'
        self.API_UNSTAKE_ASSET = '/0/private/Unstake'
        self.API_LIST_STAKING_ASSETS = '/0/private/Staking/Assets'
        self.API_STAKE_PENDING = '/0/private/Staking/Pending'
        self.API_STAKING_TRANSACTIONS = '/0/private/Staking/Transactions'
        self.API_WEBSOCKET_TOKEN = '/0/private/GetWebSocketsToken'

    def kraken_request(self, uri_path: str, data: dict, api_key: str, api_sec: str):
        """Attaches auth headers and returns results of a POST request"""
        headers = {'API-Key': api_key, 'API-Sign': get_kraken_signature(uri_path, data, api_sec)}
        req = requests.post((self.API + uri_path), headers=headers, data=data)
        return req

    # ----------------
    # Public Endpoints
    # ----------------

    # Market Data
    def get_server_time(self):
        """
        Gets server time in a Unix timestamp and RFC1123 time format
        https://docs.kraken.com/rest/#operation/getServerTime
        """
        return requests.get(self.API_SERVER_TIME)

    def get_system_status(self):
        """
        Get server status with timestamp in RFC3339 format
        https://docs.kraken.com/rest/#operation/getSystemStatus
        """
        return requests.get(self.API_SYSTEM_STATUS)

    def list_assets(self):
        """
        Gets a list of all the assets
        https://docs.kraken.com/rest/#operation/getAssetInfo
        """
        return requests.get(self.API_ASSETS)

    def get_asset_pairs(self, params: dict[str, str]):
        """
        Gets information on tradable asset pairs
        https://docs.kraken.com/rest/#operation/getTradableAssetPairs

        Parameters
        __________
         pair: string
            Asset pairs to get data for example pair=XXBTCZUSD,XETHXXBT
         info: string
            Info to retrieve. (optional). Default "info", Enum "info" "leverage" "fees" "margin"
        :return:
        """
        query = QueryObject(params)
        return requests.get(self.API_ASSET_PAIRS + query.str())

    def get_tickers(self, pair: str):
        """
        Gets information on tradable asset tickers
        https://docs.kraken.com/rest/#operation/getTickerInformation

        Parameters
        __________
        pair: str
            Asset pair to get data for Example: pair=XBTUSD
        :return:
        """
        return requests.get(self.API_TICKER + pair)

    def get_ohlc_data(self, params: dict):
        """
        Gets a list of tick data:
        https://docs.kraken.com/rest/#operation/getOHLCData

        Parameters
        __________
        pair: string
            Asset pair to get data for (required) Example: pair=XBTUSD
        interval: integer
            Time frame interval in minutes, Default: 1 Enum: 1 5 15 30 60 240 1440 10080 21600
        since: integer
            Return committed OHLC data since given ID Example: since=1548111600
        :return:
        """
        query = QueryObject(params)
        return requests.get(self.API_OHLC + query.str())

    def get_order_book(self, params: dict):
        """
        Get asset pair order book entries
        https://docs.kraken.com/rest/#operation/getOrderBook

        Parameters
        __________
        pair: string
            Asset pair to get data for (required) Example: pair=XBTUSD
        count: integer
            maximum number of asks/bids Default: 100 Example: count=2
        :return:
        """
        query = QueryObject(params)
        return requests.get(self.API_ORDER_BOOK + query.str())

    def get_recent_trades(self, params: dict):
        """
        Gets Array of trade entries:
        https://docs.kraken.com/rest/#operation/getRecentTrades

        Parameters
        __________
        pair: string
            Asset pair to get data for (required) Example: pair=XBTUSD
        since: string
            Return trade data since given timestamp Example: since=1616663618
        :return:
        """
        query = QueryObject(params)
        return requests.get(self.API_RECENT_TRADES + query.str())

    def get_recent_spread(self, params: dict):
        """
        Get Array of spread entries:
        https://docs.kraken.com/rest/#operation/getRecentSpreads

        Parameters
        __________
        pair: string
            Asset pair to get data Example: pair=XBTUSD
        since: integer
            Return spread data since given
        :return:
        """
        query = QueryObject(params)
        return requests.get(self.API_RECENT_SPREAD + query.str())

    # -----------------------
    # Authenticated Endpoints
    # -----------------------
    # TODO Authenticated Endpoints

    # User Data
    def get_account_balance(self):
        """
        Retrieve all cash balances, net of pending withdrawals:
        https://docs.kraken.com/rest/#operation/getAccountBalance
        """
        return self.kraken_request(self.API_BALANCE, {
            "nonce": str(int(1000 * time.time()))
        }, API_KEY, API_SEC)

    def get_trade_balance(self, asset: str):
        """
        Retrieve a summary of collateral balances, margin position valuations, equity and margin level.
        https://docs.kraken.com/rest/#operation/getTradeBalance

        Parameters
        __________
        asset: str
            Base asset used to determine balance
        :return:
        """
        return self.kraken_request(self.API_TRADE_BALANCE, {
            "nonce": str(int(1000 * time.time())),
            "asset": asset
        }, API_KEY, API_SEC)

    def get_open_orders(self, params: dict):
        """
        Retrieve information about currently open orders.
        https://docs.kraken.com/rest/#operation/getOpenOrders

        Parameters
        __________
        trades: boolean
            Whether or not to include trades related to position in output Default: false
        userref: integer <int32>
            Restrict results to given user reference id

        :return:
        """
        return self.kraken_request(self.API_OPEN_ORDERS, {
            "nonce": str(int(1000 * time.time())), **params
        }, API_KEY, API_SEC)

    def get_closed_orders(self, params: dict):
        """
        Retrieve information about orders that have been closed (filled or cancelled).
        50 results are returned at a time, the most recent by default.
        https://docs.kraken.com/rest/#operation/getClosedOrders

        Parameters
        __________
        trades: boolean
            Whether or not to include trades related to position in output.
        userref: integer <int32>
            Limit results to given user reference id.
        start: integer
            Starting unix timestamp or order tx ID of results (exclusive).
        end: integer
            End unix timestamp or order tx ID of results (inclusive).
        ofs: integer
            Result offset for pagination.
        closetime: string
            Which time to use to search Default: "both" Enum: "open" "close" "both".
        :return: Closed Orders
        """
        return self.kraken_request(self.API_CLOSED_ORDERS, {
            "nonce": str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def query_orders_info(self, params: dict):
        """
        Retrieve information about specific orders.
        https://docs.kraken.com/rest/#operation/getOrdersInfo

        Parameters
        __________
        trades: boolean
            Whether or not to include trades related to position in output Default: false
        userref: integer <int32>
            Restrict results to given user reference id.
        txid: string
            Comma delimited list of transaction IDs to query info about (20 maximum) (Required)
        :return:
        """
        return self.kraken_request(self.API_QUERY_ORDERS, {
            "nonce": str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def get_trades_history(self, params: dict):
        """
        Retrieve information about trades/fills. 50 results are returned at a time, the most recent by default.
        Unless otherwise stated, costs, fees, prices, and volumes are specified with the precision for the
        asset pair (pair_decimals and lot_decimals), not the individual assets' precision (decimals).
        https://docs.kraken.com/rest/#operation/getTradeHistory

        Parameters
        __________
        type: string
            Type of trade Default: "all" Enum: "all" "any position" "closed position" "closing position" "no position"
        trades: boolean
            Whether or not to include trades related to position in output Default: false
        start: integer
            Starting unix timestamp or trade tx ID of results (exclusive)
        end: integer
            End unix timestamp or txid tx ID of results (inclusive)
        ofs: integer
            Result offset for pagination
        :return:
        """
        return self.kraken_request(self.API_TRADE_HISTORY, {
            "nonce": str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def query_trade_info(self, params: dict):
        """
        Retrieve information about specific trades/fills.
        https://docs.kraken.com/rest/#operation/getTradesInfo

        Parameters
        __________
        txid: string
            Comma delimited list of transaction IDs to query info about (20 maximum)
        trades: boolean
            Whether or not to include trades related to position in output Default: false
        :return:
        """
        self.kraken_request(self.API_TRADE_INFO, {
            "nonce": str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def get_open_positions(self, params: dict):
        """
        Get information about open margin positions.
        https://docs.kraken.com/rest/#operation/getOpenPositions

        Parameters
        __________
        txid: string
            Comma delimited list of txids to limit output to
        docalcs: boolean
            Whether to include P&L calculations Default: false
        consolidation: string
            Consolidate positions by market/pair
        :return:
        """
        self.kraken_request(self.API_OPEN_POSITIONS, {
            "nonce": str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def get_ledgers_info(self, params: dict[str, any]):
        """
        Retrieve information about ledger entries. 50 results are returned at a time, the most recent by default.
        https://docs.kraken.com/rest/#operation/getLedgersInfo

        Parameters
        __________
        asset: string
            Comma delimited list of assets to restrict output to Default: "all"
        aclass: string
            Asset class Default: "currency"
        type: string
            Type of ledger to restrict Default: "all" Enum: "all" "deposit" "withdrawal" "trade" "margin"
        start: integer
            Starting unix timestamp or ledger ID of results (exclusive)
        end: integer
            End unix timestamp or ledger ID of results (inclusive)
        ofs: integer
            Result offset for pagination
        :return: Response
        """
        return self.kraken_request(self.API_LEDGERS_INFO, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def query_ledgers(self, params: dict):
        """
        Retrieve information about specific ledger entries.
        https://docs.kraken.com/rest/#operation/getLedgersInfo

        Parameters
        __________
        id: string
            Comma delimited list of ledger IDs to query info about (20 maximum)
        trades: boolean
            Whether or not to include trades related to position in output Default: false
        :return: Response
        """
        return self.kraken_request(self.API_QUERY_LEDGERS, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def get_trade_volume(self, params: dict):
        """
        Note: If an asset pair is on a maker/taker fee schedule, the taker side is given in fees and maker side in
        fees_maker. For pairs not on maker/taker, they will only be given in fees.
        https://docs.kraken.com/rest/#operation/getTradeVolume

        Parameters
        ----------
        pair: string
            Asset pair to get data for Example: pair=XBTUSD
        fee-info: boolean (optional)
            Whether or not to include fee information in results
        :return:


        Returns
        -------
        Response: Trade Volume

        """
        return self.kraken_request(self.API_TRADE_VOLUME, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def add_export(self, params: dict):
        """
        Request export of trades or ledgers.
        https://docs.kraken.com/rest/#operation/addExport

        Parameters
        ----------
        report: string (required)
            Type of data to export Enum: "trades", "ledgers"
        format: string
            File format to export Default: "CSV" Enum: "CSV", "TSV"
        description: (required)
            Description for the report.
        fields: string
            Comma delimited list of fields to include. Default "all"
            trades: ordertxid, time, ordertype, price, cost, fee, vol, margin, misc, ledgers
            ledgers: refid, time, type. aclass, asset, amount, fee, balance
        starttm: integer
            UNIX timestamp for the report start time (Default 1st of the current month)
        endtm: integer
            UNIX timestamp for the report end time (Default now)
        :return:
        Returns
        -------
        Response: Report
        """
        return self.kraken_request(self.API_ADD_EXPORT, {
            'nonce': str(int(1000) * time.time()),
            **params
        }, API_KEY, API_SEC)

    def get_export_status(self, params: dict):
        """
        Get status of requested data exports
        https://docs.kraken.com/rest/#operation/exportStatus

        Parameters
        ----------
        report: string (required)
            Type of reports to inquire about
        :return:

        Returns
        -------
        Response: Array of objects
        """
        return self.kraken_request(self.API_EXPORT_STATUS, {
            'nonce': str(int(1000) * time.time()),
            **params
        }, API_KEY, API_SEC)

    def retrieve_export(self, params: dict):
        """
        Retrieve a processed data export
        https://docs.kraken.com/rest/#operation/retrieveExport

        Parameters
        ----------
        id: string (required)
            Report ID to retrieve
        path: string (required)
            Full path to desired storage location
        :return:

        Returns
        -------
        Response: report
            Binary zip archive containing the report
        """
        # TODO: Add error checking
        resp = self.kraken_request(self.API_RETRIEVE_EXPORT, {
            'nonce': str(int(1000) * time.time()),
            **params
        }, API_KEY, API_SEC)

        # Write export to a new file 'export.zip'
        if params['path'][-1] == '/':
            target_path = params['path'] + 'export.zip'
        else:
            target_path = params['path'] + '/export.zip'

        handle = open(target_path, "wb")
        for chunk in resp.iter_content(chunk_size=512):
            if chunk:
                handle.write(chunk)
        handle.close()

    def delete_export(self, params: dict):
        """
        Delete exported trades/ledgers report
        https://docs.kraken.com/rest/#operation/removeExport

        Parameters
        ----------
        id: string (required)
            ID of report to delete or cancel
        type: string (required)
            delete can only be used for reports that have already been processed.
            Use cancel for queued or processing reports.
            Enum: "cancel", "delete"
        :return:

        Returns
        -------
        Response: boolean
            Whether the deletion/cancellation was successful
        """

        return self.kraken_request(self.API_REMOVE_EXPORT, {
            'nonce': str(int(1000) * time.time()),
            **params
        }, API_KEY, API_SEC)

    # User Trading
    def add_order(self, params: dict):
        """
        Place a new order.
        Note: See the AssetPairs endpoint for details on the available trading pairs,
        their price and quantity precisions, order minimums, available leverage, etc.
        https://docs.kraken.com/rest/#operation/addOrder

        Parameters
        ----------
        userref: integer <int32>
            User reference id
            userref is an optional user-specified integer id that can be associated with any number of orders.
            Many clients choose a userref corresponding to a unique integer id generated by their systems
            (e.g. a timestamp). However, because we don't enforce uniqueness on our side, it can also be used to easily
            group orders by pair, side, strategy, etc. This allows clients to more readily cancel or query information
            about orders in a particular group, with fewer API calls by using userref instead of our txid,
            where supported.

        ordertype: string (required)
            Order type
            Enum: "market" "limit" "stop-loss" "take-profit" "stop-loss-limit" "take-profit-limit" "settle-position"

        type: string (required)
            Order direction (buy/sell)
            Enum: "buy", "sell"

        volume: string
            Order quantity in terms of the base asset
            Note: Volume can be specified as 0 for closing margin orders to automatically fill the requisite quantity.

        pair: string (required)
            Asset pair id or altname

        price: string
            Price
            - Limit price for limit orders
            - Trigger price for stop-loss, stop-loss-limit, take-profit and take-profit-limit orders

        price2: string
            Secondary price for limit orders
            - Limit price for stop-loss-limit and take-profit-limit orders
            Note: Either price or price2 can be preceded by +, -, or # to specify the order price as an offset relative
            to the last traded price. + adds the amount to, and - subtracts the amount from the last traded price.
            # will either add or subtract the amount to the last traded price, depending on the direction and order
            type used. Relative prices can be suffixed with a % to signify the relative amount as a percentage.

        leverage: string
            Amount of leverage desired
            Default: "none"

        offlags: string
            Comma delimited list of order flags
            - post post-only order (available when ordertype = limit)
            - fcib prefer fee in base currency (default if selling)
            - fciq prefer fee in quote currency (default if buying, mutually exclusive with fcib)
            - nompp disable market price protection for market orders

        timeinforce: string
            Default "GTC"
            Enum: "GTC", "IOC", "GTD"
            Time-in-force of the order to specify how long it should remain in the order book before being cancelled.
            GTC (Good-'til-cancelled) is default if the parameter is omitted. IOC (immediate-or-cancel) will immediately
            execute the amount possible and cancel any remaining balance rather than resting in the book. GTD
            (good-'til-date), if specified, must coincide with a desired expiretm.

        starttm: string
            Scheduled start time. Can be specified as an absolute timestamp or as a number of seconds in the future
            - 0 now (default)
            - +<n> schedule start time seconds from now
            - <n> = unix timestamp of start time

        expiretm: string
            Expiration time
            - 0 no expiration (default)
            - +<n> = expire seconds from now, minimum 5 seconds
            - <n> = unix timestamp of expiration time

        close[ordertype]: string
            Conditional close order price
            Enum: "limit" "stop-loss" "take-profit" "stop-loss-limit" "take-profit-limit"
            Note: Conditional close orders are triggered by execution of the primary order in the same quantity and
            opposite direction, but once triggered are independent orders that may reduce or increase net position.

        close[price]: string
            Conditional close price

        close[price2]: string
            Conditional close price 2

        deadline: string
            RFC3339 timestamp (e.g. 2021-04-01T00:18:45Z) after which the matching engine should reject the new order
            request, in presence of latency or order queueing. min now() + 5 seconds, max now() + 60 seconds

        validate: boolean
            Validates inputs only. Do not submit order
            Default False

        :return:

        Returns
        -------
        Response: Order Added
            descr: Order description info
                order: string
                    Order description
                close:  string
                    Conditional close order description, if applicable
            txid: array<string>
                transaction IDs for order (if order was successful)
        """
        return self.kraken_request(self.API_ADD_ORDER, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def cancel_order(self, params: dict):
        """
        Cancel a particular open order (or set of open orders) by txid or userref
        https://docs.kraken.com/rest/#operation/cancelOrder

        Parameters
        ----------
        txid: string|integer
            Open order transaction ID (txid) or user reference (userref)
        :return:

        Returns
        -------
        Response: OrderCancelled
            count: integer
                Number of orders cancelled
            pending: boolean
                if set, order(s) is/are pending cancellation
        """
        return self.kraken_request(self.API_CANCEL_ORDER, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def cancel_all_orders(self):
        """
        Cancel all open orders
        https://docs.kraken.com/rest/#operation/cancelAllOrders
        """
        return self.kraken_request(self.API_CANCEL_ALL_ORDERS, {
            'nonce': str(int(1000 * time.time()))
        }, API_KEY, API_SEC)

    def cancel_orders_after_time(self, params: dict):
        """
        CancelAllOrdersAfter provides a "Dead Man's Switch" mechanism to protect the client from network malfunction,
        extreme latency or unexpected matching engine downtime. The client can send a request with a timeout
        (in seconds), that will start a countdown timer which will cancel all client orders when the timer expires.
        The client has to keep sending new requests to push back the trigger time, or deactivate the mechanism by
        specifying a timeout of 0. If the timer expires, all orders are cancelled and then the timer remains disabled
        until the client provides a new (non-zero) timeout.

        The recommended use is to make a call every 15 to 30 seconds, providing a timeout of 60 seconds. This allows
        the client to keep the orders in place in case of a brief disconnection or transient delay, while keeping them
        safe in case of a network breakdown. It is also recommended to disable the timer ahead of regularly scheduled
        trading engine maintenance (if the timer is enabled, all orders will be cancelled when the trading engine comes
        back from downtime - planned or otherwise).
        https://docs.kraken.com/rest/#operation/cancelAllOrdersAfter

        Parameters
        ----------
        timeout: integer (required)
            Duration (in seconds) to set/extend the timer by
        :return:
        Returns
        -------
        Response: object
            currentTime: string
                Timestamp (RFC3339 format) at which the request was received
            triggerTime: string
                Timestamp (RFC3339 format) at which all orders will be cancelled, unless the timer is
                extended or disabled
        """
        return self.kraken_request(self.API_CANCEL_ORDERS_AFTER_TIME, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    # ------------
    # User funding
    # ------------
    def get_deposit_methods(self, asset: str):
        """
        Retrieve methods available for depositing a particular asset.
        https://docs.kraken.com/rest/#operation/getDepositMethods

        Parameters
        ----------
        asset: string (required)
            Asset being deposited

        Returns
        -------
        Response: depositMethod
            Array [
                method: string
                    Name of deposit method
                limit: any
                    Maximum net amount that can be deposited right now, or false if no limit
                fee: string
                    Amount of fees that will be paid
                address-setup-fee: string
                    Whether or not method has an address setup fee
                gen-address: boolean
                    Whether new addresses can be generated from this method
            ]
        """
        return self.kraken_request(self.API_DEPOSIT_METHODS, {
            'nonce': str(int(1000 * time.time())),
            'asset': asset
        }, API_KEY, API_SEC)

    def get_deposit_addresses(self, params: dict):
        """
        Retrieve (or generate a new) deposit addresses for a particular asset and method.
        https://docs.kraken.com/rest/#operation/getDepositAddresses

        Parameters
        ----------
        asset: string (required)
            Asset being deposited
        method: string (required)
            Name of the deposit method
        new: boolean
            Whether or not to generate new addresses
            Default: False
        :return:

        Returns
        -------
        Response: depositAddress <Array>
            address: string
                Deposit Address
            expiretm: string
                Expiration time in unix timestamp, or - if not expiring
            new: boolean
                Whether or not address had ever been used
        """
        return self.kraken_request(self.API_DEPOSIT_ADDRESSES, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def getDepositStatus(self, params: dict):
        """
        Retrieve information about recent deposits made
        https://docs.kraken.com/rest/#operation/getStatusRecentDeposits

        Parameters
        ----------
        asset: string (required)
            Asset being deposited
        method: string
            Name of the deposit method
        :returns:

        Returns
        -------
        Response: Deposit <Array>
            Method: string
                Name of deposit method
            aclass: string
                Asset class
            asset: string
                Asset
            refid: string
                Reference ID
            txid: string
                Method transaction ID
            info: string
                Method transaction information
            amount: string
                Amount deposited
            fee: any
                Fees paid
            time: integer <int32>
                Unix timestamp when request was made
            status: any
                Status of deposit
            status-prop: string
                Addition status Properties
                Enum:
                    "return" - A return transaction initiated by Kraken
                    "onhold" - Deposit is on hold pending review
        """
        return self.kraken_request(self.API_DEPOSIT_STATUS, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def get_withdrawal_information(self, params: dict):
        """
        Retrieve fee information about potential withdrawals for a particular asset, key and amount
        https://docs.kraken.com/rest/#operation/getWithdrawalInformation

        Parameters
        ----------
        asset: string (required)
            Asset being withdrawn
        key: string (required)
            Withdrawal key name, as set up on your account
        amount: string (required)
            Amount to be withdrawn
        :return:

        Returns
        -------
        Response: withdrawalInfo
            method: string
                Name of the withdrawal method that will be used
            limit: string
                Maximum net amount that can be withdrawn right now
            amount: string
                New amount that will be sent, after fees
            fee: string
                Amount of fees that will be paid
        """
        return self.kraken_request(self.API_WITHDRAWAL_INFO, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def withdraw_funds(self, params: dict):
        """
        Make a withdrawal request
        https://docs.kraken.com/rest/#operation/withdrawFunds

        Parameters
        ----------
        asset: string (required)
            Asset being withdrawn
        key: string (required)
            Withdrawal key name, as set up on your account
        amount: string (required)
            Amount to be withdrawn
        :return:

        Returns
        -------
        Response: object
            refid: string
                Reference ID
        """
        return self.kraken_request(self.API_WITHDRAW_FUNDS, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def get_withdrawal_status(self, params: dict):
        """
        Retrieve information about recent request withdrawals
        https://docs.kraken.com/rest/#operation/getStatusRecentWithdrawals

        Parameters
        ----------
        asset: string (required)
            Asset being withdrawn
        method: string
            Name of the withdrawal method
        :return:

        Returns
        -------
        Response: Withdrawal <Array>
            method: string
                Name of the withdrawal method
            aclass: string
                Asset class
            asset: string
                Asset
            refid: string
                References ID
            txid: string
                Method transaction ID
            info: string
                Mehtod transaction information
            amount: string
                Amount withdrawn
            fee: any
                Fees paid
            time: integer <int32>
                Unix timestamp when request was made
            status: string
                Status of withdraw
                Enum: "Initial" "Pending" "Settled" "Success" "Failure"
            status-prop: string
                Additional status properties (if available)
                Enum:
                    "cancel-pending" - cancelation requested
                    "canceled" - canceled
                    "cancel-denied" - cancelation requested but was denied
                    "return" - a return transaction initiated by Kraken; it cannot be canceled
                    "onhold" - withdrawal is on hold pending review
        """
        return self.kraken_request(self.API_WITHDRAW_STATUS, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def cancel_withdraw(self, params: dict):
        """
        Cancel a recently requested withdrawal, if it has not already been successfully processed
        https://docs.kraken.com/rest/#operation/cancelWithdrawal

        Parameters
        ----------
        asset: string (required)
            Asset being withdrawn
        refid: string (required)
            Withdrawal reference ID
        :returns:

        Returns
        -------
        Response: boolean
            Whether cancellation was successful or not
        """
        return self.kraken_request(self.API_WITHDRAW_CANCEL, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def request_wallet_transfer(self, params: dict):
        """
        Transfer from Kraken spot wallet to Kraken Futures holding wallet. Note that a transfer in the
        other direction must be requested via the Kraken Futures API endpoint.
        https://docs.kraken.com/rest/#operation/walletTransfer

        Parameters
        ----------
        asset: string (required)
            Asset to transfer (asset ID or altname)
        from: string (required)
            Source wallet
            Value: "Spot Wallet"
        to: string (required)
            Destination wallet
            Value: "Futures Wallet"
        amount: string (required)
            Amount to transfer
        :returns:

        Returns
        -------
        Response: object
            refid: string
                Reference ID
        """
        return self.kraken_request(self.API_WALLET_TRANSFER, {
            "nonce": str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    # ------------
    # User Staking
    # ------------
    def stake_asset(self, params: dict):
        """
        Stake an asset from your spot wallet. This operation requires an API key with Withdraw funds permission.
        https://docs.kraken.com/rest/#operation/stake

        Parameters
        ----------
        asset: string (required)
            Asset tp stake (asset ID or altname)
        amount: string (required)
            Amount of the asset to stake
        method: string (required)
            Name of the staking option to use
            (refer to the Staking Assets endpoint for the correct method names for each asset)
        :returns:

        Returns
        -------
        Response: object
            refid: string
                Reference ID
        """
        return self.kraken_request(self.API_STAKE_ASSET, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def unstake_asset(self, params: dict):
        """
        Unstake an asset from your staking wallet. This operation requires an API key with Withdraw funds permission.
        https://docs.kraken.com/rest/#operation/unstake

        Parameters
        ----------
        asset: string (required)
            Asset to unstake (ass ID or altname). Must be a valid staking asset (e.g. XBT.M, XTZ.S, ADA.S)
        amount: string (required)
            Amount of the asset to unstake
        :returns:
        Returns
        -------
        Response: object
            refid: string
                Reference ID
        """
        return self.kraken_request(self.API_UNSTAKE_ASSET, {
            'nonce': str(int(1000 * time.time())),
            **params
        }, API_KEY, API_SEC)

    def list_stakeable_assets(self):
        """
        Returns the list of assets that the user is able to stake. This operation requires and
        API key with both Withdraw funds and Query funds permission
        https://docs.kraken.com/rest/#operation/getStakingAssetInfo

        Returns
        -------
        Response: Array of objects <Staking Asset Information>
            asset: string (required)
                Asset code/name
            satking_asset: string (required)
                Staking asset code/name
            method: string
                Unique ID of the staking option (used in Stake/Unstake operations)
            on_chain: boolean
                Whether the staking operation is on-chain or not
                Default: True
            can_stake: boolean
                Whether the staking operation is on-chain or not
                Default: True
            can_unstake: boolean
                Whether the user will be able to unstake this asset
                Default: True
            minimum_amount: object
                Minimum amounts for staking/unstaking
                unstaking: string
                    Default: "0"
                staking: string
                    Default: "0"
            lock: object
                Describes the locking periods and percentages for staking/unstaking operations
                unstaking: Array
                    days: integer
                        Days the funds are locked
                    percentage: integer
                        Percentage of the funds that are locked (0-100)
                staking: Array
                    days: integer
                        Days the funds are locked
                    percentage: integer
                        Percentage of the funds that are locked (0-100)
                lockup: Array
                    days: integer
                        Days the funds are locked
                    percentage: integer
                        Percentage of the funds that are locked (0-100)
            enabled_for_user: boolean
                Default: True
            disabled: boolean
            rewards: object
                Describes the rewards earned while staking
                reward: string
                    Reward earned while staking
                type: string
                    Reward type
                    Value: "percentage"
        """
        return self.kraken_request(self.API_LIST_STAKING_ASSETS, {
            'nonce': str(int(1000 * time.time())),
        }, API_KEY, API_SEC)

    def list_pending_staking_transactions(self):
        """
        Returns the list of pending staking transactions. Once resolved,
        these transactions will appear on the List of Staking Transactions endpoint.
        This operation requires an API key with both Query funds and Withdraw funds permissions.
        https://docs.kraken.com/rest/#operation/getStakingPendingDeposits

        Returns
        -------
        Response: Array (Staking Transaction Info)
            ref: string
                The reference ID of the transaction.
            type: string
                Enum: "bonding" "reward" "unbonding"
                The type of transaction.
            asset: string
                Asset code/name
            amount: string
                The transaction amount
            time: string
                Unix timestamp when the transaction was initiated.
            bond_start: integer
                Unix timestamp from the start of bond period (applicable only to bonding transactions).
            bond_end: integer
                Unix timestamp of the end of bond period (applicable only to bonding transactions).
            status: string
                Enum: "Initial" "Pending" "Settled" "Success" "Failure"
                Transaction status
        """
        return self.kraken_request(self.API_STAKE_PENDING, {
            'nonce': str(int(1000 * time.time())),
        }, API_KEY, API_SEC)

    def list_staking_transactions(self):
        """
        Returns the list of all staking transactions.
        This endpoint can only return up to 1000 of the most recent transactions.
        This operation requires an API key with Query funds permissions.
        https://docs.kraken.com/rest/#operation/getStakingTransactions

        Returns
        -------
        Response: Array
            refid: string
                The reference ID of the transaction.
            type: string
                Enum: "bonding" "reward" "unbonding"
                The type of transaction.
            asset: string
                Asset code/name
            amount: string
                The transaction amount
            time: string
                Unix timestamp when the transaction was initiated.
            bond_start: integer
                Unix timestamp from the start of bond period (applicable only to bonding transactions).
            bond_end: integer
                Unix timestamp of the end of bond period (applicable only to bonding transactions).
            status: string
                Enum: "Initial" "Pending" "Settled" "Success" "Failure"
                Transaction status
        """
        return self.kraken_request(self.API_STAKING_TRANSACTIONS, {
            'nonce': str(int(1000 * time.time())),
        }, API_KEY, API_SEC)

    # -------------------------
    # Websocket Authentications
    # -------------------------
    def get_websocket_token(self):
        """
        An authentication token must be requested via this REST API endpoint in order to connect to and authenticate
        with our Websockets API. The token should be used within 15 minutes of creation, but it does not expire once
        a successful Websockets connection and private subscription has been made and is maintained.
        The 'Access WebSockets API' permission must be enabled for the
        API key in order to generate the authentication token.
        https://docs.kraken.com/rest/#tag/Websockets-Authentication

        Returns
        -------
        Response: object
            token: string
                Websockets token

            expires: integer
                Time (in seconds) after which the token expires
        """
        return self.kraken_request(self.API_WEBSOCKET_TOKEN, {
            'nonce': str(int(1000 * time.time())),
        }, API_KEY, API_SEC)
