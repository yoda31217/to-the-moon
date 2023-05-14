import pandas as pd


class KLinesDataFrame(pd.DataFrame):
    open_timestamp_millis: pd.Series[int]
    open_price: pd.Series[float]
