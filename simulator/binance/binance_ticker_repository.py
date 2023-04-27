from datetime import date
import pandas as pd

from binance.binance_k_line_loader import load_binance_k_lines


def load_tickers(
    symbol: str,
    date_from: date,
    date_to: date,
    bid_ask_spread: float,
) -> pd.DataFrame:
    k_lines = load_binance_k_lines(symbol, date_from, date_to)
    return pd.DataFrame(
        {
            "timestamp": k_lines.open_timestamp_millis,
            "bid_price": k_lines.open_price,
            "ask_price": k_lines.open_price + bid_ask_spread,
        }
    )
