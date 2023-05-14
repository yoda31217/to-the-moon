from typing import TypeVar
import pandas as pd

T = TypeVar("T", float, int)


def avg(series: pd.Series[T]) -> float:
    return series.mean()  # pyright: ignore


def sum(series: pd.Series[T]) -> T:
    return series.sum()  # pyright: ignore
