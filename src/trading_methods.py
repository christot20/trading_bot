from src.specific_helpers import the_reddit, the_algo, the_net
from src.gen_helpers import operations

class methods:
    '''
    This class holds all the methods for running each specific type 
    of trading methodology as well as buying and selling each
    of the stocks they choose and connecting the actions to a 
    MYSQL local database.
    '''
    def reddit_mode(self, trading_client, stock_client):
        money_maker = the_reddit() # instance of reddit method 
        buy_sell = operations(stock_client, trading_client, "reddit_method") # buy and sell and monitor functions
        # call upon apewisdom api to get stocks most actively talked about
        buy_list, sell_list = money_maker.api_method(trading_client) 
        print(buy_list)
        print(sell_list)
        # buy and sell stocks
        buy_sell.buyer(buy_list)
        buy_sell.seller(sell_list)

    def algo_mode(self, trading_client, stock_client):
        money_maker = the_algo() # instance of algo method 
        buy_sell = operations(stock_client, trading_client, "algo_method") # buy and sell and monitor functions
        # find stocks using algo method
        buy_list, sell_list = money_maker.stock_finder(trading_client)
        print(buy_list)
        print(sell_list)
        # buy and sell stocks
        buy_sell.buyer(buy_list)
        buy_sell.seller(sell_list)   

    def neural_mode(self, trading_client, stock_client):
        money_maker = the_net() # instance of net method 
        buy_sell = operations(stock_client, trading_client, "net_method") # buy and sell and monitor functions
        # use neural net to choose stocks
        buy_list, sell_list = money_maker.stock_chooser(trading_client)
        print(buy_list)
        print(sell_list)
        # buy and sell stocks
        buy_sell.buyer(buy_list)
        buy_sell.seller(sell_list) # maybe change all these to singular function in bot.py? have the object instance and db as parameter?
