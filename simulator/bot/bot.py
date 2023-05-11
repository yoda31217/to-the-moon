from abc import ABC, abstractmethod

from order.order import Order
from market.market_ticker import MarketTicker


class Bot(ABC):
    config: dict

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config

    @abstractmethod
    def process_ticker(
        self, new_ticker: MarketTicker, orders: list[Order], closed_orders: list[Order]
    ):
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {str(self.config)}"
