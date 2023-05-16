from typing import Iterable, NamedTuple
import pandas as pd

from utils.series import TypedSeries


class MarketTicker:
    timestamp: int
    ask_price: float
    bid_price: float

    def __init__(self, timestamp: int, bid_price: float, ask_price: float):
        self.timestamp = timestamp
        self.ask_price = ask_price
        self.bid_price = bid_price
        if ask_price <= bid_price:
            raise ValueError(
                f"Ask price (${ask_price}) should be > than bid price (${bid_price})."
            )


MarketTickersDataFrameRowTuple = NamedTuple(
    "Pandas", timestamp=int, bid_price=float, ask_price=float
)


class MarketTikersDataFrame(pd.DataFrame):
    timestamp: TypedSeries[int]
    bid_price: TypedSeries[float]
    ask_price: TypedSeries[float]

    def itertuples(  # pyright: ignore [reportIncompatibleMethodOverride]
        self,
    ) -> Iterable[MarketTickersDataFrameRowTuple]:
        return self.itertuples()
