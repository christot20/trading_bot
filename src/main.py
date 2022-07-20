import alpaca_trade_api as tradeapi
from helpers import *

# API info
BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_API_KEY = "PKBB1M233ZVNY0RVWFS7"
ALPACA_SECRET_KEY = "CYn6R3eylmUJq0xyVD8QRy4FauwPd7mwE7wCg8JG"

# Instantiate REST API Connection
api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

# obtain account information
account = api.get_account()
print(account)