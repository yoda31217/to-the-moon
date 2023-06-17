import pandas as pd

from simulator.utils.series import TypedSeries


class MarketKLinesDataFrame(pd.DataFrame):
    open_timestamp_millis: TypedSeries[int]
    open_price: TypedSeries[float]
