from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient

from src.config import ALPACA_API_KEY, ALPACA_SECRET_KEY
from src.reddit_method import reddit_mode

# look at how to set up your code/organize like that guy did with ai bot
# start trying to have it make trades as a test and try to learn how to use an AI for it later

if __name__  == "__main__":
    # paper=True enables paper trading
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
    # used for stock data 
    stock_client = StockHistoricalDataClient(ALPACA_API_KEY,  ALPACA_SECRET_KEY)    
    while True:
        valid_choices = ("r", "a", "m")
        choice = input("Enter what method to choose (algorithmic: A, reddit: R, or machine learning: M): ").lower()
        if choice not in valid_choices:
            print("Please Enter a Valid Choice!")
        else:
            break
    if choice == "r":
        reddit_mode(trading_client, stock_client)
    elif choice == "a":
        pass
    else:
        pass # M choice




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
