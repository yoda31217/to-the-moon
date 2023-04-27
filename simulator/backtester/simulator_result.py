from typing import cast
import pandas as pd

from order.order import Order
from market.market_ticker import MarketTicker


class SimulatorResult:
    transactions: pd.DataFrame
    ticks: pd.DataFrame

    def __init__(self, closed_orders: list[Order], ticks: pd.DataFrame) -> None:
        super().__init__()
        self.ticks = ticks
        self.transactions = self._to_transactions(closed_orders)

    def _to_transactions(self, closed_orders: list[Order]) -> pd.DataFrame:
        cumulative_profit: float = 0
        cumulative_profits: list[float] = []

        for closed_order in closed_orders:
            closed_order_profit = closed_order.get_pnl()
            assert closed_order_profit is not None
            cumulative_profit = cumulative_profit + closed_order_profit
            cumulative_profits.append(cumulative_profit)

        return pd.DataFrame(
            {
                "open_timestamp": list(
                    (closed_order.entry_ticker.timestamp for closed_order in closed_orders)
                ),
                "type": list(
                    (closed_order.side.name for closed_order in closed_orders)
                ),
                "open_price": list(
                    (closed_order.get_entry_price() for closed_order in closed_orders)
                ),
                "close_price": list(
                    (closed_order.get_exit_price() for closed_order in closed_orders)
                ),
                "price_margin": list(
                    (
                        abs(
                            cast(float, closed_order.get_exit_price())
                            - closed_order.get_entry_price()
                        )
                        for closed_order in closed_orders
                    )
                ),
                "close_timestamp": list(
                    (
                        cast(MarketTicker, closed_order.exit_ticker).timestamp
                        for closed_order in closed_orders
                    )
                ),
                "profit": list(
                    (closed_order.get_pnl() for closed_order in closed_orders)
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

    def get_transactions_average_return(self):
        return self.transactions.open_price.mean()

    def get_transactions_cumulative_return(self):
        return self.transactions.open_price.sum()

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
