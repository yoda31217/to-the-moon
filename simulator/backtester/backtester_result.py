from typing import cast
import pandas as pd
from bot.bot import Bot

from order.order import Order
from market.market_ticker import MarketTicker
from utils import series


class BacktesterResultPositionsDataFrame(pd.DataFrame):
    entry_timestamp: pd.Series[int]
    exit_timestamp: pd.Series[int]
    durarion_millis: pd.Series[int]
    side: pd.Series[str]
    entry_price: pd.Series[float]
    exit_price: pd.Series[float]
    price_margin: pd.Series[float]
    quantity: pd.Series[float]
    initial_margin: pd.Series[float]
    pnl: pd.Series[float]
    roe: pd.Series[float]


class BacktesterResult:
    bot: Bot
    positions: BacktesterResultPositionsDataFrame
    tickers: pd.DataFrame
    balances: pd.DataFrame

    def __init__(
        self,
        bot: Bot,
        closed_orders: list[Order],
        tickers: pd.DataFrame,
        balances: pd.DataFrame,
    ) -> None:
        super().__init__()
        self.bot = bot
        self.tickers = tickers
        self.positions = self._to_positions(closed_orders)
        self.balances = balances

    def _to_positions(
        self, closed_orders: list[Order]
    ) -> BacktesterResultPositionsDataFrame:
        data_frame = pd.DataFrame(
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
                "durarion_millis": list(
                    (
                        cast(MarketTicker, closed_order.exit_ticker).timestamp
                        - closed_order.entry_ticker.timestamp
                        for closed_order in closed_orders
                    )
                ),
                "side": list(
                    (closed_order.side.name for closed_order in closed_orders)
                ),
                "entry_price": list(
                    (closed_order.entry_price for closed_order in closed_orders)
                ),
                "exit_price": list(
                    (closed_order.exit_price for closed_order in closed_orders)
                ),
                "price_margin": list(
                    (
                        abs(
                            cast(float, closed_order.exit_price)
                            - closed_order.entry_price
                        )
                        for closed_order in closed_orders
                    )
                ),
                "quantity": list(
                    (closed_order.quantity for closed_order in closed_orders)
                ),
                "initial_margin": list(
                    (closed_order.initial_margin for closed_order in closed_orders)
                ),
                "pnl": list((closed_order.pnl for closed_order in closed_orders)),
                "roe": list((closed_order.roe for closed_order in closed_orders)),
            }
        )
        return cast(BacktesterResultPositionsDataFrame, data_frame)

    def get_positions_count(self):
        return len(self.positions.index)

    def get_positions_average_price_margin(self) -> float:
        return series.avg(self.positions.price_margin)

    def get_positions_average_pnl(self):
        return series.avg(self.positions.pnl)

    def get_positions_average_duration_millis(self):
        return series.avg(self.positions.durarion_millis)

    def get_positions_average_initial_margin(self):
        return series.avg(self.positions.initial_margin)

    def get_positions_average_quantity(self):
        return series.avg(self.positions.quantity)

    def get_positions_initial_margin_sum(self):
        return series.sum(self.positions.initial_margin)

    def get_positions_average_roe(self):
        return series.avg(self.positions.roe)

    def get_positions_pnl_sum(self):
        return series.sum(self.positions.pnl) if self.get_positions_count() > 0 else 0

    def get_average_tickers_price_change(self):
        return series.avg(self.tickers.ask_price.diff().abs())

    def get_interval_days(self) -> float:
        min_timestamp = series.min(self.tickers.timestamp)
        max_timestamp = series.max(self.tickers.timestamp)
        return (max_timestamp - min_timestamp) / (1.0 * 24 * 60 * 60 * 1000)
