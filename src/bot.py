from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from src.config import Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY
from src.trading_methods import methods
import time

# look at how to set up your code/organize like that guy did with ai bot
# start trying to have it make trades as a test and try to learn how to use an AI for it later
# def keep_running():
#     while True:
#         time.sleep(1)

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




    # # Instantiate REST API Connection
    # alpaca_client = api.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

    # # obtain account information
    # account = alpaca_client.get_account()
    # print(account)
    # print(account.cash) # use ths notation for getting stuff you need for acc

    # symbol = "BTCUSD" # for historical data
    # timeframe = "1Day"
    # start = "2022-01-01"
    # end = date.today() # gets current day
    # btc_bars = alpaca_client.get_crypto_bars(symbol, timeframe, start, end).df
    # print(btc_bars)  

    # print(alpaca_client.get_asset(symbol))

    # # make a market order
    # qty = 1
    # order = alpaca_client.submit_order(symbol, qty=qty, side="sell") # change to buy to buy
    # print(order)

    # stream = Stream(ALPACA_API_KEY, # for realtime data
    #                 ALPACA_SECRET_KEY,
    #                 base_url=BASE_URL,
    #                 data_feed=data_feed)

    # async def bar_callback(b):
    #     print(b)

    # # Subscribing to bar event
    # symbol = "BTCUSD"
    # stream.subscribe_crypto_bars(bar_callback, symbol)

    # stream.run()
