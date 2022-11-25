import socket
import time
import datetime
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.requests import StockLatestQuoteRequest
from src.db_intializer import db
from src.config import REMOTE_SERVER

class operations: 
    '''
    This class contains general functions used by many of the functions/methods
    written in this program. These are the buying and selling functions as well
    as a static method used to check if the machine is currently connected to the
    internet as to not be disrupted when making api calls.
    '''
    def __init__(self, stock_client, trading_client, db_name):
        self.trading_client = trading_client
        self.db_name = db_name
        self.stock_client = stock_client

    @staticmethod
    def is_connected(hostname): # used to make sure connection to internet is made before calling apis
        status = False
        while not status:
            # https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python by miraculixx
            try: 
                # see if we can resolve the host name -- tells us if there is a DNS listening
                host = socket.gethostbyname(hostname)
                # connect to the host -- tells us if the host is actually reachable
                s = socket.create_connection((host, 80), 2) # ((host, port), timeout) where port 80 = http
                s.close()
                status = True
            except Exception:
                print("Retrying...")
                time.sleep(5)
                pass # we ignore any errors, returning False
    
    def db_logger(self, choice): # adds the values into list to be executed into db
        time.sleep(30)
        operations.is_connected(REMOTE_SERVER)
        db_execute = []
        executer = db(self.db_name) # execute selling to be recorded in db
        today = datetime.date.today()
        if choice == "BUY":
            order_side = OrderSide.BUY
        else:
            order_side = OrderSide.SELL
        orders = GetOrdersRequest(
            status="filled",
            side=order_side,
            after=datetime.datetime(today.year, today.month, today.day),
        )
        
        for order in self.trading_client.get_orders(orders):
            print("-------------------------------")
            print(order)
            db_execute.insert(0, (order.symbol, choice, order.filled_qty, order.filled_avg_price, order.filled_at - datetime.timedelta(hours=5, minutes=0), self.trading_client.get_account().portfolio_value))
        executer.table_inserter(db_execute) # insert into db

    def buyer(self, stocks): # used to buy stocks using alpaca-py api
        for stock in stocks:
            try:
                operations.is_connected(REMOTE_SERVER)
                acc_value = self.trading_client.get_account()
                request_params = StockLatestQuoteRequest(symbol_or_symbols=stock) 
                latest_quote = self.stock_client.get_stock_latest_quote(request_params)
                ask_price = float(latest_quote[stock].ask_price)
                print("#############################")
                print(latest_quote)
                print(ask_price, acc_value.buying_power)
                amount = int((float(acc_value.buying_power ) * .005)//(ask_price)) # amount of stock to buy (roughly enough to buy 10 stocks a day for a month)
                print(stock, " ", amount)   # I give each account 500k just in case it wants to buy an expensive stocks
                if float(ask_price) * amount > 0: # checks if possible to buy stock 
                    operations.is_connected(REMOTE_SERVER)
                    # Market order
                    market_order_data = MarketOrderRequest(
                                symbol=stock, 
                                qty=amount, 
                                side=OrderSide.BUY,
                                time_in_force=TimeInForce.DAY
                                )
                    # Market order
                    market_order = self.trading_client.submit_order(
                                    order_data=market_order_data
                                )
                    print(market_order)
            except:
                continue
        self.db_logger("BUY")

    def seller(self, stocks): # used to sell stocks using alpaca-py api
        for stock in stocks:
            try:
                operations.is_connected(REMOTE_SERVER)
                sell = self.trading_client.close_position(stock) # sells positions based on price diff %
                print(sell) # use for logging transactions (do same with buys for ur db)
            except:
                continue
        self.db_logger("SELL")