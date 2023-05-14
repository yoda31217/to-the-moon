from typing import TypeVar
import pandas as pd

T = TypeVar("T", float, int)


def avg(series: pd.Series[T]) -> float:
    return series.mean()  # pyright: ignore


def sum(series: pd.Series[T]) -> T:
    return series.sum()  # pyright: ignore


def min(series: pd.Series[T]) -> T:
    return series.min()  # pyright: ignore


def max(series: pd.Series[T]) -> T:
    return series.max()  # pyright: ignore
