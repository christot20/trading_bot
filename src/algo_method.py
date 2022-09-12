import numpy as np
import pandas as pd
import requests
from scipy import stats
from statistics import mean
from tqdm import tqdm
# from datapackage import Package
from src.config import IEX_CLOUD_API_TOKEN
from src.specific_helpers import the_algo
from src.gen_helpers import operations

# maybe try to make this a class?
def algo_mode(trading_client, stock_client):
    #Instantiate Reddit Mode and Helpers
    money_maker = the_algo()
    buy_sell = operations(stock_client, trading_client, "algo_method")
    # call upon apewisdom api to get stocks most actively talked about
    stocks = money_maker.stock_finder()
    # buy and sell stocks
    buy_sell.streamer(stocks)


# '''
# Going to make a new strategy based on:
# 1. Price-to-earnings ratio
# 2. Price-to-book ratio
# 3. Price-to-sales ratio
# 4. Enterprise Value divided by Earnings Interest, Taxes, Depreciation, and Amoritization (EV/EBITDA)
# 5. Enterprise Value divided by Gross Profit (EV/GP)

# Strategy influenced by algorithmic trading with python by freecodecamp: https://www.youtube.com/watch?v=xfzGZB4HhEE
# '''

# rv_columns = [  # columns of pandas DF
#     'Ticker',
#     'Price',
#     'Price-to-Earnings Ratio',
#     'PE Percentile',
#     'Price-to-Book Ratio',
#     'PB Percentile',
#     'Price-to-Sales Ratio',
#     'PS Percentile',
#     'EV/EBITDA',
#     'EV/EBITDA Percentile',
#     'EV/GP',
#     'EV/GP Percentile',
#     'RV Score'
# ]

# rv_dataframe = pd.DataFrame(columns = rv_columns) # pandas DF

# data = pd.read_csv(f"src/nasdaq_stock_list.csv")   # stocks to analyze
# stocks = data["Symbol"].tolist() 

# appender = [] # used to add each row using concat
# for symbol in tqdm(stocks, desc="Loading"):
#     try:
#         batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,advanced-stats&token={IEX_CLOUD_API_TOKEN}' # api call to get IEX info
#         data = requests.get(batch_api_call_url).json() # IEX data
#         enterprise_value = data[symbol]['advanced-stats']['enterpriseValue']
#         ebitda = data[symbol]['advanced-stats']['EBITDA']
#         gross_profit = data[symbol]['advanced-stats']['grossProfit']
#     except: # Key error or JSON request error
#         continue
    
#     try:
#         ev_to_ebitda = enterprise_value/ebitda
#     except TypeError: # used if value is None, N/A
#         ev_to_ebitda = np.NaN
    
#     try:
#         ev_to_gross_profit = enterprise_value/gross_profit
#     except TypeError: # used if value is None, N/A
#         ev_to_gross_profit = np.NaN


#     df_new_row = pd.Series(
#         [
#             symbol,
#             data[symbol]['quote']['latestPrice'],
#             data[symbol]['quote']['peRatio'],
#             'N/A',
#             data[symbol]['advanced-stats']['priceToBook'],
#             'N/A',
#             data[symbol]['advanced-stats']['priceToSales'],
#             'N/A',
#             ev_to_ebitda,
#             'N/A',
#             ev_to_gross_profit,
#             'N/A',
#             'N/A'
#         ], 
#         index=rv_columns
#     ) 
#     appender.append(df_new_row)  
# rv_dataframe = pd.concat(appender, axis=1, ignore_index=True).T  # dataframe with values

# for column in ['Price-to-Earnings Ratio', 'Price-to-Book Ratio','Price-to-Sales Ratio',  'EV/EBITDA', 'EV/GP']:
#     rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace = True)  # fill N/A values with average of each column (datapoint)

# metrics = {  # used to make calculating percentiles easier
#             'Price-to-Earnings Ratio': 'PE Percentile',
#             'Price-to-Book Ratio':'PB Percentile',
#             'Price-to-Sales Ratio': 'PS Percentile',
#             'EV/EBITDA':'EV/EBITDA Percentile',
#             'EV/GP':'EV/GP Percentile'
# }

# for row in rv_dataframe.index: # iterate over each row in DF
#     # print(row)
#     for metric in metrics.keys(): # uses keys so that if value is needed just use metrics[metric]
#         rv_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(rv_dataframe[metric], rv_dataframe.loc[row, metric])/100  # get percentile of each stock

# for row in rv_dataframe.index: # iterate over each stock in pandas by row index
#     value_percentiles = []
#     for metric in metrics.keys(): # iterate over metrics
#         value_percentiles.append(rv_dataframe.loc[row, metrics[metric]]) # append each percentile to list
#     rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles) # get average from each percentile of that stock to find RV score

# rv_dataframe.sort_values(by = 'RV Score', inplace = True) # sort by RV score
# rv_dataframe = rv_dataframe[:10] # get top 10 values
# rv_dataframe.reset_index(drop = True, inplace = True) # drop other values

# stock_list = rv_dataframe.Ticker.values.tolist()  # list of stocks in top 10

# #Print the entire DataFrame    
# print(rv_dataframe)
# print(len(rv_dataframe))
# print(stock_list)