import pandas as pd


class TradeSimulatorResult:
    transactions: pd.DataFrame

    def __init__(self, data_frame: pd.DataFrame) -> None:
        super().__init__()
        self.transactions = data_frame

    def get_transactions_count(self):
        return len(self.transactions.index)

    def get_transactions_average_price_margin(self):
        return self.transactions.price_margin.mean()

    def get_transactions_average_profit(self):
        return self.transactions.profit.mean()

    def get_transactions_cumulative_profit(self):
        return self.transactions.cumulative_profit.iloc[-1]
