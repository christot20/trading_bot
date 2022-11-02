import time  
import datetime
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from src.gen_helpers import operations
from src.config import Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, PROJECT_PATH, REMOTE_SERVER

# This is a little script I made to 
# monitor each accounts' value throughout the
# day so that it could be used for visualizations
# in my streamlit webapp.
 
r_trading_client = TradingClient(Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
r_stock_client = StockHistoricalDataClient(Reddit_ALPACA_API_KEY,  Reddit_ALPACA_SECRET_KEY)

a_trading_client = TradingClient(Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
a_stock_client = StockHistoricalDataClient(Algo_ALPACA_API_KEY,  Algo_ALPACA_SECRET_KEY)

m_trading_client = TradingClient(Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
m_stock_client = StockHistoricalDataClient(Neural_ALPACA_API_KEY,  Neural_ALPACA_SECRET_KEY)


################################################################################################# is to get account data for line charts (WORKS!!!)
today = datetime.date.today()
year = today.year
month = today.month
day = today.day
# print(datetime.datetime(year, month, day, 9, 30, 0) + datetime.timedelta(minutes=30, hours=7))


df = pd.DataFrame(
    {
        "Date": pd.date_range(
            start=datetime.datetime(year, month, day, 4, 0, 0), end=datetime.datetime(year, month, day, 20, 0, 0), freq="T", closed="left"
        )
    }
)
df["Reddit Account Value"] = None
df["Algo Account Value"] = None
df["Neural Account Value"] = None
df["Actual Time"] = None

for i in range(0, len(df)):
    operations.is_connected(REMOTE_SERVER)
    df.at[i,"Reddit Account Value"] = r_trading_client.get_account().portfolio_value
    df.at[i,"Algo Account Value"] = a_trading_client.get_account().portfolio_value
    df.at[i,"Neural Account Value"] = m_trading_client.get_account().portfolio_value
    df.at[i,"Actual Time"] = datetime.datetime.now()
    df.to_csv(f"{PROJECT_PATH}/app/acc_data.csv", encoding='utf-8')
    # time.sleep(60)

# i = 0
# while i < len(df):
#     try:
#         operations.is_connected(REMOTE_SERVER)
#         df.at[i,"Reddit Account Value"] = r_trading_client.get_account().portfolio_value
#         df.at[i,"Algo Account Value"] = a_trading_client.get_account().portfolio_value
#         df.at[i,"Neural Account Value"] = m_trading_client.get_account().portfolio_value
#         df.at[i,"Actual Time"] = datetime.datetime.now()
#         df.to_csv(f"{PROJECT_PATH}/src/acc_data.csv", encoding='utf-8')
#         i += 1
#         time.sleep(60)
#     except:
#         continue
#     # print(i)
#################################################################################################