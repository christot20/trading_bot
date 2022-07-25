import alpaca_trade_api as api
from alpaca_trade_api.stream import Stream
from helpers import *
from config import BASE_URL, ALPACA_API_KEY, ALPACA_SECRET_KEY, data_feed
# use pip-compile to get stuff for requirements .txt
# use piprqs --force to get base packages   

# Instantiate REST API Connection
alpaca_client = api.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

# obtain account information
account = alpaca_client.get_account()
print(account)

symbol = "BTCUSD"
timeframe = "1Day"
start = "2022-01-01"
end = "2022-01-31"
btc_bars = alpaca_client.get_crypto_bars(symbol, timeframe, start, end).df
print(btc_bars.head())  

stream = Stream(ALPACA_API_KEY,
                ALPACA_SECRET_KEY,
                base_url=BASE_URL,
                data_feed=data_feed)

async def bar_callback(b):
    print(b)

# Subscribing to bar event
symbol = "BTCUSD"
stream.subscribe_crypto_bars(bar_callback, symbol)

stream.run()