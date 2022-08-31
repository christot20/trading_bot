import requests
from nltk.corpus import stopwords


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
        self.url = "https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1" # url to send request to
    
    def stock_finder(self, false_positives, stocks): # returns set from hot and top stocks to choose from
        top_stocks, hot_stocks = [], [] # used to store stocks to buy
        for value in stocks:
            if len(top_stocks) == 3 and len(hot_stocks) == 2:
                break

            mentions = 0 if value['mentions'] == None else value['mentions'] # used for perc diff if being talked about a lot
            past_mentions = 0 if value['mentions_24h_ago'] == None else value['mentions_24h_ago']
        
            if "ETF" in value['name'].upper() or "TRUST" in value['name'].upper() or value['ticker'] in false_positives: # check to see if in portfolio, Ignore ETFs and slang and stopwords
                continue # issues with getting stuff like HE, LFG, RC, FOR, etc., slang and stopwords used for that
            if len(top_stocks) < 3: # top stocks finder
                top_stocks.append(value['ticker'])
            try:    
                perc_diff = ((int(mentions) - int(past_mentions)) / int(past_mentions)) * 100 # perc diff of mentions
                if perc_diff > 100 and len(hot_stocks) < 2 and value['ticker'] not in top_stocks: # hot stocks finder
                    hot_stocks.append(value['ticker'])
            except:
                pass

        return (top_stocks + hot_stocks) # list of stocks

    def api_method(self, current_positions): 
        r =  requests.get(self.url) # send request to api
        data = r.json() # raw api data
        stocks = list(data.values())[3] # stocks to check
        false_positives = set(self.slang + self.stop + current_positions)
        return self.stock_finder(false_positives, stocks) # final list of stocks to buy

class the_algo:
    
    def __init__(self):
        pass

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
