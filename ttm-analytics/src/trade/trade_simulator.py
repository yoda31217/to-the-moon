import pandas as pd
# from binance.binance_k_line_loader import load_binance_k_lines
# from binance.binance_tick_loader import load_binance_ticks
# from chart.ttm_chart import draw_line_chart


class TradeSimulatorTick:
    def __init__(self, timestamp: int, bid_price: float, ask_price: float):
        self.timestamp: int = timestamp
        self.bid_price: float = bid_price
        self.ask_price: float = ask_price


class TradeSimulator:

    def __init__(self) -> None:
        self.checkPointTick: TradeSimulatorTick | None = None

    def process_ticks(self, ticks: pd.DataFrame):
        ticks2 = []

        for i in range(len(ticks.timestamp)):
            tick_timestamp = ticks.timestamp[i]
            tick_bid_price = ticks.bid_price[i]
            tick_ask_price = ticks.ask_price[i]
            tick = TradeSimulatorTick(tick_timestamp, tick_bid_price, tick_ask_price)
            ticks2.append(tick)

        return ticks2



# k_lines = load_binance_k_lines(f"../ttm-data/{symbol}-{symbol_k_lines_interval}-2023-03-01.csv")
#
# ticks = load_binance_ticks(k_lines, symbol_ask_bid_price_difference)

