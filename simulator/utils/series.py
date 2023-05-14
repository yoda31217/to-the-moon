from typing import TypeVar
import pandas as pd

T = TypeVar("T", float, int)


def avg(series: pd.Series[T]) -> float:
    return series.mean()  # pyright: ignore [reportUnknownMemberType]


def sum(series: pd.Series[T]) -> T:
    return series.sum()  # pyright: ignore [reportUnknownMemberType]


def min(series: pd.Series[T]) -> T:
    return series.min()  # pyright: ignore [reportUnknownMemberType]


def max(series: pd.Series[T]) -> T:
    return series.max()  # pyright: ignore [reportUnknownMemberType]


def cumsum(series: pd.Series[T]) -> pd.Series[T]:
    return series.cumsum()  # pyright: ignore [reportUnknownMemberType]
