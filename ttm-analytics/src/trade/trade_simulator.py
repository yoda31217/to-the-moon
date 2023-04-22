import typing

import pandas as pd

from trade.trade_simulator_order import TradeSimulatorOrder
from trade.trade_simulator_result import TradeSimulatorResult
from trade.trade_simulator_strategy import TradeSimulatorStrategy
from trade.trade_simulator_tick import TradeSimulatorTick

TickDataFrameRowTuple = typing.NamedTuple('Employee', timestamp=int, bid_price=float, ask_price=float)


class TradeSimulator:
    ticks: [TradeSimulatorTick]
    ticks_data_frame: pd.DataFrame

    def __init__(self, ticks_data_frame: pd.DataFrame) -> None:
        # self.ticks = list((self._to_tick(tick_row) for tick_index, tick_row in ticks_data_frame.iterrows()))
        self.ticks = list((self._to_tick(tick_row) for tick_row in ticks_data_frame.itertuples()))
        self.ticks_data_frame = ticks_data_frame

    def simulate(self, strategy: TradeSimulatorStrategy) -> TradeSimulatorResult:
        orders: [TradeSimulatorOrder] = []
        closed_orders: [TradeSimulatorOrder] = []

        for new_tick in self.ticks:
            self._notify_orders(new_tick, orders)
            strategy.process_tick(new_tick, orders, closed_orders)
            self._move_orders_to_closed(orders, closed_orders)

        self._close_orders(orders, closed_orders)

        return self._to_transactions(closed_orders)

    def _to_transactions(self, closed_orders: [TradeSimulatorOrder]) -> TradeSimulatorResult:
        cumulative_profit: float = 0
        cumulative_profits: [float] = []

        for closed_order in closed_orders:
            cumulative_profit = cumulative_profit + closed_order.get_profit()
            cumulative_profits.append(cumulative_profit)

        return TradeSimulatorResult(pd.DataFrame({
            'open_timestamp': list((closed_order.open_tick.timestamp for closed_order in closed_orders)),
            'type': list((closed_order.type.name for closed_order in closed_orders)),
            'open_price': list((closed_order.get_open_price() for closed_order in closed_orders)),
            'close_price': list((closed_order.get_close_price() for closed_order in closed_orders)),
            'price_margin': list((abs(closed_order.get_close_price() - closed_order.get_open_price())
                                  for closed_order in closed_orders)),
            'close_timestamp': list((closed_order.close_tick.timestamp for closed_order in closed_orders)),
            'profit': list((closed_order.get_profit() for closed_order in closed_orders)),
            'cumulative_profit': cumulative_profits,
        }), self.ticks_data_frame)

    def _close_orders(self, orders: [TradeSimulatorOrder], closed_orders: [TradeSimulatorOrder]):
        order: TradeSimulatorOrder
        for order in orders:
            if order.is_open:
                order.close(self.ticks[-1])
        self._move_orders_to_closed(orders, closed_orders)

    @staticmethod
    def _move_orders_to_closed(orders: [TradeSimulatorOrder], closed_orders: [TradeSimulatorOrder]):
        new_closed_orders = [order for order in orders if not order.is_open]
        closed_orders.extend(new_closed_orders)

        open_orders = [order for order in orders if order.is_open]
        orders.clear()
        orders.extend(open_orders)

    @staticmethod
    def _notify_orders(tick, orders: [TradeSimulatorOrder]):
        order: TradeSimulatorOrder
        for order in orders:
            order.notify(tick)

    @staticmethod
    def _to_tick(tick_row: TickDataFrameRowTuple):
        return TradeSimulatorTick(
            tick_row.timestamp,
            tick_row.bid_price,
            tick_row.ask_price)
