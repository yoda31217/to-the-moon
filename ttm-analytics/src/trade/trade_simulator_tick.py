from datetime import datetime


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
