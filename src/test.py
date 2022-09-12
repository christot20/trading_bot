from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY


# client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

# # paper=True enables paper trading
# trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

# # multi symbol request - single symbol is similar


# market_order_data = MarketOrderRequest(
#                             symbol="AMC", # maybe do (buying_power)//(stock_price * 100)
#                             qty=1, # gonna want to determine quantity based on amount of $ in acc and price per share
#                             side=OrderSide.BUY,
#                             time_in_force=TimeInForce.DAY
#                             )
#                 # Market order
# market_order = trading_client.submit_order(
#         order_data=market_order_data
#     )
# print(market_order)

# multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["AMC", "AMC", "TSLA"])

# latest_multisymbol_quotes = client.get_stock_latest_quote(multisymbol_request_params)

# gld_latest_ask_price = latest_multisymbol_quotes["AMC"]
# print(gld_latest_ask_price)

import requests
from nltk.corpus import stopwords
import pandas as pd

# def __init__(self):
#     self.slang = [  # more should be constantly added
#         'YOLO', 'BUY', 'SELL', 'LFG', 'SHORT', 'LONG', 'WSB', 'HOLD', 'BAG', 'HYPE', 'BET', 'HODL',
#         'BULL', 'BEAR', 'LOSS', 'GAIN', 'FTW', 'APE', 'APES', 'OP', 'DD', 'CEO', 'OTM', 'WSB1', 'WSB2',
#         'WSB3', 'IV', 'LMAO', 'RC', 'RYAN', 'COHEN', 'MOON', 'IRS', 'TAX', 'FOMO', 'CPI', 'PM', 'F', 'U',
#         'ITM', 'RIP', 'LOL', 'AH', 'PUT', 'CALL', 'GO', 'BABY', 'NFT', 'HANDS', 'SEC', 'LINK', 'OH', 'RSI',
#         'WSB4', 'WSB5', 'WSB6', 'WSB7', 'WSB8', 'WSB9', 'WSB10', 'WTF', 'BTFO', 'ATH', 'DRS', 'WTH', 'DTC', 'IMO'
#         'ATM', 'AI', 'FUD', 'YTD', 'GET', 'OG', 'TLDR', 'FED'
#     ]
#     self.stop = [word.upper() for word in set(stopwords.words('english'))]
#     self.url = "https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1" # url to send request to
    
# def stock_finder(self, false_positives, stocks): # returns set from hot and top stocks to choose from
#     top_stocks, hot_stocks = [], [] # used to store stocks to buy
#     for value in stocks:
#         if len(top_stocks) == 3 and len(hot_stocks) == 2:
#             break

#         mentions = 0 if value['mentions'] == None else value['mentions'] # used for perc diff if being talked about a lot
#         past_mentions = 0 if value['mentions_24h_ago'] == None else value['mentions_24h_ago']
    
#         if "ETF" in value['name'].upper() or "TRUST" in value['name'].upper() or value['ticker'] in false_positives: # check to see if in portfolio, Ignore ETFs and slang and stopwords
#             continue # issues with getting stuff like HE, LFG, RC, FOR, etc., slang and stopwords used for that
#         if len(top_stocks) < 3: # top stocks finder
#             top_stocks.append(value['ticker'])
#         try:    
#             perc_diff = ((int(mentions) - int(past_mentions)) / int(past_mentions)) * 100 # perc diff of mentions
#             if perc_diff > 100 and len(hot_stocks) < 2 and value['ticker'] not in top_stocks: # hot stocks finder
#                 hot_stocks.append(value['ticker'])
#         except:
#             pass

#     return (top_stocks + hot_stocks) # list of stocks

# def api_method(self, current_positions): 
#     r =  requests.get(self.url) # send request to api
#     data = r.json() # raw api data
#     stocks = list(data.values())[3] # stocks to check
#     false_positives = set(self.slang + self.stop + current_positions)
#     return self.stock_finder(false_positives, stocks) # final list of stocks to buy

slang = [  # more should be constantly added
        'YOLO', 'BUY', 'SELL', 'LFG', 'SHORT', 'LONG', 'WSB', 'HOLD', 'BAG', 'HYPE', 'BET', 'HODL',
        'BULL', 'BEAR', 'LOSS', 'GAIN', 'FTW', 'APE', 'APES', 'OP', 'DD', 'CEO', 'OTM', 'WSB1', 'WSB2',
        'WSB3', 'IV', 'LMAO', 'RC', 'RYAN', 'COHEN', 'MOON', 'IRS', 'TAX', 'FOMO', 'CPI', 'PM', 'F', 'U',
        'ITM', 'RIP', 'LOL', 'AH', 'PUT', 'CALL', 'GO', 'BABY', 'NFT', 'HANDS', 'SEC', 'LINK', 'OH', 'RSI',
        'WSB4', 'WSB5', 'WSB6', 'WSB7', 'WSB8', 'WSB9', 'WSB10', 'WTF', 'BTFO', 'ATH', 'DRS', 'WTH', 'DTCC', 'IMO'
        'ATM', 'AI', 'FUD', 'YTD', 'GET', 'OG', 'TLDR', 'FED', 'JPOW', 'ROTH', 'AMA'
    ]
stop = [word.upper() for word in set(stopwords.words('english'))]
false_positives = set(slang + stop)

def data_cleaner(dicti):
    if dicti['mentions'] == None:
        dicti['mentions'] = 0
    if dicti['mentions_24h_ago'] == None:  # used later when determining POP score, better to be 0 than N/A
        dicti['mentions_24h_ago'] = 0
    if "ETF" in dicti['name'].upper() or "TRUST" in dicti['name'].upper() or dicti['ticker'] in false_positives: # removes commonly found words/WSB slang from dataframe
        # print(dicti['name'], " ", dicti['ticker'])
        return None
    return dicti

r =  requests.get("https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1") # send request to api
data = r.json() # raw api data
stocks = list(data.values())[3] # stocks to check

reddit_columns = [
    'Rank',
    'Ticker',
    'Name',
    'Mentions',
    'Upvotes',
    '24hr Rank Change',
    '24hr Mentions',
    'POP Score'
]
reddit_df = pd.DataFrame(columns = reddit_columns)
appender = []
for dicti in stocks:  

    pop_score = (int(dicti['upvotes']) / int(dicti['mentions'])) / int(dicti['rank']) # I like this

    dicti = data_cleaner(dicti)
    if dicti == None:
        continue

    df_new_row = pd.Series(
        [
            int(dicti['rank']),
            dicti['ticker'],
            dicti['name'],
            int(dicti['mentions']),
            int(dicti['upvotes']),
            int(dicti['rank_24h_ago']),
            int(dicti['mentions_24h_ago']),
            pop_score
        ], 
        index=reddit_columns
    ) 
    appender.append(df_new_row)  
reddit_df = pd.concat(appender, axis=1, ignore_index=True).T
reddit_df.sort_values(by='POP Score', inplace = True, ascending=False)
print(reddit_df)
