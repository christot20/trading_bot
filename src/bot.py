from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from src.config import Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY
from src.trading_methods import methods

def main():
    # paper=True enables paper trading
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
        trader.reddit_mode(trading_client, stock_client)
        # keep_running() # used to monitor activity manually
    elif choice == "a":
        trading_client = TradingClient(Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, paper=True)
        stock_client = StockHistoricalDataClient(Algo_ALPACA_API_KEY,  Algo_ALPACA_SECRET_KEY)
        trader.algo_mode(trading_client, stock_client)
        # keep_running()
    else:
        trading_client = TradingClient(Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, paper=True)
        stock_client = StockHistoricalDataClient(Neural_ALPACA_API_KEY,  Neural_ALPACA_SECRET_KEY)
        trader.neural_mode(trading_client, stock_client)
        # keep_running()

if __name__  == "__main__":
    main()