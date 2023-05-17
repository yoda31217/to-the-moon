from abc import ABC, abstractmethod

from order.order import Order
from market.market_ticker import MarketTicker

BotConfig = dict[str, object]


class Bot(ABC):
    config: BotConfig

    def __init__(self, config: BotConfig) -> None:
        super().__init__()
        self.config = config

    @abstractmethod
    def process_ticker(
        self, new_ticker: MarketTicker, orders: list[Order], closed_orders: list[Order]
    ):
        pass

    def get_name(self) -> str:
        return self.__class__.__name__
