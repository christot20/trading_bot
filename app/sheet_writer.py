import time  
import datetime
import pandas as pd
from alpaca.trading.client import TradingClient
from src.gen_helpers import operations
from src.config import Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, PROJECT_PATH, REMOTE_SERVER

'''
This is a little script I made to 
monitor each accounts' value throughout the
day so that it could be used for visualizations
in my streamlit webapp. Does so by making a csv
of each minute with the account value of each account.
'''
 
r_trading_client = TradingClient(Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
a_trading_client = TradingClient(Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
m_trading_client = TradingClient(Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts


################################################################################################# is to get account data for line charts (WORKS!!!)
today = datetime.date.today()
year = today.year
month = today.month
day = today.day
# print(datetime.datetime(year, month, day, 9, 30, 0) + datetime.timedelta(minutes=30, hours=7))

# creation of dataframe for the day
df = pd.DataFrame(
    {
        "Date": pd.date_range(
            start=datetime.datetime(year, month, day, 4, 0, 0), end=datetime.datetime(year, month, day, 20, 0, 0), freq="T", closed="left"
        )
    }
)
# creating columns for each account
df["Reddit Account Value"] = None
df["Algo Account Value"] = None
df["Neural Account Value"] = None

for i in range(0, len(df)): # filling in each column with account data
    operations.is_connected(REMOTE_SERVER)
    df.at[i,"Reddit Account Value"] = r_trading_client.get_account().portfolio_value
    df.at[i,"Algo Account Value"] = a_trading_client.get_account().portfolio_value
    df.at[i,"Neural Account Value"] = m_trading_client.get_account().portfolio_value
    df.to_csv(f"{PROJECT_PATH}/app/acc_data.csv", encoding='utf-8')
    time.sleep(60)