import pandas as pd

# from binance.binance_k_line_loader import load_binance_k_lines
# from binance.binance_tick_loader import load_binance_ticks
# from chart.ttm_chart import draw_line_chart
from binance.binance_k_line_loader import load_binance_k_lines
from binance.binance_tick_loader import load_binance_ticks
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

            order: TradeSimulatorOrder
            for order in self.orders:
                order.on_new_tick(tick)

            if self.check_point_tick is None:
                self.check_point_tick = tick
                print(f"Initial checkpoint set at {tick.get_date_time()} and bid price: {tick.bid_price}")

            elif self.check_point_tick.is_growth_step(tick, price_step_ratio):
                order = TradeSimulatorOrder(tick, TradeSimulatorOrderType.SELL, price_step_ratio)
                self.orders.append(order)
                self.check_point_tick = tick
                print(f"New Order: {order.id} {order.open_tick.get_date_time()} {order.type} {order.get_open_price()}")

            elif self.check_point_tick.is_falling_step(tick, price_step_ratio):
                order = TradeSimulatorOrder(tick, TradeSimulatorOrderType.BUY, price_step_ratio)
                self.orders.append(order)
                self.check_point_tick = tick
                print(f"New Order: {order.id} {order.open_tick.get_date_time()} {order.type} {order.get_open_price()}")

    @staticmethod
    def _get_tick(ticks: pd.DataFrame, index: int):
        tick_timestamp = ticks.timestamp[index]
        tick_bid_price = ticks.bid_price[index]
        tick_ask_price = ticks.ask_price[index]
        return TradeSimulatorTick(tick_timestamp, tick_bid_price, tick_ask_price)


k_lines = load_binance_k_lines(f"../../../ttm-data/ETHUSDT-1s-2023-03-01.csv")
ticks = load_binance_ticks(k_lines, 0.01)

trade_simulator: TradeSimulator = TradeSimulator()
trade_simulator.process_ticks(ticks, 0.01)
