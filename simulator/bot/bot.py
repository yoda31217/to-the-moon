from abc import ABC, abstractmethod

from order.order import Order
from market.market_ticker import MarketTicker


class Bot(ABC):
    description: str

    def __init__(self, description: str) -> None:
        super().__init__()
        self.description = description

    @abstractmethod
    def  process_tick(self, new_tick: MarketTicker,
                     orders: list[Order], closed_orders: list[Order]):
        pass

    def __str__(self) -> str:
        return self.description
