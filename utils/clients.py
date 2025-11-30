# Importing modules
import asyncio
from decouple import config as env_config
from alpaca.data.requests import CryptoBarsRequest, NewsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical.news import NewsClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import CryptoHistoricalDataClient
from datetime import datetime



API_KEY = env_config("KEY")
SECRET_KEY = env_config("SECRET")

data_client = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)
news_client = NewsClient(API_KEY, SECRET_KEY)
trading_client = TradingClient(API_KEY, SECRET_KEY)