import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
from nltk.corpus import stopwords
from scipy import stats
from statistics import mean
from src.config import IEX_CLOUD_API_TOKEN


class the_reddit:
    '''
    Consumer Sentiment (reddit) Strategy based on:
    1. Amount of mentions stock has
    2. Upvotes of each stock
    3. Rank compared to other stocks
    
    Simple formula used to calculate popularity: (upvotes / mentions) / rank
    This is the POP score

    Certian stocks come up due to the nature of finding stocks, letters in all caps and with $ behind them, when they shouldn't and create false positives
    NLTK stopwords and my own small list of words tries to filter and fix this issue
    '''
    
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
        self.url = "https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1" # url to send request to
        self.reddit_columns = [
                    'Rank',
                    'Ticker',
                    'Name',
                    'Mentions',
                    'Upvotes',
                    '24hr Rank Change',
                    '24hr Mentions',
                    'POP Score'
                ]
    
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

    def api_method(self, current_positions): 
        r =  requests.get(self.url) # send request to api
        data = r.json() # raw api data
        stocks = list(data.values())[3] # stocks to check
        false_positives = set(self.slang + self.stop + current_positions)
        # return self.stock_finder(false_positives, stocks) # final list of stocks to buy
        return self.stocker(false_positives, stocks)

    def data_cleaner(self, false_positives, dicti):
        if dicti['mentions'] == None:
            dicti['mentions'] = 0
        if dicti['mentions_24h_ago'] == None:  # used later when determining POP score, better to be 0 than N/A
            dicti['mentions_24h_ago'] = 0
        if "ETF" in dicti['name'].upper() or "TRUST" in dicti['name'].upper() or dicti['ticker'] in false_positives: # removes commonly found words/WSB slang from dataframe
            # print(dicti['name'], " ", dicti['ticker'])
            return None
        return dicti
    
    def stocker(self, false_positives, stocks):
        reddit_df = pd.DataFrame(columns = self.reddit_columns)
        appender = []
        for dicti in stocks:  

            pop_score = (int(dicti['upvotes']) / int(dicti['mentions'])) / int(dicti['rank']) # I like this

            dicti = self.data_cleaner(false_positives, dicti)
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
                index=self.reddit_columns
            ) 
            appender.append(df_new_row)  
        reddit_df = pd.concat(appender, axis=1, ignore_index=True).T
        reddit_df.sort_values(by='POP Score', inplace = True, ascending=False)
        reddit_df = reddit_df[:10] # get top 10 values
        reddit_df.reset_index(drop = True, inplace = True) # drop other values
        print(reddit_df)

        stock_list = reddit_df.Ticker.values.tolist()  # list of stocks in top 10
        print(stock_list)
        return stock_list





