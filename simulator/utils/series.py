import pandas as pd


def avg(series: pd.Series[int | float]):
    return series.mean()  # pyright: ignore
