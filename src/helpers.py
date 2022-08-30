import requests
from nltk.corpus import stopwords
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import StockDataStream
from db_intializer import db
from config import REDDIT_ID, REDDIT_NAME, REDDIT_SECRET, ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL


class the_reddit:
    def __init__(self):
        self.slang = [  # more should be constantly added
            'YOLO', 'BUY', 'SELL', 'LFG', 'SHORT', 'LONG', 'WSB', 'HOLD', 'BAG', 'HYPE', 'BET', 'HODL',
            'BULL', 'BEAR', 'LOSS', 'GAIN', 'FTW', 'APE', 'APES', 'OP', 'DD', 'CEO', 'OTM', 'WSB1', 'WSB2',
            'WSB3', 'IV', 'LMAO', 'RC', 'RYAN', 'COHEN', 'MOON', 'IRS', 'TAX', 'FOMO', 'CPI', 'PM', 'F', 'U',
            'ITM', 'RIP', 'LOL', 'AH', 'PUT', 'CALL', 'GO', 'BABY', 'NFT', 'HANDS', 'SEC', 'LINK', 'OH', 'RSI',
            'WSB4', 'WSB5', 'WSB6', 'WSB7', 'WSB8', 'WSB9', 'WSB10', 'WTF', 'BTFO', 'ATH', 'DRS', 'WTH', 'DTC', 'IMO'
            'ATM', 'AI', 'FUD', 'YTD', 'GET', 'OG', 'TLDR', 'FED'
        ]
        self.stop = [word.upper() for word in set(stopwords.words('english'))]

    def api_method(self, current_positions):
        url = "https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1" # url to send reauest to
        r =  requests.get(url) # send request to api
        data = r.json() # raw api data
        stocks = list(data.values())[3] # stocks to check
        top_stocks, hot_stocks = [], [] # used to store stocks to buy
        false_positives = set(self.slang + self.stop + current_positions)
        for value in stocks:
            if len(top_stocks) == 3 and len(hot_stocks) == 2:
                break

            mentions = 0 if value['mentions'] == None else value['mentions']
            past_mentions = 0 if value['mentions_24h_ago'] == None else value['mentions_24h_ago']
        
            if "ETF" in value['name'].upper() or "TRUST" in value['name'].upper() or value['ticker'] in false_positives: # check to see if not in portfolio, Ignore ETFs and slang and stopwords
                continue # issues with getting stuff like HE, LFG, RC, FOR, etc.
            if len(top_stocks) < 3:
                top_stocks.append(value['ticker'])
            perc_diff = ((int(mentions) - int(past_mentions)) / int(past_mentions)) * 100 # perc diff of mentions
            if perc_diff > 100 and len(hot_stocks) < 2 and value['ticker'] not in top_stocks:
                hot_stocks.append(value['ticker'])
            
        top_set, hot_set = set(top_stocks), set(hot_stocks) # change to sets to merge
        return list(top_set.union(hot_set)) # final list of stocks to buy

    def buyer(self, trading_client, latest_multisymbol_quotes, stocks, db_name):
        db_execute = []
        for stock in stocks:
            acc_value = trading_client.get_account()
            latest_ask_price = float(latest_multisymbol_quotes[stock].ask_price) # price of stock (ask)
            amount = int((float(acc_value.buying_power))//(latest_ask_price * 100)) # amount of stock to buy
            print(stock, " ", amount)
            if float(latest_ask_price) * amount < float(acc_value.buying_power): # checks if possible to buy stock
                market_order_data = MarketOrderRequest(
                            symbol=stock, # maybe do (buying_power)//(stock_price * 100)
                            qty=amount, # gonna want to determine quantity based on amount of $ in acc and price per share
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.DAY
                            )

                # Market order
                market_order = trading_client.submit_order(
                                order_data=market_order_data
                            )
                db_execute.append((stock, "BUY", amount, latest_multisymbol_quotes[stock].ask_price, market_order.submitted_at, acc_value.portfolio_value))
            else:
                continue
        executer = db(db_name)
        executer.table_inserter(db_execute)

    def streamer(self, positions, trading_client, db_name): # used 
        wss_client = StockDataStream(ALPACA_API_KEY, ALPACA_SECRET_KEY)
        executer = db(db_name)
        # async handler
        async def quote_data_handler(data: any):
            # quote data will arrive here
            if data.symbol in positions:
                sell_eq = (float(positions[data.symbol]) - float(data.ask_price)) / float(data.ask_price)
                if abs(sell_eq) > .2: # doesn't matter if it's down or up
                    acc_value = trading_client.get_account()
                    db_execute = []
                    sell = trading_client.close_position(data.symbol) # sells positions based on price diff %
                    print(sell) # use for logging transactions (do same with buys for ur db)
                    del positions[data.symbol]
                    db_execute.append((sell.symbol, "SELL", int(sell.qty), float(data.ask_price), sell.submitted_at, acc_value.portfolio_value))
                    executer.table_inserter(db_execute)

        wss_client.subscribe_quotes(quote_data_handler, *list(positions.keys())) # get data for this list of stocks
        wss_client.run()

        # maybe add another method to run in streamer to sell stocks??
        # 50% when 10% down and the rest at 20%? for sellingg even when up?
        # For consistency**
        # MYABE MAKE THIS GENERSL FUNCTION TO USE FOR ALL METHODS
        # BEST WAY TO COMPARE AS ALGO WILL CHOOSE CERTIAN STOCKS AND SO WILL NEURAL NET

        # also make a general func to put in each thing you bought, what price you did, how many, 
        # and when In a MYSQL db


# streamer()
# money_maker = the_reddit()
# print(money_maker.api_method())


########################## Old Method
# import praw
# from tqdm import tqdm    ### used for manual method
# import yfinance as yf
# import pandas as pd
# import numpy as np
# import re

# slang = [  # more should be constantly added
#             'YOLO', 'BUY', 'SELL', 'LFG', 'SHORT', 'LONG', 'WSB', 'HOLD', 'BAG', 'HYPE', 'BET', 'HODL',
#             'BULL', 'BEAR', 'LOSS', 'GAIN', 'FTW', 'APE', 'APES', 'OP', 'DD', 'CEO', 'OTM', 'WSB1', 'WSB2',
#             'WSB3', 'IV', 'LMAO', 'RC', 'RYAN', 'COHEN', 'MOON', 'IRS', 'TAX', 'FOMO', 'CPI', 'PM', 'F', 'U',
#             'ITM', 'RIP', 'LOL', 'AH', 'PUT', 'CALL', 'GO', 'BABY', 'NFT', 'HANDS', 'SEC', 'LINK', 'OH', 'RSI',
#             'WSB4', 'WSB5', 'WSB6', 'WSB7', 'WSB8', 'WSB9', 'WSB10', 'WTF', 'BTFO', 'ATH', 'DRS', 'WTH', 'DTC', 'IMO'
#             'ATM', 'AI', 'FUD', 'DTC', 'YTD', 'GET', 'OG', 'TLDR', 'FED'
#         ]

# def manual_method():
#     def checker(stocks):
#         full_stock_list = []
#         for stock in tqdm(stocks, desc="Please Wait"):
#             ticker = yf.Ticker(stock)
#             try:
#                 if (ticker.info['regularMarketPrice'] == None):
#                     continue
#                 full_stock_list.append(stock)
#             except:
#                 # print(f"Cannot get info of {stock}, it probably does not exist")
#                 continue
            
#             # Got the info of the ticker, do more stuff with it
#             # print(f"Info of {stock}: {info}")
#         return full_stock_list[:10] #lucky seven >:)

#     def iterator(words, post_wrd_freq, slang):
#         '''
#         iterates through block of text and gets word frequency and
#         places into above dictionary
#         '''
#         # NLTK stopwords
#         stop = set(stopwords.words('english'))
#         # Remove punctuation and links
#         # words = re.sub(r"\$[^\]]+", "", words)
#         # words = re.sub(r'[^\w\s]', '', words) # change btween these 2
#         words = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", words) # and this
#         # make lowercase and remove stopwords
#         words = " ".join([word for word in words.split() if word.lower() not in (stop)])
        
#         for word in words.split():
#             # print(word)
#             if (word not in post_wrd_freq and word.isupper()) and word not in slang:
#                 post_wrd_freq[word] = 1
#             elif (word in post_wrd_freq and word.isupper()) and word not in slang:
#                 post_wrd_freq[word] += 1
#     def main():

#         reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent=REDDIT_NAME) 
#         wsb = reddit.subreddit('wallstreetbets')
        
#         post_wrd_freq = {} # dict with words and how many times found
#         posts = [] # used to get posts and turn into df

#         for post in wsb.hot(limit=500):
#             posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
#         posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
#         # print(posts)

#         for column in tqdm(posts["id"]):
#             submission = reddit.submission(id=column)
#             submission.comments.replace_more(limit=0)
#             iterator(posts.loc[posts['id'] == column, 'body'].values[0], post_wrd_freq, slang)
#             for comment in submission.comments.list():
#                 iterator(comment.body, post_wrd_freq, slang)

#             # for top_level_comment in submission.comments:
#             #     if isinstance(top_level_comment, MoreComments):
#             #         continue
#             #     iterator(top_level_comment.body)
#                 # now try to make something to save these bodies and look at what stocks
#                 # are being talked about the most and if buy, sell, and hold is being used with them
#         # print(post_wrd_freq)

#         print(sorted(post_wrd_freq, key=post_wrd_freq.get, reverse=True))
#         print(sorted(post_wrd_freq, key=post_wrd_freq.get, reverse=True)[:5])
#         test_set = (sorted(post_wrd_freq, key=post_wrd_freq.get, reverse=True))[:50]
#         print(checker(test_set))

#     main()

# # manual_method()
