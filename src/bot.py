from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.stream import TradingStream
from src.config import Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY
from src.trading_methods import methods

'''
This is a trading bot that specifically runs once every trading day
and will make its trades as soon as the bell opens.
One can choose a specific method of determining which stocks to buy
from their liking.
The point of the bot is to determine if the stock choices made by one
method is better than the others.
'''
def main():
    trader = methods()    
    while True:
        valid_choices = ("r", "a", "m")
        choice = input("Enter what method to choose (reddit: R, algorithmic: A, or machine learning: M): ").lower()
        if choice not in valid_choices:
            print("Please Enter a Valid Choice!")
        else:
            break
    if choice == "r":
        trading_client = TradingClient(Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
        stock_client = StockHistoricalDataClient(Reddit_ALPACA_API_KEY,  Reddit_ALPACA_SECRET_KEY)
        stream = TradingStream(Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, paper=True)
        trader.reddit_mode(trading_client, stock_client, stream)
    elif choice == "a":
        trading_client = TradingClient(Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, paper=True) # paper=True enables paper trading
        stock_client = StockHistoricalDataClient(Algo_ALPACA_API_KEY,  Algo_ALPACA_SECRET_KEY)
        stream = TradingStream(Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, paper=True)
        trader.algo_mode(trading_client, stock_client, stream)
    else:
        trading_client = TradingClient(Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, paper=True)
        stock_client = StockHistoricalDataClient(Neural_ALPACA_API_KEY,  Neural_ALPACA_SECRET_KEY)
        stream = TradingStream(Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, paper=True)
        trader.neural_mode(trading_client, stock_client, stream)

if __name__  == "__main__":
    main()