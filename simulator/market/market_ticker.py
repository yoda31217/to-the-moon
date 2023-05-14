import pandas as pd


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


class MarketTikersDataFrame(pd.DataFrame):
    timestamp: pd.Series[int]
    bid_price: pd.Series[float]
    ask_price: pd.Series[float]
