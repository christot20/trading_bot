from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import StockDataStream
from db_intializer import db
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY

class operations: 

    def __init__(self, trading_client, db_name):
        self.trading_client = trading_client
        self.db_name = db_name

    def buyer(self, latest_multisymbol_quotes, stocks):
        db_execute = []
        for stock in stocks:
            acc_value = self.trading_client.get_account()
            latest_ask_price = float(latest_multisymbol_quotes[stock].ask_price) # price of stock (ask)
            amount = int((float(acc_value.buying_power))//(latest_ask_price * 100)) # amount of stock to buy
            print(stock, " ", amount)
            if float(latest_ask_price) * amount < float(acc_value.buying_power): # checks if possible to buy stock
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
                db_execute.append((stock, "BUY", amount, latest_ask_price, market_order.submitted_at, self.trading_client.get_account().portfolio_value))
            else:
                continue
        executer = db(self.db_name)
        executer.table_inserter(db_execute)

    def seller(self, positions, data):
        sell_eq = abs(((float(positions[data.symbol]) - float(data.bid_price)) / float(data.bid_price)) * 100) # determines if to sell or not
        if sell_eq > -1: # doesn't matter if it's down or up, 20% is the threshold
            db_execute = []
            sell = self.trading_client.close_position(data.symbol) # sells positions based on price diff %
            print(sell) # use for logging transactions (do same with buys for ur db)
            db_execute.append((sell.symbol, "SELL", int(sell.qty), float(data.bid_price), sell.submitted_at, self.trading_client.get_account().portfolio_value))
            del positions[data.symbol]
            print(positions)
            return db_execute

    def streamer(self, positions): # TRY TO ADD BUY FUNCTION HERE NOW AND GET POSITIONS
        wss_client = StockDataStream(ALPACA_API_KEY, ALPACA_SECRET_KEY)
        executer = db(self.db_name)
        # async handler
        async def quote_data_handler(data: any):
            # quote data will arrive here
            if data.symbol in positions:
                db_execute = self.seller(positions, data) # test if this method works with sell, if yes then try to get something to work with the buyer func to be async
                executer.table_inserter(db_execute)

        wss_client.subscribe_quotes(quote_data_handler, *list(positions.keys())) # get data for this list of stocks
        wss_client.run()