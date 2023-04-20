from datetime import datetime
from enum import Enum

import pandas as pd

# from binance.binance_k_line_loader import load_binance_k_lines
# from binance.binance_tick_loader import load_binance_ticks
# from chart.ttm_chart import draw_line_chart
from binance.binance_k_line_loader import load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks


class TradeSimulatorTick:
    timestamp: int
    ask_price: float
    bid_price: float

    def __init__(self, timestamp: int, bid_price: float, ask_price: float):
        self.timestamp = timestamp
        self.ask_price = ask_price
        self.bid_price = bid_price

    def get_date_time(self):
        return datetime.utcfromtimestamp(self.timestamp / 1000)

    def is_growth_step(self, tick: 'TradeSimulatorTick', price_step_ratio: float):
        return tick.bid_price >= self.ask_price + self.ask_price * price_step_ratio

    def is_falling_step(self, tick: 'TradeSimulatorTick', price_step_ratio: float):
        return tick.ask_price <= self.bid_price - self.bid_price * price_step_ratio


class TradeSimulatorOrderType(Enum):
    BUY = 0
    SELL = 1


class TradeSimulatorOrder:
    type: TradeSimulatorOrderType
    open_tick: TradeSimulatorTick
    close_tick: TradeSimulatorTick | None

    def __init__(self, tick: TradeSimulatorTick, type: TradeSimulatorOrderType) -> None:
        self.type = type
        self.open_tick = tick


class TradeSimulator:
    check_point_tick: TradeSimulatorTick | None
    orders: [TradeSimulatorOrder]

    def __init__(self) -> None:
        self.check_point_tick = None
        self.orders = []

    def process_ticks(self, ticks: pd.DataFrame, price_step_ratio: float):
        for i in range(len(ticks.timestamp)):
            tick = self._get_tick(ticks, i)

            if self.check_point_tick is None:
                self.check_point_tick = tick
                print(f"Initial checkpoint set at {tick.get_date_time()} and bid price: {tick.bid_price}")
                continue

            if self.check_point_tick.is_growth_step(tick, price_step_ratio):
                order = TradeSimulatorOrder(tick, TradeSimulatorOrderType.SELL)
                self.orders.append(order)
                self.check_point_tick = tick
                print(f"New Order: {tick.get_date_time()}, SELL, {tick.bid_price}")
                continue

            if self.check_point_tick.is_falling_step(tick, price_step_ratio):
                order = TradeSimulatorOrder(tick, TradeSimulatorOrderType.BUY)
                self.orders.append(order)
                self.check_point_tick = tick
                print(f"New Order: {tick.get_date_time()}, BUY , {tick.ask_price}")
                continue

    @staticmethod
    def _get_tick(ticks, i):
        tick_timestamp = ticks.timestamp[i]
        tick_bid_price = ticks.bid_price[i]
        tick_ask_price = ticks.ask_price[i]
        return TradeSimulatorTick(tick_timestamp, tick_bid_price, tick_ask_price)


k_lines = load_binance_k_lines(f"../../../ttm-data/ETHUSDT-1s-2023-03-01.csv")
ticks = load_binance_ticks(k_lines, 0.01)

trade_simulator: TradeSimulator = TradeSimulator()
trade_simulator.process_ticks(ticks, 0.01)
