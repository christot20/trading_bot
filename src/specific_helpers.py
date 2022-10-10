import requests
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
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

    Certain stocks come up due to the nature of finding stocks, letters in all caps and with $ behind them, when they shouldn't and create false positives
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

    def api_method(self, trading_client): 
        r =  requests.get(self.url) # send request to api
        data = r.json() # raw api data
        stocks = list(data.values())[3] # stocks to check
        false_positives = set(self.slang + self.stop)
        # return self.stock_finder(false_positives, stocks) # final list of stocks to buy
        positions = [stock.symbol for stock in trading_client.get_all_positions()]
        buy_list = self.stocker(false_positives, stocks)
        buy_list, sell_list = self.stock_seller(buy_list, positions)
        return buy_list, sell_list

    def stock_seller(self, buy_list, positions):
        sell_list = []
        for stock in positions:
            if stock not in buy_list:
                sell_list.append(stock)
        return buy_list, sell_list

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
        # reddit_df.sort_values(by='POP Score', inplace = True, ascending=False)
        reddit_df = reddit_df.sort_values(by='POP Score', ascending=False)
        new_reddit_df = reddit_df[:10] # get top 10 values
        # reddit_df.reset_index(drop = True, inplace = True) # drop other values
        new_reddit_df = new_reddit_df.reset_index(drop = True) # drop other values
        # print(new_reddit_df)

        stock_list = new_reddit_df.Ticker.values.tolist()  # list of stocks in top 10
        # print(stock_list)
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
        self.stock_data = pd.read_csv(f"datasets/sp500_companies_test.csv")   # stocks to analyze
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
            # rv_dataframe = rv_dataframe[column].fillna(rv_dataframe[column].mean())  # fill N/A values with average of each column (datapoint)

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

        # rv_dataframe.sort_values(by = 'RV Score', inplace = True) # sort by RV score
        rv_dataframe = rv_dataframe.sort_values(by = 'RV Score') # sort by RV score
        return rv_dataframe
    
    def stock_seller(self, positions, buy_list, df):
        sell_list = []
        for stock in set().union(positions, buy_list):
            result = df.loc[df["Ticker"] == stock]
            if result["RV Score"].values > .2:
                if stock in buy_list:
                    buy_list.remove(stock)
                if stock in positions:
                    sell_list.append(stock)
        return buy_list, sell_list

    def stock_finder(self, trading_client):
        rv_dataframe = self.df_initializer()
        rv_dataframe = self.df_fixer(rv_dataframe)
        # print(rv_dataframe)
        
        new_rv_dataframe = rv_dataframe[:10] # get top 10 values
        # rv_dataframe.reset_index(drop = True, inplace = True) # drop other values     #### MAKE THE LIST OF STOCKS DF SEPEARTE FROM RVDF, USE RV DF TO KNOW WHEN TO SELL STOCKS
        new_rv_dataframe = new_rv_dataframe.reset_index(drop = True) # drop other values

        buy_list = new_rv_dataframe.Ticker.values.tolist()  # list of stocks in top 10

        positions = [stock.symbol for stock in trading_client.get_all_positions()] # current positions
        buy_list, sell_list = self.stock_seller(positions, buy_list, rv_dataframe) # final stocks to buy and sell
        return buy_list, sell_list

