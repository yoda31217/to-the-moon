import pandas as pd


class TradeSimulatorTransactions:
    data_frame: pd.DataFrame

    def __init__(self, data_frame: pd.DataFrame) -> None:
        super().__init__()
        self.data_frame = data_frame

    def get_count(self):
        return len(self.data_frame.index)

    def get_average_price_margin(self):
        return self.data_frame.price_margin.mean()

    def get_average_profit(self):
        return self.data_frame.profit.mean()

    def get_cumulative_profit(self):
        return self.data_frame.cumulative_profit.iloc[-1]
