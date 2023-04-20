from functools import reduce

import pandas as pd

from trade.trade_simulator_order import TradeSimulatorOrder
from trade.trade_simulator_order_type import TradeSimulatorOrderType
from trade.trade_simulator_tick import TradeSimulatorTick


class TradeSimulator:
    check_point_tick: TradeSimulatorTick | None
    orders: [TradeSimulatorOrder]

    def __init__(self) -> None:
        self.check_point_tick = None
        self.orders: [TradeSimulatorOrder] = []

    def process_ticks(self, ticks: pd.DataFrame, price_step_ratio: float):
        for i in range(len(ticks.timestamp)):
            tick = self._get_tick(ticks, i)

            self._notify_orders(tick)

            if self.check_point_tick is None:
                self.check_point_tick = tick
                # print(f"Initial checkpoint set at {tick.get_date_time()} and bid price: {tick.bid_price}")

            elif self.check_point_tick.is_growth_step(tick, price_step_ratio):
                order = TradeSimulatorOrder(tick, TradeSimulatorOrderType.SELL, price_step_ratio)
                self.orders.append(order)
                self.check_point_tick = tick
                # print(f"New Order: {order.id} {order.open_tick.get_date_time()} {order.type} {order.get_open_price()}")

            elif self.check_point_tick.is_falling_step(tick, price_step_ratio):
                order = TradeSimulatorOrder(tick, TradeSimulatorOrderType.BUY, price_step_ratio)
                self.orders.append(order)
                self.check_point_tick = tick
                # print(f"New Order: {order.id} {order.open_tick.get_date_time()} {order.type} {order.get_open_price()}")

    def get_closed_orders(self):
        return list(filter(lambda order: not order.is_open, self.orders))

    def get_cumulative_profit(self) -> float:
        return reduce(lambda profit, order: profit + order.get_profit(), self.get_closed_orders(), 0)

    def get_profits(self) -> [float]:
        closed_orders = self.get_closed_orders()

        cumulative_profit: float = 0
        cumulative_profits: [float] = []

        for closed_order in closed_orders:
            cumulative_profit = cumulative_profit + closed_order.get_profit()
            cumulative_profits.append(cumulative_profit)

        return pd.DataFrame({
            'timestamp': list((closed_order.open_tick.timestamp for closed_order in closed_orders)),
            'type': list((closed_order.type.name for closed_order in closed_orders)),
            'open_price': list((closed_order.get_open_price() for closed_order in closed_orders)),
            'close_price': list((closed_order.get_close_price() for closed_order in closed_orders)),
            'profit': list((closed_order.get_profit() for closed_order in closed_orders)),
            'cumulative_profit': cumulative_profits,
        })

    def _notify_orders(self, tick):
        order: TradeSimulatorOrder
        for order in self.orders:
            order.notify(tick)

    @staticmethod
    def _get_tick(ticks: pd.DataFrame, index: int):
        tick_timestamp = ticks.timestamp[index]
        tick_bid_price = ticks.bid_price[index]
        tick_ask_price = ticks.ask_price[index]
        return TradeSimulatorTick(tick_timestamp, tick_bid_price, tick_ask_price)
