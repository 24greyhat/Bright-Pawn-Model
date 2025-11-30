import pandas as pd
from .clients import (
    trading_client,
    data_client,
    news_client,
    CryptoBarsRequest,
    TimeFrame,
    TimeFrameUnit
)



class Data:
    def __init__(self):
        self.trading = trading_client
        self.data = data_client
        self.news = news_client



    def fetch_bars(self, symbol: str, start: str = None, limit: int = 1000, days: int = 1):
        if start is None:
            start = "2020-01-01"

        req = CryptoBarsRequest(
            symbol_or_symbols=symbol,
            start=start,
            timeframe= TimeFrame(days, TimeFrameUnit(TimeFrameUnit.Day)),
            limit=limit
        )

        bars = self.data.get_crypto_bars(req)

        bars = bars.df

        bars = bars[['open', 'high', 'low', 'close', 'volume']]
        bars.index.name = "datetime"
        return bars


