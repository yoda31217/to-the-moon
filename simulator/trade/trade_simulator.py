import typing

import pandas as pd

from order.order import Order
from trade.trade_simulator_result import TradeSimulatorResult
from trade.trade_simulator_strategy import TradeSimulatorStrategy
from trade.trade_simulator_tick import TradeSimulatorTick

TickDataFrameRowTuple = typing.NamedTuple(
    "Employee", timestamp=int, bid_price=float, ask_price=float
)


class TradeSimulator:
    ticks: list[TradeSimulatorTick]
    ticks_data_frame: pd.DataFrame

    def __init__(self, ticks_data_frame: pd.DataFrame) -> None:
        # self.ticks = list((self._to_tick(tick_row) for tick_index, tick_row in ticks_data_frame.iterrows()))
        tick_row: TickDataFrameRowTuple
        self.ticks = list(
            (self._to_tick(tick_row) for tick_row in ticks_data_frame.itertuples())
        )
        self.ticks_data_frame = ticks_data_frame

    def simulate(self, strategy: TradeSimulatorStrategy) -> TradeSimulatorResult:
        orders: list[Order] = []
        closed_orders: list[Order] = []

        for new_tick in self.ticks:
            self._notify_orders(new_tick, orders)
            strategy.process_tick(new_tick, orders, closed_orders)
            self._move_orders_to_closed(orders, closed_orders)

        self._close_orders(orders, closed_orders)

        return TradeSimulatorResult(closed_orders, self.ticks_data_frame)

    def _close_orders(
        self,
        orders: list[Order],
        closed_orders: list[Order],
    ):
        order: Order
        for order in orders:
            if order.is_open:
                order.close(self.ticks[-1])
        self._move_orders_to_closed(orders, closed_orders)

    @staticmethod
    def _move_orders_to_closed(orders: list[Order], closed_orders: list[Order]):
        new_closed_orders = [order for order in orders if not order.is_open]
        closed_orders.extend(new_closed_orders)

        open_orders = [order for order in orders if order.is_open]
        orders.clear()
        orders.extend(open_orders)

    @staticmethod
    def _notify_orders(tick, orders: list[Order]):
        order: Order
        for order in orders:
            order.notify(tick)

    @staticmethod
    def _to_tick(tick_row: TickDataFrameRowTuple):
        return TradeSimulatorTick(
            tick_row.timestamp, tick_row.bid_price, tick_row.ask_price
        )
