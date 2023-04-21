import pandas as pd


class TradeSimulatorResult:
    transactions: pd.DataFrame
    ticks: pd.DataFrame

    def __init__(self, data_frame: pd.DataFrame, ticks: pd.DataFrame) -> None:
        super().__init__()
        self.transactions = data_frame
        self.ticks = ticks

    def get_transactions_count(self):
        return len(self.transactions.index)

    def get_transactions_average_price_margin(self):
        return self.transactions.price_margin.mean()

    def get_transactions_average_profit(self):
        return self.transactions.profit.mean()

    def get_transactions_cumulative_profit(self):
        return self.transactions.cumulative_profit.iloc[-1]

    def get_average_ticks_price_change(self):
        return self.ticks.ask_price.diff().abs().mean()

    def get_interval_days(self):
        min_timestamp = self.ticks.timestamp.min()
        max_timestamp = self.ticks.timestamp.max()
        return (max_timestamp - min_timestamp) / (1.0 * 24 * 60 * 60 * 1000)