class the_net:

    '''
    Neural Net Strategy based on:
    Inputs:
        1. Matrix of prices from intervals given by num_days_predict
        2. Price of next day after num_days_predict interval to predict
    Outputs:
        1. "Accuracy" of each model run of stock time series (RMSE, MPAE, MAE)
        2. Predicted Stock Price for Next Day based on training and testing data

    Stocks are then chosen based on a dataframe with the "value" score being determined by: (perc_chng / abs(perc_chng * accuracy_avg)) / accuracy_avg   
    This is just the accuracy of each model with those that predict the price going up being higher than those predicting it to go down
    The more accurate the model was at predicting the stock's price and higher the % change from last close, the higher the value
    
    The The Neural Net Model Used is a Stacked LSTM Structure (https://machinelearningmastery.com/stacked-long-short-term-memory-networks/)
    LSTM proves to be very effective and accurate when predicting time series, hence why it was chosen
    NASDAQ csv up to date as of 9/10/2022

    Strategy influenced by Stock Price Prediction Using Python & Machine Learning by Computer Science: https://www.youtube.com/watch?v=QIUxPv5PJOY
    '''

    def __init__(self):
        self.columns = [  # columns of pandas DF
                    'Ticker',
                    'Predicted Price',
                    'Percent Diff', # diff from last close
                    'Accuracy',
                    'Value'
                ]
        self.stock_data = pd.read_csv(f"datasets/sp500_companies_test.csv")
        self.stocks = self.stock_data["Symbol"].tolist()        
        self.num_days_predict = 60 # amount of days used to predict next day

    def train_data(self, scaled_data, data_cut):
        train_data = scaled_data[0:data_cut, :] # these rows, all columns

        x_train = [train_data[i-self.num_days_predict:i, 0] for i in range(self.num_days_predict, len(train_data))] # independent training features (last 14 values based on i)
        y_train = [train_data[i, 0] for i in range(self.num_days_predict, len(train_data))] # dependent (target) variables (15th value to predict)

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) # samples, timesteps, features (must be 3d for lstm)
        return x_train, y_train

    def test_data(self, data, scaled_data, data_cut):
        test_data = scaled_data[data_cut-self.num_days_predict: , :] # last quarter of data

        x_test = [test_data[i-self.num_days_predict:i, 0] for i in range(self.num_days_predict, len(test_data))] # last 14 values
        y_test = data[data_cut: , :] # values we want model to predict (normal dataset vals) (last quarter)

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        return x_test, y_test

    def predict_data(self, dataset, scaler):
        last_x_days = dataset[-self.num_days_predict:].values
        xdays_test = [scaler.transform(last_x_days)]
        xdays_test = np.array(xdays_test)
        xdays_test = np.reshape(xdays_test, (xdays_test.shape[0], xdays_test.shape[1], 1))
        return xdays_test
    
    def stock_predictor(self):
        gen_stock_appender = []
        for stock in tqdm(self.stocks, desc="Loading..."):
            try:
                dataset = yf.Ticker(stock) # stock
                dataset = dataset.history(period="5Y") # stock data
                dataset = dataset.filter(["Close"]) # make dataframe of stock close prices
                data_cut = (len(dataset) * 3) // 4 # used to cut data into training and testing
                data = dataset.values # convert train data to numpy array
                    
                scaler = MinMaxScaler(feature_range=(0, 1)) # scale data (normalize to help model) from 0 to 1
                scaled_data = scaler.fit_transform(data)

                x_train, y_train = self.train_data(scaled_data, data_cut) # training data
                
                # Build Stacked LSTM
                model = Sequential()
                model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1))) # timesteps and features, first layers needs input shape
                model.add(LSTM(64, return_sequences=False)) # no more LSTM models so return sequence is false
                model.add(Dense(32)) # regular dense layer
                model.add(Dropout(0.2)) # KEEP MESSING WITH LAYERS AND AMOUNT OF DAYS TO PREDICT
                model.add(Dense(1))  # output layer
                model.compile(optimizer="adam", loss="mean_squared_error") # adam optimizer, mse loss
                # batch size is total number of training examples present in batch
                # epochs are number of iterations an entire dataset is passed forward and backward a Neural net (kind of like for loop)
                # https://github.com/keras-team/keras/issues/1007 used to get rid of loading bars, remove verbose otherwise
                model.fit(x_train, y_train, batch_size=56, epochs=1, verbose=0) # Train model
                
                x_test, y_test = self.test_data(data, scaled_data, data_cut) # testing (validation) data

                # get model predicted values
                predictions = model.predict(x_test, verbose=0)
                predictions = scaler.inverse_transform(predictions) # unscaling values

                # evaluate model with RMSE, MAE, and MPAE for model accuracy
                # https://stats.stackexchange.com/questions/458366/how-would-you-judge-the-performance-of-an-lstm-for-time-series-predictions
                rmse = np.sqrt(np.mean(((predictions - y_test)**2)))
                mae = np.mean(abs(predictions - y_test))
                mpae = np.mean(abs((predictions - y_test) / y_test)) * 100 

                # predict next day using last x days
                xdays_test = self.predict_data(dataset, scaler) # prediction data
                pred_price = model.predict(xdays_test, verbose=0)

                pred_price = scaler.inverse_transform(pred_price)[0][0] # predicted price
                last_price = dataset[-1:].values[0][0] # last close
                perc_chng = ((pred_price - last_price) / last_price) * 100 # perc chng of prediction from close
                accuracy_avg = np.mean(np.array([rmse, mae, mpae])) # accuracy of model

                df_new_row = pd.Series( # add to dataframe
                                [
                                    stock,
                                    pred_price,
                                    perc_chng,
                                    accuracy_avg,
                                    perc_chng / accuracy_avg  # (perc_chng / abs(perc_chng * accuracy_avg)) / accuracy_avg (was finicking with size of dataset, structure of net, and value eq)
                                ], 
                                index=self.columns
                            ) 
            except: # if yf doesn't retrieve data for the stock insert NA into df
                df_new_row = pd.Series(
                            [
                                stock,
                                float("NaN"),
                                float("NaN"),
                                float("NaN"),
                                float("NaN")
                            ], 
                            index=self.columns
                        ) 
            gen_stock_appender.append(df_new_row)
        return gen_stock_appender

    def stock_seller(self, positions, buy_list, df):
        sell_list = []
        for stock in set().union(positions, buy_list):
            result = df.loc[df["Ticker"] == stock]
            if result["Value"].values < 0:
                if stock in buy_list:
                    buy_list.remove(stock)
                if stock in positions:
                    sell_list.append(stock)
        return buy_list, sell_list

    def stock_chooser(self, trading_client):
        gen_stock_df = pd.DataFrame(columns = self.columns)
        gen_stock_appender = self.stock_predictor()

                 
        gen_stock_df = pd.concat(gen_stock_appender, axis=1, ignore_index=True).T  # dataframe with values
        gen_stock_df = gen_stock_df.sort_values(by='Value', ascending=False)

        new_stock_df = gen_stock_df[:10] # get top 10 values
        new_stock_df = new_stock_df.reset_index(drop = True) # drop other values

        buy_list = new_stock_df.Ticker.values.tolist()  # list of stocks in top 10
        # print(gen_stock_df.to_string())
        # print(new_stock_df)
        # print(stock_list)

        positions = [stock.symbol for stock in trading_client.get_all_positions()] # current positions
        buy_list, sell_list = self.stock_seller(positions, buy_list, gen_stock_df) # final stocks to buy and sell
        return buy_list, sell_list

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
