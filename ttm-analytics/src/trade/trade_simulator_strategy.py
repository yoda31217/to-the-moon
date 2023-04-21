from abc import ABC, abstractmethod

from trade.trade_simulator_order import TradeSimulatorOrder
from trade.trade_simulator_tick import TradeSimulatorTick


class TradeSimulatorStrategy(ABC):
    @abstractmethod
    def process_tick(self, new_tick: TradeSimulatorTick,
                     orders: [TradeSimulatorOrder], closed_orders: [TradeSimulatorOrder]):
        pass
