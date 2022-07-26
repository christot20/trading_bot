import alpaca_trade_api as api
import matplotlib.pyplot as plt
import pandas as pd
from alpaca_trade_api.stream import Stream
from datetime import date, timedelta
from ..src.helpers import *
from ..src.config import BASE_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY, data_feed

# run using python -m bot.src.main
# use pip-compile to get stuff for requirements .txt
# use pipreqs --force to get base packages   
# use pip install -r requirements.txt to run

# look at how to set up your code/organize like that guy did with ai bot
# start trying to have it make trades as a test and try to learn how to use an AI for it later

def main():
    # Instantiate REST API Connection
    alpaca_client = api.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')
    account = alpaca_client.get_account()
    print(account)

    STOCK_DATA = pd.DataFrame()
    while len(STOCK_DATA) == 0:
        try:
            stock = input("Enter a stock ticker: ")
            STOCK_DATA = alpaca_client.get_bars(stock, '1Day', (date.today()-timedelta(days=30)).isoformat()).df # getting 30 day avg
        except:
            pass    

    print(STOCK_DATA)
    # Plot stock price data
    plot = STOCK_DATA.plot(y="close", use_index=True, legend=False)
    plot.set_xlabel("Date")
    plot.set_ylabel(f"{stock.upper()} Close Price ($)")
    plt.show()
    


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
