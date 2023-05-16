from typing import Generic, Literal, TypeVar
import pandas as pd

T = TypeVar("T", float, int, str)


def cumsum(series: "pd.Series[T]") -> "pd.Series[T]":
    return series.cumsum()  # pyright: ignore [reportUnknownMemberType]


class TypedSeries(pd.Series, Generic[T]):  # pyright: ignore [reportMissingTypeArgument]
    def mean(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> float:  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def sum(self) -> T:  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def min(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> T:  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def max(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> T:  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def abs(
        self,
    ) -> "TypedSeries[T]":  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def diff(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> "TypedSeries[T]":  # pyright: ignore [reportGeneralTypeIssues]
        pass
