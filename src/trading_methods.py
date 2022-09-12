from src.specific_helpers import the_reddit
from src.specific_helpers import the_algo
from src.gen_helpers import operations

class methods:

    def reddit_mode(self, trading_client, stock_client):
        #Instantiate Reddit Mode and Helpers
        money_maker = the_reddit()
        buy_sell = operations(stock_client, trading_client, "reddit_method")
        # call upon apewisdom api to get stocks most actively talked about
        # stocks = money_maker.api_method([stock.symbol for stock in trading_client.get_all_positions()])
        stocks = money_maker.api_method() # got rid of current positions when buying stocks
        # buy and sell stocks
        buy_sell.streamer(stocks)

    def algo_mode(self, trading_client, stock_client):
        #Instantiate Reddit Mode and Helpers
        money_maker = the_algo()
        buy_sell = operations(stock_client, trading_client, "algo_method")
        # call upon apewisdom api to get stocks most actively talked about
        stocks = money_maker.stock_finder()
        # buy and sell stocks
        buy_sell.streamer(stocks)