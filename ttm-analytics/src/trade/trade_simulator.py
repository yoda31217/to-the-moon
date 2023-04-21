from functools import reduce

import pandas as pd

from trade.trade_simulator_order import TradeSimulatorOrder
from trade.trade_simulator_strategy import TradeSimulatorStrategy
from trade.trade_simulator_tick import TradeSimulatorTick


class TradeSimulator:
    orders: [TradeSimulatorOrder]
    closed_orders: [TradeSimulatorOrder]
    ticks: [TradeSimulatorTick]

    def __init__(self, ticks_data_frame: pd.DataFrame) -> None:
        self.orders: [TradeSimulatorOrder] = []
        self.closed_orders = []
        self.ticks = list((self._to_tick(tick_row) for tick_index, tick_row in ticks_data_frame.iterrows()))

    def simulate(self, strategy: TradeSimulatorStrategy):
        for new_tick in self.ticks:
            self._notify_orders(new_tick)
            strategy.process_tick(new_tick, self.orders, self.closed_orders)
            self._move_orders_to_closed()

        self._close_orders()

    def get_cumulative_profit(self) -> float:
        return reduce(lambda profit, order: profit + order.get_profit(), self.closed_orders, 0)

    def get_profits(self) -> [float]:
        cumulative_profit: float = 0
        cumulative_profits: [float] = []

        for closed_order in self.closed_orders:
            cumulative_profit = cumulative_profit + closed_order.get_profit()
            cumulative_profits.append(cumulative_profit)

        return pd.DataFrame({
            'open_timestamp': list((closed_order.open_tick.timestamp for closed_order in self.closed_orders)),
            'type': list((closed_order.type.name for closed_order in self.closed_orders)),
            'open_price': list((closed_order.get_open_price() for closed_order in self.closed_orders)),
            'close_price': list((closed_order.get_close_price() for closed_order in self.closed_orders)),
            'close_timestamp': list((closed_order.close_tick.timestamp for closed_order in self.closed_orders)),
            'profit': list((closed_order.get_profit() for closed_order in self.closed_orders)),
            'cumulative_profit': cumulative_profits,
        })

    def _close_orders(self):
        order: TradeSimulatorOrder
        for order in self.orders:
            if order.is_open:
                order.close(self.ticks[-1])
        self._move_orders_to_closed()

    def _move_orders_to_closed(self):
        self.closed_orders.extend(list(filter(lambda order: not order.is_open, self.orders)))
        self.orders = list(filter(lambda order: order.is_open, self.orders))

    def _notify_orders(self, tick):
        order: TradeSimulatorOrder
        for order in self.orders:
            order.notify(tick)

    @staticmethod
    def _to_tick(tick_row: pd.Series):
        return TradeSimulatorTick(
            tick_row.get('timestamp'),
            tick_row.get('bid_price'),
            tick_row.get('ask_price'))
