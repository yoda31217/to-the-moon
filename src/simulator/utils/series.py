from typing import Generic, TypeVar
import pandas as pd

T = TypeVar("T", float, int, str)


class TypedSeries(pd.Series, Generic[T]):  # pyright: ignore [reportMissingTypeArgument]
    def mean(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> float:  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def median(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> T:  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def mode(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> "TypedSeries[T]":  # pyright: ignore [reportGeneralTypeIssues]
        pass

    def sum(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> T:  # pyright: ignore [reportGeneralTypeIssues]
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

    def cumsum(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> "TypedSeries[T]":  # pyright: ignore [reportGeneralTypeIssues]
        pass
