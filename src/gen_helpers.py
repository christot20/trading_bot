import socket
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import yfinance as yf
from db_intializer import db
from config import REMOTE_SERVER


class operations: 

    def __init__(self, stock_client, trading_client, db_name):
        self.trading_client = trading_client
        self.db_name = db_name
        self.stock_client = stock_client

    @staticmethod
    def is_connected(hostname): # used to make sure connection to internet is made before calling apis
        status = False
        while status == False:
            # https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python by miraculixx
            try: 
                # see if we can resolve the host name -- tells us if there is
                # a DNS listening
                host = socket.gethostbyname(hostname)
                # connect to the host -- tells us if the host is actually reachable
                s = socket.create_connection((host, 80), 2) # ((host, port), timeout) where port 80 = http
                s.close()
                status = True
            except Exception:
                # print("Retrying...")
                # time.sleep(5)
                pass # we ignore any errors, returning False

    def buyer(self, stocks): # used to buy stocks using alpaca-py api
        db_execute = []
        executer = db(self.db_name) # execute buying to be recorded in db
        for stock in stocks:
            operations.is_connected(REMOTE_SERVER)
            stock_info = yf.Ticker(stock).info
            acc_value = self.trading_client.get_account()
            market_price = float(stock_info['regularMarketPrice']) # price of stock 
            # print(market_price, acc_value.buying_power)
            print(market_price, acc_value.cash)
            amount = int((float(acc_value.cash ) * .005)//(market_price)) # amount of stock to buy (roughly enough to buy 10 stocks a day for a month)
            print(stock, " ", amount)                                       # I give each account 500k just in case it wants to buy an expensive stocks
            if float(market_price) * amount < float(acc_value.cash) and (float(market_price) * amount )> 0: # checks if possible to buy stock (i use available cash to avoid margin)
                operations.is_connected(REMOTE_SERVER)
                # Market order
                market_order_data = MarketOrderRequest(
                            symbol=stock, # maybe do (buying_power)//(stock_price * 100)
                            qty=amount, # gonna want to determine quantity based on amount of $ in acc and price per share
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.DAY
                            )
                # Market order
                market_order = self.trading_client.submit_order(
                                order_data=market_order_data
                            )
                db_execute.append((stock, "BUY", amount, market_price, market_order.submitted_at, self.trading_client.get_account().portfolio_value))
            else:
                continue
        executer.table_inserter(db_execute)


    def seller(self, stocks): # used to sell stocks using alpaca-py api
        executer = db(self.db_name) # execute selling to be recorded in db
        for stock in stocks:
            operations.is_connected(REMOTE_SERVER)
            stock_info = yf.Ticker(stock).info
            # time.sleep(2) # let stock info load
            market_price = float(stock_info['regularMarketPrice'])
            db_execute = []
            operations.is_connected(REMOTE_SERVER)
            sell = self.trading_client.close_position(stock) # sells positions based on price diff %
            print(sell) # use for logging transactions (do same with buys for ur db)
            db_execute.append((sell.symbol, "SELL", int(sell.qty), market_price, sell.submitted_at, self.trading_client.get_account().portfolio_value))
            executer.table_inserter(db_execute)