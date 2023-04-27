from datetime import date
import pandas as pd

from binance import binance_k_line_repository


def load_tickers(
    symbol: str,
    date_from: date,
    date_to: date,
    bid_ask_spread: float,
) -> pd.DataFrame:
    k_lines = binance_k_line_repository.load_k_lines(symbol, date_from, date_to)
    return pd.DataFrame(
        {
            "timestamp": k_lines.open_timestamp_millis,
            "bid_price": k_lines.open_price,
            "ask_price": k_lines.open_price + bid_ask_spread,
        }
    )
