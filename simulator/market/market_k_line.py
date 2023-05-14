import pandas as pd


class MarketKLinesDataFrame(pd.DataFrame):
    open_timestamp_millis: pd.Series[int]
    open_price: pd.Series[float]
