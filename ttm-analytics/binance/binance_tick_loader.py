import pandas as pd
from pandas import DataFrame


def load_binance_ticks(k_lines_data_frame: DataFrame, ask_bid_price_difference: float):
    return pd.DataFrame({
        'timestamp_millis': k_lines_data_frame.open_timestamp_millis,
        'bid_price': k_lines_data_frame.open_price,
        'ask_price': k_lines_data_frame.open_price + ask_bid_price_difference,
    })
