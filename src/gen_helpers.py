import socket
import time
import datetime
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.common.exceptions import APIError
from db_intializer import db
from config import REMOTE_SERVER

class operations: 
    '''
    This class contains general functions used by many of the functions/methods
    written in this program. These are the buying and selling functions as well
    as a static method used to check if the machine is currently connected to the
    internet as to not be disrupted when making api calls.
    '''
    def __init__(self, stock_client, trading_client, stream, db_name):
        self.trading_client = trading_client
        self.db_name = db_name
        self.stock_client = stock_client
        self.stream = stream

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
    
    def db_logger(self, choice):
        time.sleep(10)
        db_execute = []
        executer = db(self.db_name) # execute selling to be recorded in db
        today = datetime.date.today()
        if choice == "BUY":
            # time.sleep(4000)
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
            db_execute.insert(0, (order.symbol, choice, order.filled_qty, order.filled_avg_price, order.filled_at - datetime.timedelta(hours=4, minutes=0), self.trading_client.get_account().portfolio_value))
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
                                symbol=stock, # maybe do (buying_power)//(stock_price * 100)
                                qty=amount, # gonna want to determine quantity based on amount of $ in acc and price per share
                                side=OrderSide.BUY,
                                time_in_force=TimeInForce.DAY
                                )
                    # Market order
                    market_order = self.trading_client.submit_order(
                                    order_data=market_order_data
                                )
                    print(market_order)
            except APIError:
                continue
        self.db_logger("BUY")

    def seller(self, stocks): # used to sell stocks using alpaca-py api
        for stock in stocks:
            try:
                operations.is_connected(REMOTE_SERVER)
                sell = self.trading_client.close_position(stock) # sells positions based on price diff %
                print(sell) # use for logging transactions (do same with buys for ur db)
            except APIError:
                continue
        self.db_logger("SELL")

    # def buyer(self, stocks): # used to buy stocks using alpaca-py api
    #     # db_execute = []
    #     for stock in stocks:
    #         try:
    #             operations.is_connected(REMOTE_SERVER)
    #             acc_value = self.trading_client.get_account()
    #             request_params = StockLatestQuoteRequest(symbol_or_symbols=stock) 
    #             latest_quote = self.stock_client.get_stock_latest_quote(request_params)
    #             ask_price = float(latest_quote[stock].ask_price)
    #             print(ask_price)
    #             print(latest_quote)
    #             print(ask_price, acc_value.buying_power)

    #             # stock_info = yf.Ticker(stock).info   
    #             # market_price = float(stock_info['regularMarketPrice']) # price of stock 
    #             # print(market_price, acc_value.buying_power)
    #             # print(market_price, acc_value.cash)

    #             amount = int((float(acc_value.buying_power ) * .005)//(ask_price)) # amount of stock to buy (roughly enough to buy 10 stocks a day for a month)
    #             print(stock, " ", amount)   # I give each account 500k just in case it wants to buy an expensive stocks
    #             # if float(ask_price) * amount < float(acc_value.buying_power) and (float(ask_price) * amount) > 0: # checks if possible to buy stock 
    #             if float(ask_price) * amount > 0: # checks if possible to buy stock 
    #                 operations.is_connected(REMOTE_SERVER)
    #                 # price = self.streamer(amount)
    #                 # Market order
    #                 market_order_data = MarketOrderRequest(
    #                             symbol=stock, # maybe do (buying_power)//(stock_price * 100)
    #                             qty=amount, # gonna want to determine quantity based on amount of $ in acc and price per share
    #                             side=OrderSide.BUY,
    #                             time_in_force=TimeInForce.DAY
    #                             )
    #                 # Market order
    #                 market_order = self.trading_client.submit_order(
    #                                 order_data=market_order_data
    #                             )
    #                 print(market_order)
    #         except APIError:
    #             continue
    #     #         price = self.streamer(amount)
    #     #         # print("buy price: ", price)
    #     #         db_execute.append((stock, "BUY", amount, price, market_order.submitted_at, self.trading_client.get_account().portfolio_value))
    #     #     # else:
    #     #     #     continue
    #     self.db_logger("BUY")

    # def seller(self, stocks): # used to sell stocks using alpaca-py api
    #     # db_execute = []
    #     for stock in stocks:
    #         # operations.is_connected(REMOTE_SERVER)
    #         # amount = [int(ticker.qty) for ticker in self.trading_client.get_all_positions() if ticker.symbol == stock][0]
    #         # amount = 0
    #         # for ticker in self.trading_client.get_all_positions():
    #         #     if ticker.symbol == stock:
    #         #         amount = int(ticker.qty)
    #         # stock_info = yf.Ticker(stock).info
    #         # market_price = float(stock_info['regularMarketPrice'])
    #         operations.is_connected(REMOTE_SERVER)
    #         sell = self.trading_client.close_position(stock) # sells positions based on price diff %
    #         # price = self.streamer(int(sell.qty))
    #         # print("sell price: ", price)
    #         print(sell) # use for logging transactions (do same with buys for ur db)
    #     #     db_execute.append((sell.symbol, "SELL", int(sell.qty), price, sell.submitted_at, self.trading_client.get_account().portfolio_value))
    #     self.db_logger("SELL")

    # def streamer(self, amount):
    #     async def trade_updates_callback(data: any):
    #         await asyncio.sleep(2)
    #         # print("on")
    #         global qty
    #         order = data.order
    #         #if qty == 0:
    #         qty += int(order.filled_qty) - qty
    #         # else:
    #         #     qty = qty + ()
    #         price = float(order.filled_avg_price)
    #         order_avg.append(float(price))
    #         print(order)
    #         # print(qty)
    #         if qty == amount:
    #             await self.stream.stop_ws()

    #     global qty 
    #     qty = 0
    #     order_avg = []
    #     # print(amount)
    #     self.stream.subscribe_trade_updates(trade_updates_callback)
    #     # x = threading.Thread(target = self.stream.run())
    #     # x.start()
    #     self.stream.run()
    #     self.stream.stop()
    #     # x.join()
    #     return sum(order_avg) / len(order_avg)

    # def buyer(self, stocks): # used to buy stocks using alpaca-py api
    #     db_execute = []
    #     executer = db(self.db_name) # execute buying to be recorded in db
    #     while stocks:
    #         try:
    #             stock = stocks[0]
    #             operations.is_connected(REMOTE_SERVER)
    #             stock_info = yf.Ticker(stock).info
    #             acc_value = self.trading_client.get_account()
    #             market_price = float(stock_info['regularMarketPrice']) # price of stock 
    #             print(market_price, acc_value.buying_power)
    #             # print(market_price, acc_value.cash)
    #             amount = int((float(acc_value.buying_power ) * .005)//(market_price)) # amount of stock to buy (roughly enough to buy 10 stocks a day for a month)
    #             print(stock, " ", amount)                                       # I give each account 500k just in case it wants to buy an expensive stocks
    #             if float(market_price) * amount < float(acc_value.buying_power) and (float(market_price) * amount) > 0: # checks if possible to buy stock 
    #                 operations.is_connected(REMOTE_SERVER)
    #                 # Market order
    #                 market_order_data = MarketOrderRequest(
    #                             symbol=stock, # maybe do (buying_power)//(stock_price * 100)
    #                             qty=amount, # gonna want to determine quantity based on amount of $ in acc and price per share
    #                             side=OrderSide.BUY,
    #                             time_in_force=TimeInForce.DAY
    #                             )
    #                 # Market order
    #                 market_order = self.trading_client.submit_order(
    #                                 order_data=market_order_data
    #                             )
    #                 db_execute.append((stock, "BUY", amount, market_price, market_order.submitted_at, self.trading_client.get_account().portfolio_value))
    #             del stocks[0]
    #             print(stocks)
    #             print(market_order)
    #         except:
    #             print("retrying")
    #             continue
    #     executer.table_inserter(db_execute)
    
    # def seller(self, stocks): # used to sell stocks using alpaca-py api
    #     executer = db(self.db_name) # execute selling to be recorded in db
    #     db_execute = []
    #     while stocks:
    #         try: 
    #             print(stocks)
    #             stock = stocks[0]
    #             operations.is_connected(REMOTE_SERVER)
    #             stock_info = yf.Ticker(stock).info
    #             # time.sleep(2) # let stock info load
    #             market_price = float(stock_info['regularMarketPrice'])
    #             operations.is_connected(REMOTE_SERVER)
    #             sell = self.trading_client.close_position(stock) # sells positions based on price diff %
    #             print(sell) # use for logging transactions (do same with buys for ur db)
    #             db_execute.append((sell.symbol, "SELL", int(sell.qty), market_price, sell.submitted_at, self.trading_client.get_account().portfolio_value))
    #             del stocks[0]
    #             print(stocks)
    #         except:
    #             print("retrying")
    #             continue
    #     executer.table_inserter(db_execute)