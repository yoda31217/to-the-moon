import pandas as pd


class TradeSimulatorTransactions:
    data_frame: pd.DataFrame

    def __init__(self, data_frame: pd.DataFrame) -> None:
        super().__init__()
        self.data_frame = data_frame
