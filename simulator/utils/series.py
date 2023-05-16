from typing import Generic, Literal, TypeVar
import pandas as pd

T = TypeVar("T", float, int, str)


def sum(series: "pd.Series[T]") -> T:
    return series.sum()  # pyright: ignore [reportUnknownMemberType]


def min(series: "pd.Series[T]") -> T:
    return series.min()  # pyright: ignore [reportUnknownMemberType]


def max(series: "pd.Series[T]") -> T:
    return series.max()  # pyright: ignore [reportUnknownMemberType]


def cumsum(series: "pd.Series[T]") -> "pd.Series[T]":
    return series.cumsum()  # pyright: ignore [reportUnknownMemberType]


class TypedSeries(pd.Series, Generic[T]):  # pyright: ignore [reportMissingTypeArgument]
    def mean(self) -> float:  # pyright: ignore [reportIncompatibleMethodOverride]
        return super().mean()  # pyright: ignore [reportUnknownMemberType]
