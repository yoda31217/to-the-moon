from datetime import date
from typing import cast
import pandas as pd

from binance import binance_k_line_repository
from market.market_ticker import MarketTikersDataFrame


def load_tickers(
    symbol: str,
    date_from: date,
    date_to: date,
    bid_ask_spread: float,
) -> MarketTikersDataFrame:
    k_lines = binance_k_line_repository.load_k_lines(symbol, date_from, date_to)
    data_frame = pd.DataFrame(
        {
            "timestamp": k_lines.open_timestamp_millis,
            "bid_price": k_lines.open_price,
            "ask_price": k_lines.open_price + bid_ask_spread,
        }
    )
    return cast(MarketTikersDataFrame, data_frame)
