from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import StockDataStream
import time 
import yfinance as yf
from db_intializer import db
# from config import ALPACA_API_KEY, ALPACA_SECRET_KEY

class operations: 

    def __init__(self, stock_client, trading_client, db_name):
        self.trading_client = trading_client
        self.db_name = db_name
        self.stock_client = stock_client

    def buyer(self, stocks):
        db_execute = []
        executer = db(self.db_name)
        for stock in stocks:
            stock_info = yf.Ticker(stock).info
            acc_value = self.trading_client.get_account()
            market_price = float(stock_info['regularMarketPrice']) # price of stock 
            print(market_price, acc_value.buying_power)
            amount = int((float(acc_value.buying_power))//(market_price * 100)) # amount of stock to buy
            print(stock, " ", amount)
            if float(market_price) * amount < float(acc_value.buying_power): # checks if possible to buy stock
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


    def seller(self, stocks):
        executer = db(self.db_name)
        for stock in stocks:
            stock_info = yf.Ticker(stock).info
            time.sleep(2) # let stock info load
            market_price = float(stock_info['regularMarketPrice'])
            db_execute = []
            sell = self.trading_client.close_position(stock) # sells positions based on price diff %
            print(sell) # use for logging transactions (do same with buys for ur db)
            db_execute.append((sell.symbol, "SELL", int(sell.qty), market_price, sell.submitted_at, self.trading_client.get_account().portfolio_value))
            executer.table_inserter(db_execute)

    # def seller(self, positions, data):
    #     stock_info = yf.Ticker(data.symbol).info
    #     time.sleep(5) # let stock info load
    #     market_price = float(stock_info['regularMarketPrice'])
    #     # print(stock_info)
    #     sell_eq = abs(((float(positions[data.symbol]) - market_price) / market_price) * 100) # determines if to sell or not
    #     if sell_eq > 20: # doesn't matter if it's down or up, 20% is the threshold    # I CHANGED THIS AND AM CHECKING IF THE SQL CMD IS XECUTED IN BY FUNCTION
    #         db_execute = []
    #         sell = self.trading_client.close_position(data.symbol) # sells positions based on price diff %
    #         print(sell) # use for logging transactions (do same with buys for ur db)
    #         db_execute.append((sell.symbol, "SELL", int(sell.qty), market_price, sell.submitted_at, self.trading_client.get_account().portfolio_value))
    #         del positions[data.symbol]
    #         print(positions)
    #         return db_execute

    # def streamer(self, stocks): # TRY TO ADD BUY FUNCTION HERE NOW AND GET POSITIONS
    #     executer = db(self.db_name)
    #     db_execute = self.buyer(stocks)
    #     executer.table_inserter(db_execute)
    #     time.sleep(10) # wait for all positions to load
    #     positions = {stock.symbol : stock.avg_entry_price for stock in self.trading_client.get_all_positions()}
    #     print(positions)
       
    #     wss_client = StockDataStream(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    #     # async handler
    #     async def quote_data_handler(data: any):
    #         # quote data will arrive here
    #         if data.symbol in positions:
    #             db_execute = self.seller(positions, data) # test if this method works with sell, if yes then try to get something to work with the buyer func to be async
    #             executer.table_inserter(db_execute)

    #     wss_client.subscribe_quotes(quote_data_handler, *list(positions.keys())) # get data for this list of stocks
    #     wss_client.run()


# check to see if the value that is being inputted into the database at where u bought and sold is the same when looking at alpaca
# otherwise, try to get something else to get the price of a stock