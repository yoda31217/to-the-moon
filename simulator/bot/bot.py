from abc import ABC, abstractmethod

from order.order import Order
from market.market_tick import MarketTick


class Bot(ABC):
    description: str

    def __init__(self, description: str) -> None:
        super().__init__()
        self.description = description

    @abstractmethod
    def  process_tick(self, new_tick: MarketTick,
                     orders: list[Order], closed_orders: list[Order]):
        pass

    def __str__(self) -> str:
        return self.description
