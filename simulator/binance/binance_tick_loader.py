import pandas as pd
from pandas import DataFrame, Series


def load_binance_ticks(k_lines_data_frame: DataFrame, ask_bid_price_difference: float):
    new_var: Series[int] = k_lines_data_frame.open_timestamp_millis
    return pd.DataFrame(
        {
            "timestamp": new_var,
            "bid_price": k_lines_data_frame.open_price,
            "ask_price": k_lines_data_frame.open_price + ask_bid_price_difference,
        }
    )
