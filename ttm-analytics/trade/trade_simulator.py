import pandas as pd


class TradeSimulatorTick:
    def __init__(self, timestamp: int, bid_price: float, ask_price: float):
        self.timestamp = timestamp
        self.bid_price = bid_price
        self.ask_price = ask_price


class TradeSimulator:
    def process_ticks(self, ticks: pd.DataFrame):
        ticks2 = []

        for i in range(len(ticks.timestamp)):
            tick_timestamp = ticks.timestamp[i]
            tick_bid_price = ticks.bid_price[i]
            tick_ask_price = ticks.ask_price[i]
            tick = TradeSimulatorTick(tick_timestamp, tick_bid_price, tick_ask_price)
            ticks2.append(tick)

        return ticks2
