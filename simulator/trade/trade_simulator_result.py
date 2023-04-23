import pandas as pd

from trade.trade_simulator_order import TradeSimulatorOrder


class TradeSimulatorResult:
    transactions: pd.DataFrame
    ticks: pd.DataFrame

    def __init__(
        self, closed_orders: [TradeSimulatorOrder], ticks: pd.DataFrame
    ) -> None:
        super().__init__()
        self.ticks = ticks
        self.transactions = self._to_transactions(closed_orders)

    def _to_transactions(self, closed_orders: [TradeSimulatorOrder]) -> pd.DataFrame:
        cumulative_profit: float = 0
        cumulative_profits: [float] = []

        for closed_order in closed_orders:
            cumulative_profit = cumulative_profit + closed_order.get_profit()
            cumulative_profits.append(cumulative_profit)

        return pd.DataFrame(
            {
                "open_timestamp": list(
                    (closed_order.open_tick.timestamp for closed_order in closed_orders)
                ),
                "type": list(
                    (closed_order.type.name for closed_order in closed_orders)
                ),
                "open_price": list(
                    (closed_order.get_open_price() for closed_order in closed_orders)
                ),
                "close_price": list(
                    (closed_order.get_close_price() for closed_order in closed_orders)
                ),
                "price_margin": list(
                    (
                        abs(
                            closed_order.get_close_price()
                            - closed_order.get_open_price()
                        )
                        for closed_order in closed_orders
                    )
                ),
                "close_timestamp": list(
                    (
                        closed_order.close_tick.timestamp
                        for closed_order in closed_orders
                    )
                ),
                "profit": list(
                    (closed_order.get_profit() for closed_order in closed_orders)
                ),
                "cumulative_profit": cumulative_profits,
            }
        )

    def get_transactions_count(self):
        return len(self.transactions.index)

    def get_transactions_average_price_margin(self):
        return self.transactions.price_margin.mean()

    def get_transactions_average_profit(self):
        return self.transactions.profit.mean()

    def get_transactions_cumulative_profit(self):
        return (
            self.transactions.cumulative_profit.iloc[-1]
            if self.get_transactions_count() > 0
            else 0
        )

    def get_average_ticks_price_change(self):
        return self.ticks.ask_price.diff().abs().mean()

    def get_interval_days(self):
        min_timestamp = self.ticks.timestamp.min()
        max_timestamp = self.ticks.timestamp.max()
        return (max_timestamp - min_timestamp) / (1.0 * 24 * 60 * 60 * 1000)