class the_algo:
    '''
    Algorithmic Strategy based on:
    1. Price-to-earnings ratio
    2. Price-to-book ratio
    3. Price-to-sales ratio
    4. Enterprise Value divided by Earnings Interest, Taxes, Depreciation, and Amoritization (EV/EBITDA)
    5. Enterprise Value divided by Gross Profit (EV/GP)

    Takes mean percentile of each category to find "relative value"
    This is the RV score

    NASDAQ csv up to date as of 9/10/2022

    Strategy influenced by algorithmic trading with python by freecodecamp: https://www.youtube.com/watch?v=xfzGZB4HhEE
    '''
    
    def __init__(self):
        self.rv_columns = [  # columns of pandas DF
            'Ticker',
            'Price',
            'Price-to-Earnings Ratio',
            'PE Percentile',
            'Price-to-Book Ratio',
            'PB Percentile',
            'Price-to-Sales Ratio',
            'PS Percentile',
            'EV/EBITDA',
            'EV/EBITDA Percentile',
            'EV/GP',
            'EV/GP Percentile',
            'RV Score'
        ]
        self.stock_data = pd.read_csv(f"src/nasdaq_stock_list.csv")   # stocks to analyze
        self.stocks = self.stock_data["Symbol"].tolist()

    def df_initializer(self):
        rv_dataframe = pd.DataFrame(columns = self.rv_columns) # pandas DF 

        appender = [] # used to add each row using concat
        for symbol in tqdm(self.stocks, desc="Loading"):
            try:
                batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,advanced-stats&token={IEX_CLOUD_API_TOKEN}' # api call to get IEX info
                data = requests.get(batch_api_call_url).json() # IEX data
                enterprise_value = data[symbol]['advanced-stats']['enterpriseValue']
                ebitda = data[symbol]['advanced-stats']['EBITDA']
                gross_profit = data[symbol]['advanced-stats']['grossProfit']
            except: # Key error or JSON request error
                continue
            
            try:
                ev_to_ebitda = enterprise_value/ebitda
            except TypeError: # used if value is None, N/A
                ev_to_ebitda = np.NaN
            
            try:
                ev_to_gross_profit = enterprise_value/gross_profit
            except TypeError: # used if value is None, N/A
                ev_to_gross_profit = np.NaN

            try:
                df_new_row = pd.Series(
                    [
                        symbol,
                        data[symbol]['quote']['latestPrice'],
                        data[symbol]['quote']['peRatio'],
                        'N/A',
                        data[symbol]['advanced-stats']['priceToBook'],
                        'N/A',
                        data[symbol]['advanced-stats']['priceToSales'],
                        'N/A',
                        ev_to_ebitda,
                        'N/A',
                        ev_to_gross_profit,
                        'N/A',
                        'N/A'
                    ], 
                    index=self.rv_columns
                ) 
            except KeyError:
                continue
            appender.append(df_new_row)  
        rv_dataframe = pd.concat(appender, axis=1, ignore_index=True).T  # dataframe with values
        return rv_dataframe
    
    def df_fixer(self, rv_dataframe):
        for column in ['Price-to-Earnings Ratio', 'Price-to-Book Ratio','Price-to-Sales Ratio',  'EV/EBITDA', 'EV/GP']:
            rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace = True)  # fill N/A values with average of each column (datapoint)

        metrics = {  # used to make calculating percentiles easier
                    'Price-to-Earnings Ratio': 'PE Percentile',
                    'Price-to-Book Ratio':'PB Percentile',
                    'Price-to-Sales Ratio': 'PS Percentile',
                    'EV/EBITDA':'EV/EBITDA Percentile',
                    'EV/GP':'EV/GP Percentile'
        }

        for row in rv_dataframe.index: # iterate over each row in DF
            # print(row)
            for metric in metrics.keys(): # uses keys so that if value is needed just use metrics[metric]
                rv_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(rv_dataframe[metric], rv_dataframe.loc[row, metric])/100  # get percentile of each stock

        for row in rv_dataframe.index: # iterate over each stock in pandas by row index
            value_percentiles = []
            for metric in metrics.keys(): # iterate over metrics
                value_percentiles.append(rv_dataframe.loc[row, metrics[metric]]) # append each percentile to list
            rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles) # get average from each percentile of that stock to find RV score

        rv_dataframe.sort_values(by = 'RV Score', inplace = True) # sort by RV score
        return rv_dataframe

    def stock_finder(self):
        rv_dataframe = self.df_initializer()
        rv_dataframe = self.df_fixer(rv_dataframe)
        
        rv_dataframe = rv_dataframe[:10] # get top 10 values
        rv_dataframe.reset_index(drop = True, inplace = True) # drop other values

        stock_list = rv_dataframe.Ticker.values.tolist()  # list of stocks in top 10

        #Print the entire DataFrame    
        print(rv_dataframe)
        print(len(rv_dataframe))
        print(stock_list)
        return stock_list

########################## Old Method for getting stock in reddit
# import praw
# from tqdm import tqdm    ### used for manual method
# import yfinance as yf
# import pandas as pd
# import numpy as np
# import re
# from config import REDDIT_ID, REDDIT_NAME, REDDIT_SECRET


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
