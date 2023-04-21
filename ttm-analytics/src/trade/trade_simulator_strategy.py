from abc import ABC, abstractmethod

from trade.trade_simulator_order import TradeSimulatorOrder
from trade.trade_simulator_tick import TradeSimulatorTick


class TradeSimulatorStrategy(ABC):
    description: str

    def __init__(self, description: str) -> None:
        super().__init__()
        self.description = description

    @abstractmethod
    def process_tick(self, new_tick: TradeSimulatorTick,
                     orders: [TradeSimulatorOrder], closed_orders: [TradeSimulatorOrder]):
        pass

    def __str__(self) -> str:
        return self.description
