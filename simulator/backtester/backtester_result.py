from typing import cast
import pandas as pd

from order.order import Order
from market.market_ticker import MarketTicker


class BacktesterResult:
    positions: pd.DataFrame
    tickers: pd.DataFrame

    def __init__(self, closed_orders: list[Order], tickers: pd.DataFrame) -> None:
        super().__init__()
        self.tickers = tickers
        self.positions = self._to_positions(closed_orders)

    def _to_positions(self, closed_orders: list[Order]) -> pd.DataFrame:
        ticker_balance: float = 0
        ticker_balances: list[float] = []

        # TODO how to calculate balance via Pandas
        for closed_order in closed_orders:
            closed_order_pnl = closed_order.get_pnl()
            assert closed_order_pnl is not None
            ticker_balance = ticker_balance + closed_order_pnl
            ticker_balances.append(ticker_balance)

        return pd.DataFrame(
            {
                "entry_timestamp": list(
                    (
                        closed_order.entry_ticker.timestamp
                        for closed_order in closed_orders
                    )
                ),
                "exit_timestamp": list(
                    (
                        cast(MarketTicker, closed_order.exit_ticker).timestamp
                        for closed_order in closed_orders
                    )
                ),
                "side": list(
                    (closed_order.side.name for closed_order in closed_orders)
                ),
                "entry_price": list(
                    (closed_order.get_entry_price() for closed_order in closed_orders)
                ),
                "exit_price": list(
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
                "pnl": list((closed_order.get_pnl() for closed_order in closed_orders)),
                "balance": ticker_balances,
            }
        )

    def get_positions_count(self):
        return len(self.positions.index)

    def get_positions_average_price_margin(self):
        return self.positions.price_margin.mean()

    def get_positions_average_pnl(self):
        return self.positions.pnl.mean()

    # TODO
    def get_transactions_average_return(self):
        return self.positions.entry_price.mean()

    # TODO
    def get_transactions_cumulative_return(self):
        return self.positions.entry_price.sum()

    def get_positions_balance(self):
        return (
            self.positions.balance.iloc[-1]
            if self.get_positions_count() > 0
            else 0
        )

    def get_average_tickers_price_change(self):
        return self.tickers.ask_price.diff().abs().mean()

    def get_interval_days(self):
        min_timestamp = self.tickers.timestamp.min()
        max_timestamp = self.tickers.timestamp.max()
        return (max_timestamp - min_timestamp) / (1.0 * 24 * 60 * 60 * 1000)
