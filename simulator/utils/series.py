import pandas as pd


def avg(series: pd.Series[float] | pd.Series[int]):
    return series.mean()  # pyright: ignore
