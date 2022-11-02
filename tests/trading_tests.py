# run pytest .\tests\trading_tests.py
from alpaca.trading.client import TradingClient
from src.config import Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY
from src.specific_helpers import the_reddit, the_algo, the_net

def test_reddit():
    money_maker = the_reddit()
    trading_client = TradingClient(Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
    buy_list, sell_list = money_maker.api_method(trading_client) 
    assert len(buy_list) == 10 and isinstance(sell_list, list) # check if it does choose 10 stocks to buy and has a list of sell stocks
        
def test_algo():
    money_maker = the_algo()
    trading_client = TradingClient(Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, paper=True)
    buy_list, sell_list = money_maker.stock_finder(trading_client) 
    assert len(buy_list) == 10 and isinstance(sell_list, list) # check if it does choose 10 stocks to buy and has a list of sell stocks

def test_neural():
    money_maker = the_net()
    trading_client = TradingClient(Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, paper=True)
    buy_list, sell_list = money_maker.stock_chooser(trading_client) 
    assert len(buy_list) == 10 and isinstance(sell_list, list) # check if it does choose 10 stocks to buy and has a list of sell stocks