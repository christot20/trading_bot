import matplotlib.pyplot as plt
import pandas as pd

from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockLatestQuoteRequest

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

import time
from datetime import date, timedelta
from helpers import the_reddit

# maybe try to make this a class?
def reddit_mode(trading_client, stock_client):
    #Instantiate Reddit Mode and Helpers
    money_maker = the_reddit()
    # Instantiate REST API Connection
    stocks = money_maker.api_method([stock.symbol for stock in trading_client.get_all_positions()])

    money_maker.buyer(trading_client, stock_client, stocks, "reddit_method")
            # money_maker.seller(stock, trading_client, current_positions, .1)
    
    current_positions = {stock.symbol : stock.avg_entry_price for stock in trading_client.get_all_positions()}
    money_maker.streamer(current_positions, trading_client, "reddit_method") # have it check positions periodically
    # pass a status parameter through reddit mode for on and off to determine if streamer should be called






    # for stock in stocks:
    #     request_params = StockBarsRequest(
    #                             symbol_or_symbols=stock,
    #                             timeframe=TimeFrame.Day,
    #                             start=str((date.today()-timedelta(days=30)).isoformat())
    #                     )
    #     bars = stock_client.get_stock_bars(request_params).df
    #     # convert to dataframe
    #     print(bars)
    #     plot = bars.plot(y="close", use_index=True, legend=False)
    #     plot.set_xlabel("Date")
    #     plot.set_ylabel(f"{stock.upper()} Close Price ($)")
    #     plt.show()


    # for stock in stocks:
    #     STOCK_DATA = alpaca_client.get_bars(stock, '1Day', (date.today()-timedelta(days=30)).isoformat()).df # getting 30 day avg
        
    #     order = alpaca_client.submit_order(stock, qty=1, side="buy") # change to buy to buy/ sell to sell
    #     print(order)
        
    #     # print(STOCK_DATA)
    #     # Plot stock price data
    #     plot = STOCK_DATA.plot(y="close", use_index=True, legend=False)
    #     plot.set_xlabel("Date")
    #     plot.set_ylabel(f"{stock.upper()} Close Price ($)")
    #     plt.show()

        # streamer()

# def reddit_mode(alpaca_client):
#     # do something to check if it is 9:30 to 4 and if it is a weekday so it can trade
#     # also do something so that it's checking the url every 5 mins

#     # Maybe make powershell script to start (python .\src\bot.py) and stop (ctrl + c) the bot
#     # at certain times? (9:30 to 4 on weekdays)
#     # then use while true for this whole function and have stuff for making it work above (i.e. classes and helpers)

#     url = "https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1"
#     r =  requests.get(url)
#     data = r.json()
#     stocks = list(data.values())[3]
#     print(stocks[:10]) # IF ETF OR TRUST IN STRING IGNORE IT
#     main(alpaca_client)

    
            ### PROBABLY GONNA NEED A POWERSHELL SCRIPT TO START THIS THING AND HAVE IT END ON ITS OWN
            # OR MAKE A POWERSHELL SCRIPT TO START AND END IT
            # if that's the case, have it check if it is a weekday as well so it doesnt run when it shouldnt
#print(sorted(data, key=data.get, reverse=True)[:5])


