from abc import ABC, abstractmethod

from order.order import Order
from trade.trade_simulator_tick import TradeSimulatorTick


class TradeSimulatorStrategy(ABC):
    description: str

    def __init__(self, description: str) -> None:
        super().__init__()
        self.description = description

    @abstractmethod
    def process_tick(self, new_tick: TradeSimulatorTick,
                     orders: list[Order], closed_orders: list[Order]):
        pass

    def __str__(self) -> str:
        return self.description
