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
    is_open: bool
    stop_loss_take_profit_ratio: float

    def __init__(self, tick: TradeSimulatorTick, type: TradeSimulatorOrderType, stop_loss_take_profit_ratio: float):
        self.type = type
        self.open_tick = tick
        self.close_tick = None
        self.is_open = True
        self.stop_loss_take_profit_ratio = stop_loss_take_profit_ratio

    def get_profit(self):
        return self._get_profit(self.close_tick)

    def close(self, tick: TradeSimulatorTick):
        self.close_tick = tick
        self.is_open = False
        print(f"Closed Order: {tick.get_date_time()}, {self.type}, "
              + f"{tick.bid_price if self.type is TradeSimulatorOrderType.BUY else tick.ask_price}")

    def on_new_tick(self, tick: TradeSimulatorTick):
        if not self.is_open:
            return

        if self._should_auto_close(tick):
            self.close(tick)

    def _get_profit(self, new_tick: TradeSimulatorTick):
        return (new_tick.bid_price - self.open_tick.ask_price
                if self.type is TradeSimulatorOrderType.BUY
                else self.open_tick.bid_price - new_tick.ask_price)

    def _should_auto_close(self, tick: TradeSimulatorTick):
        profit = self._get_profit(tick)
        profit_ratio = (profit / self.open_tick.ask_price
                        if self.type is TradeSimulatorOrderType.BUY
                        else profit / self.open_tick.bid_price)
        return profit_ratio >= abs(self.stop_loss_take_profit_ratio)


class TradeSimulator:
    check_point_tick: TradeSimulatorTick | None
    orders: [TradeSimulatorOrder]

    def __init__(self) -> None:
        self.check_point_tick = None
        self.orders: [TradeSimulatorOrder] = []

    def process_ticks(self, ticks: pd.DataFrame, price_step_ratio: float):
        for i in range(len(ticks.timestamp)):
            tick = self._get_tick(ticks, i)

            order: TradeSimulatorOrder
            for order in self.orders:
                order.on_new_tick(tick)

            if self.check_point_tick is None:
                self.check_point_tick = tick
                print(f"Initial checkpoint set at {tick.get_date_time()} and bid price: {tick.bid_price}")

            elif self.check_point_tick.is_growth_step(tick, price_step_ratio):
                self.orders.append(TradeSimulatorOrder(tick, TradeSimulatorOrderType.SELL, price_step_ratio))
                self.check_point_tick = tick
                print(f"New Order: {tick.get_date_time()}, SELL, {tick.bid_price}")

            elif self.check_point_tick.is_falling_step(tick, price_step_ratio):
                self.orders.append(TradeSimulatorOrder(tick, TradeSimulatorOrderType.BUY, price_step_ratio))
                self.check_point_tick = tick
                print(f"New Order: {tick.get_date_time()}, BUY , {tick.ask_price}")

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
